import os
import re
from pathlib import Path

import settings

GITHUB_PACKAGE_LINK_PATTERN = re.compile(r'https?://github\.com/(?:[^/\s]+/)+(?:wlhd-[A-Za-z]+-package|)')


def link_is_valid(link: str) -> bool:
    """
    Checks if link is valid
    """
    return bool(GITHUB_PACKAGE_LINK_PATTERN.match(link))


def inject_github_token(url: str) -> str:
    """
    Injects github token into the environment
    """
    return url.replace('https://github.com', f'https://{settings.GITHUB_USERNAME}:{settings.GITHUB_TOKEN}@github.com')


def purge(file_or_dir: str | Path):
    file_or_dir = Path(file_or_dir) if isinstance(file_or_dir, str) else file_or_dir
    if not file_or_dir.exists():
        return
    if not file_or_dir.is_dir():
        file_or_dir.unlink()
        return
    for item in file_or_dir.iterdir():
        os.chmod(item, 0o777)
        if item.is_dir():
            purge(item)
        else:
            item.unlink()
    file_or_dir.rmdir()
