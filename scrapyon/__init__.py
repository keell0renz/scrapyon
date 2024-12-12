from scrapyon.prompt import launch_prompt, scrape_prompt, scrape_query_to_prompt
from scrapyon.agent import run_agent
from scrapybara import Scrapybara

from typing import TypeVar, Optional, Literal
from pydantic_core import ValidationError
from pydantic import BaseModel

from playwright.sync_api import sync_playwright

import asyncio

T = TypeVar("T", bound=BaseModel)

scrapybara = Scrapybara()


def launch(
    cmd: str,
    url: Optional[str] = None,
    instance_type: Optional[Literal["small", "medium", "large"]] = "small",
) -> str:  # type: ignore temporary
    """Launch a computer use agent with Scrapybara as a back-end.

    When url is specified, programmatically starts the browser with the given URL first,
    so the agent spends less time opening browser and typing manually.

    Args:
        cmd: The command/instruction for the agent to execute
        url: Optional URL to open in browser before launching the agent

    Returns:
        str: Result from the agent execution
    """

    instance = scrapybara.start(instance_type=instance_type)

    if url:
        cdp_url = instance.browser.start().cdp_url
        playwright = sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp(cdp_url)
        page = browser.new_page()
        page.goto(url)

    try:
        result = asyncio.run(run_agent(launch_prompt(), cmd, instance))
    finally:
        instance.stop()

    return result


def scrape(
    query: T,
    url: Optional[str] = None,
    cmd: Optional[str] = None,
    instance_type: Optional[Literal["small", "medium", "large"]] = "small",
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
    instance = scrapybara.start(instance_type=instance_type)

    if url:
        cdp_url = instance.browser.start().cdp_url
        playwright = sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp(cdp_url)
        page = browser.new_page()
        page.goto(url)

    schema, cmd = scrape_query_to_prompt(query, cmd)
    try:
        result = asyncio.run(run_agent(scrape_prompt(schema), cmd, instance))
    finally:
        instance.stop()

    try:
        return query.model_validate(result)
    except ValidationError as e:
        # TODO potentially handle re-request
        raise e
