from anthropic.types.beta import BetaToolResultBlockParam
from scrapybara.anthropic.base import ToolResult
from scrapybara.client import Instance
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio

async def open_url_async(instance: Instance, url: str):
    cdp_url = instance.browser.start().cdp_url
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_url)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state("load")

def open_url(instance: Instance, url: str):
    cdp_url = instance.browser.start().cdp_url
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp_url)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("load")

# Helper function to automatically choose the right version
def open_url_auto(instance: Instance, url: str):
    try:
        # Check if we're in an async context
        loop = asyncio.get_running_loop()
        # We're in an async context, use the async version
        loop.create_task(open_url_async(instance, url))
    except RuntimeError:
        # We're not in an async context, use the sync version
        open_url(instance, url)


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
