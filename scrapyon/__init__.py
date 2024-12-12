from scrapyon.prompt import launch_prompt, scrape_prompt, scrape_query_to_prompt
from scrapyon.agent import run_agent
from scrapybara import Scrapybara

from typing import TypeVar, Optional, Literal
from pydantic_core import ValidationError
from pydantic import BaseModel

from playwright.sync_api import sync_playwright

import asyncio
import os

SCRAPYBARA_API_KEY = os.getenv("SCRAPYBARA_API_KEY")

T = TypeVar("T", bound=BaseModel)

scrapybara = Scrapybara(api_key=SCRAPYBARA_API_KEY)


async def launch(
    cmd: str,
    url: Optional[str] = None,
    instance_type: Optional[Literal["small", "medium", "large"]] = "small",
    verbose: bool = False,
) -> str:  # type: ignore temporary
    """Launch a computer use agent with Scrapybara as a back-end.

    When url is specified, programmatically starts the browser with the given URL first,
    so the agent spends less time opening browser and typing manually.

    Args:
        cmd: The command/instruction for the agent to execute
        url: Optional URL to open in browser before launching the agent
        instance_type: By default "small", but also can be "medium" or "large"
        verbose: If True, prints detailed progress information

    Returns:
        str: Result from the agent execution
    """

    instance = scrapybara.start(instance_type=instance_type)

    if url:
        try:
            cdp_url = instance.browser.start().cdp_url
            with sync_playwright() as playwright:
                browser = playwright.chromium.connect_over_cdp(cdp_url)
                page = browser.new_page()
                page.goto(url)
                page.wait_for_load_state("load")  # Ensure the page is fully loaded
        except:
            pass

    try:
        result = await run_agent(launch_prompt(), cmd, instance, verbose=verbose)
    finally:
        instance.stop()

    return result


async def scrape(
    query: T,
    url: Optional[str] = None,
    cmd: Optional[str] = None,
    instance_type: Optional[Literal["small", "medium", "large"]] = "small",
    verbose: bool = False,
) -> T:  # type: ignore temporary
    """Use an agent as an intelligent information retriever.

    Allows retrieving information that requires agentic behavior by defining
    the query and response structure using a Pydantic model.

    Args:
        query: A Pydantic model class defining the query structure and response fields
        url: Optional URL to open in browser before launching the agent
        cmd: Optional command which overrides the query model docstring
        instance_type: By default "small", but also can be "medium" or "large"
        verbose: If True, prints detailed progress information

    Returns:
        T: Instance of the provided Pydantic model containing the retrieved information
    """
    instance = scrapybara.start(instance_type=instance_type)

    if url:
        try:
            cdp_url = instance.browser.start().cdp_url
            with sync_playwright() as playwright:
                browser = playwright.chromium.connect_over_cdp(cdp_url)
                page = browser.new_page()
                page.goto(url)
                page.wait_for_load_state("load")  # Ensure the page is fully loaded
        except:
            pass

    schema, cmd = scrape_query_to_prompt(query, cmd)
    try:
        result = await run_agent(scrape_prompt(schema), cmd, instance, verbose=verbose)
    finally:
        instance.stop()

    try:
        return query.model_validate(result)
    except ValidationError as e:
        # TODO potentially handle re-request
        raise e
