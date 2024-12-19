from typing import Optional
from scrapybara.client import Instance
from scrapybara.anthropic.base import BaseAnthropicTool


class BaseTool(BaseAnthropicTool):
    """Base class for all Scrapyon tools that implements common functionality."""

    instance: Optional[Instance] = None

    def __init__(self):
        self.instance: Optional[Instance] = None
        super().__init__()

    def set_instance(self, instance: Instance):
        """Set the Scrapybara instance for this tool."""
        self.instance = instance 