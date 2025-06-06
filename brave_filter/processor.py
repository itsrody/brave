import re
from typing import Iterable, List

COMMENT_RE = re.compile(r'^(#|!)')
HOSTS_RE = re.compile(r'^(?:0\.0\.0\.0|127\.0\.0\.1)\s+')


def is_comment(line: str) -> bool:
    return bool(COMMENT_RE.match(line))


def rewrite_host_rule(line: str) -> str:
    match = HOSTS_RE.match(line)
    if match:
        domain = line[match.end():].strip()
        if domain:
            return f"||{domain}^"
    return ''


def validate_rule(line: str) -> bool:
    if not line or is_comment(line):
        return False
    if HOSTS_RE.match(line):
        return False
    return True


def process_rules(lines: Iterable[str]) -> List[str]:
    processed: List[str] = []
    for line in lines:
        line = line.strip()
        if validate_rule(line):
            processed.append(line)
        else:
            rewritten = rewrite_host_rule(line)
            if rewritten:
                processed.append(rewritten)
    return processed
