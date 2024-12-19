from scrapybara.anthropic.base import BaseAnthropicTool
from typing import Any


class BaseTool(BaseAnthropicTool):
    """Base class for all Scrapyon tools that implements common functionality."""

    def __call__(self, **kwargs: Any) -> None:
        pass
