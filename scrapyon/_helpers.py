from anthropic.types.beta import BetaToolResultBlockParam
from scrapybara.anthropic.base import ToolResult
from scrapybara.client import Instance
from playwright.sync_api import sync_playwright
import json
import re


def extract_json(text: str) -> dict:
    """Extract a valid JSON object from text, ignoring any surrounding content."""
    # Find text that looks like a JSON object (between curly braces)
    json_match = re.search(r"{.*}", text, re.DOTALL)
    if not json_match:
        raise ValueError(f"No JSON object found in text: {text}")

    try:
        # Parse the matched text as JSON
        return json.loads(json_match.group(0))
    except json.JSONDecodeError:
        raise ValueError(
            f"Found text between curly braces, but it's not valid JSON: {text}"
        )


def open_url(instance: Instance, url: str):
    try:
        cdp_url = instance.browser.start().cdp_url
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(cdp_url)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state("load")
    except:
        pass


def make_tool_result(result: ToolResult, tool_use_id: str) -> BetaToolResultBlockParam:
    tool_result_content = []
    is_error = False

    if result.error:
        is_error = True
        tool_result_content = result.error
    else:
        if result.output:
            tool_result_content.append(
                {
                    "type": "text",
                    "text": result.output,
                }
            )
        if result.base64_image:
            tool_result_content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": result.base64_image,
                    },
                }
            )

    return {
        "type": "tool_result",
        "content": tool_result_content,
        "tool_use_id": tool_use_id,
        "is_error": is_error,
    }
