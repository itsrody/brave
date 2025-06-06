from datetime import datetime
from typing import Dict, Iterable, List

from .processor import process_rules

HEADER_TEMPLATE = """! Title: Rody's Brave List
! Author: Murtaza Salih
! Version: {version}
! Generated on: {generated}
"""

def generate_unified_list(data: Dict[str, Iterable[str]]) -> List[str]:
    processed_lines: List[str] = []
    for name, lines in data.items():
        processed_lines.extend(process_rules(lines))
    # Remove duplicates while preserving order
    seen = set()
    unique_lines = []
    for line in processed_lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)
    header = HEADER_TEMPLATE.format(
        version=datetime.utcnow().strftime('%Y%m%d%H%M%S'),
        generated=datetime.utcnow().isoformat(),
    )
    return header.splitlines() + unique_lines
