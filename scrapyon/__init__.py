from scrapyon._prompt import launch_prompt, scrape_prompt, scrape_query_to_prompt
from scrapyon.tools import ToolCollection, ComputerTool, BashTool, EditTool
from scrapyon._helpers import open_url, extract_json
from scrapyon._agent import run_agent
from scrapybara import Scrapybara
from scrapyon._logging import logger, setup_logging

from typing import TypeVar, Optional, Literal
from pydantic_core import ValidationError
from pydantic import BaseModel

import logging

T = TypeVar("T", bound=BaseModel)

scrapybara = Scrapybara()
logger = logging.getLogger(__name__)


def launch(
    cmd: str,
    url: Optional[str] = None,
    tools: Optional[ToolCollection] = None,
    instance_type: Optional[Literal["small", "medium", "large"]] = "small",
    verbose: bool = False,
) -> list[dict]:  # type: ignore temporary
    """Launch an agent to execute a command using Scrapybara as the back-end.

    If a URL is provided, the browser is opened with the specified URL before
    executing the command, reducing the time spent on manual browser operations.

    Args:
        cmd: The command or instruction for the agent to execute.
        url: An optional URL to open in the browser before launching the agent.
        tools: An optional collection of tools for the agent to use. Defaults to a set of basic tools.
        instance_type: The type of instance to start, can be "small", "medium", or "large". Defaults to "small".
        verbose: If True, enables detailed logging of the agent's progress.

    Returns:
        list[dict]: The result of the agent's execution.
    """

    setup_logging(verbose)
    instance = scrapybara.start(instance_type=instance_type)
    logger.info(f"Started Scrapybara instance: {instance_type}")
    stream_url = instance.get_stream_url().stream_url
    logger.info(f"VNC stream URL: {stream_url}")

    try:
        if url:
            open_url(instance, url)
            logger.info(f"Opened URL in browser: {url}")

        if tools is None:
            tools = ToolCollection(
                ComputerTool(instance), BashTool(instance), EditTool(instance)
            )
        result = run_agent(launch_prompt(), cmd, instance, tools, verbose=verbose)
    finally:
        instance.stop()
        logger.info("Stopped Scrapybara instance")
    return result


def scrape(
    query: T,
    url: Optional[str] = None,
    cmd: Optional[str] = None,
    tools: Optional[ToolCollection] = None,
    instance_type: Optional[Literal["small", "medium", "large"]] = "small",
    verbose: bool = False,
) -> T:  # type: ignore temporary
    """Retrieve information using an agent with a defined query structure.

    This function uses a Pydantic model to define the query and response structure,
    allowing the agent to perform complex information retrieval tasks.

    Args:
        query: A Pydantic model instance defining the query structure and expected response fields.
        url: An optional URL to open in the browser before launching the agent.
        cmd: An optional command that overrides the query model's docstring.
        tools: An optional collection of tools for the agent to use. Defaults to a set of basic tools.
        instance_type: The type of instance to start, can be "small", "medium", or "large". Defaults to "small".
        verbose: If True, enables detailed logging of the agent's progress.

    Returns:
        T: An instance of the provided Pydantic model containing the retrieved information.
    """
    setup_logging(verbose)
    instance = scrapybara.start(instance_type=instance_type)
    logger.info(f"Started Scrapybara instance: {instance_type}")
    stream_url = instance.get_stream_url().stream_url
    logger.info(f"VNC stream URL: {stream_url}")

    try:
        if url:
            open_url(instance, url)
            logger.info(f"Opened URL in browser: {url}")

        schema, cmd = scrape_query_to_prompt(query, cmd)

        if tools is None:
            tools = ToolCollection(
                ComputerTool(instance), BashTool(instance), EditTool(instance)
            )
        messages = run_agent(
            scrape_prompt(schema), cmd, instance, tools, verbose=verbose
        )
    finally:
        instance.stop()
        logger.info("Stopped Scrapybara instance")

    try:
        logger.info(
            f"Extracting JSON from last message: {messages[-1]['content'][-1]['text']}"
        )
        return query.model_validate(extract_json(messages[-1]["content"][-1]["text"]))
    except ValidationError as e:
        # TODO potentially handle re-request
        raise e
