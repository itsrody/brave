import concurrent.futures
import urllib.request
from typing import List, Dict

DEFAULT_FILTERS: Dict[str, str] = {
    "adguard": "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/EnglishFilter/sections/adservers.txt",
    "adblock_plus": "https://easylist-downloads.adblockplus.org/easylist.txt",
    "ublock": "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt",
    "hosts": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
}

def fetch_url(url: str) -> List[str]:
    """Fetch a filter list from a URL and return lines."""
    with urllib.request.urlopen(url) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
    return content.splitlines()

def fetch_filters(urls: Dict[str, str] = None) -> Dict[str, List[str]]:
    """Fetch multiple filter lists in parallel."""
    urls = urls or DEFAULT_FILTERS
    results: Dict[str, List[str]] = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_name = {executor.submit(fetch_url, url): name for name, url in urls.items()}
        for future in concurrent.futures.as_completed(future_to_name):
            name = future_to_name[future]
            try:
                results[name] = future.result()
            except Exception as exc:
                results[name] = []
    return results
