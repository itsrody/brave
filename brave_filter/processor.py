from enum import Enum, auto
import re
from typing import Iterable, List

# Regular expressions used to inspect incoming rules
COMMENT_RE = re.compile(r'^(#|!)')
HOSTS_RE = re.compile(r'^(?:0\.0\.0\.0|127\.0\.0\.1)\s+')


class RuleCategory(Enum):
    """Classification for incoming filter rules."""
    NATIVE_VALID = auto()
    NEED_REPHRASE = auto()
    UNSUPPORTED = auto()


def is_comment(line: str) -> bool:
    """Return True if the line is a comment."""
    return bool(COMMENT_RE.match(line))


def rewrite_host_rule(line: str) -> str:
    """Convert a hosts-file style rule to Brave adblock syntax."""
    match = HOSTS_RE.match(line)
    if match:
        # Strip out any trailing comment and extract the domain
        remainder = line[match.end():].split()[0]
        if remainder:
            return f"||{remainder}^"
    return ""


def categorize_rule(line: str) -> RuleCategory:
    """Determine the category for a single rule."""
    line = line.strip()
    if not line or is_comment(line):
        return RuleCategory.UNSUPPORTED
    if HOSTS_RE.match(line):
        return RuleCategory.NEED_REPHRASE
    return RuleCategory.NATIVE_VALID


def validate_rule(line: str) -> bool:
    """Return True if the rule is natively valid for Brave."""
    return categorize_rule(line) == RuleCategory.NATIVE_VALID


def _merge(left: List[str], right: List[str]) -> List[str]:
    """Merge two lists of rules based on their categories."""
    result: List[str] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if categorize_rule(left[i]).value <= categorize_rule(right[j]).value:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def _merge_sort_rules(rules: List[str]) -> List[str]:
    """Sort rules based on category using a merge sort."""
    if len(rules) <= 1:
        return rules
    mid = len(rules) // 2
    left = _merge_sort_rules(rules[:mid])
    right = _merge_sort_rules(rules[mid:])
    return _merge(left, right)


def process_rules(lines: Iterable[str]) -> List[str]:
    """Process and rephrase rules for Brave.

    The incoming rules are first sorted into categories using a merge sort.
    Native valid rules are kept as-is, rules needing rephrase are converted,
    and unsupported rules are discarded.
    """
    rules = [line.strip() for line in lines]
    sorted_rules = _merge_sort_rules(rules)
    processed: List[str] = []
    for line in sorted_rules:
        category = categorize_rule(line)
        if category == RuleCategory.NATIVE_VALID:
            processed.append(line)
        elif category == RuleCategory.NEED_REPHRASE:
            rewritten = rewrite_host_rule(line)
            if rewritten:
                processed.append(rewritten)
    return processed
