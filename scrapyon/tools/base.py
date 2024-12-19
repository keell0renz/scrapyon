from typing import Optional
from scrapybara.client import Instance
from scrapybara.anthropic.base import BaseAnthropicTool


class BaseTool(BaseAnthropicTool):
    """Base class for all Scrapyon tools that implements common functionality."""

    def __init__(self):
        super().__init__()
