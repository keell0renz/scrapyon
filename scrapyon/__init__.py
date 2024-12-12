from typing import TypeVar
from pydantic import BaseModel
from typing import Optional

T = TypeVar("T", bound=BaseModel)


def launch(cmd: str, url: Optional[str]) -> str:  # type: ignore temporary
    pass


def scrape(
    query: T,
    url: Optional[str],
) -> T:  # type: ignore temporary
    pass
