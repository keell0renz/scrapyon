from typing import TypeVar
from pydantic import BaseModel
from typing import Optional

T = TypeVar("T", bound=BaseModel)


def launch(cmd: str, url: Optional[str] = None) -> str:  # type: ignore temporary
    """Launch a computer use agent with Scrapybara as a back-end.

    When url is specified, programmatically starts the browser with the given URL first,
    so the agent spends less time opening browser and typing manually.

    Args:
        cmd: The command/instruction for the agent to execute
        url: Optional URL to open in browser before launching the agent

    Returns:
        str: Result from the agent execution
    """
    pass


def scrape(
    query: T,
    url: Optional[str] = None,
    cmd: Optional[str] = None,
) -> T:  # type: ignore temporary
    """Use an agent as an intelligent information retriever.

    Allows retrieving information that requires agentic behavior by defining
    the query and response structure using a Pydantic model.

    Args:
        query: A Pydantic model class defining the query structure and response fields
        url: Optional URL to open in browser before launching the agent
        cmd: Optional command which overrides the query model docstring

    Returns:
        T: Instance of the provided Pydantic model containing the retrieved information
    """
    pass
