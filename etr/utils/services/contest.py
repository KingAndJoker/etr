from urllib.parse import urlparse

from etr.schemas.contest import ContestUrl


def parse_url(contest_url: str) -> ContestUrl:
    parse = urlparse(contest_url)
    return ContestUrl(
        protocol=parse.scheme,
        host=parse.netloc,
        port=parse.port,
        path=parse.path,
        params=parse.params
    )
