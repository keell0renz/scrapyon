from typing import Literal, Optional, TypedDict, Any
from anthropic.types.beta import (
    BetaToolComputerUse20241022Param,
    BetaToolTextEditor20241022Param,
    BetaToolBash20241022Param,
)
from scrapybara.client import Instance
from scrapybara.anthropic.base import ToolResult, ToolError, CLIResult
from scrapyon._logging import logger
from .base import BaseTool


class ComputerToolOptions(TypedDict):
    display_height_px: int
    display_width_px: int
    display_number: Optional[int]


class ToolCollection:
    def __init__(self, *tools):
        self.tools = tools
        self.tool_map = {tool.to_params()["name"]: tool for tool in tools}

    def set_instance(self, instance: Instance):
        self.instance = instance

    def to_params(self) -> list:
        return [tool.to_params() for tool in self.tools]

    def run(self, *, name: str, tool_input: dict) -> Optional[ToolResult]:
        tool = self.tool_map.get(name)
        if not tool:
            return None
        try:
            if not self.instance:
                raise ValueError("Instance not set!")
            return tool.call(tool_input, self.instance)
        except Exception as e:
            logger.error(f"Error running tool {name}: {e}")
            return None


class ComputerTool(BaseTool):
    """A computer interaction tool that allows the agent to control mouse and keyboard."""

    api_type: Literal["computer_20241022"] = "computer_20241022"
    name: Literal["computer"] = "computer"
    width: int = 1024
    height: int = 768
    display_num: Optional[int] = 1

    def __init__(self):
        super().__init__()

    @property
    def options(self) -> ComputerToolOptions:
        return {
            "display_width_px": self.width,
            "display_height_px": self.height,
            "display_number": self.display_num,
        }

    def to_params(self) -> BetaToolComputerUse20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
            "display_width_px": self.width,
            "display_height_px": self.height,
            "display_number": self.display_num,
        }

    def call(self, kwargs: dict, instance: Instance) -> ToolResult:
        action = kwargs.pop("action")
        coordinate = kwargs.pop("coordinate", None)
        text = kwargs.pop("text", None)

        try:
            result = instance.computer(
                action=action,
                coordinate=tuple(coordinate) if coordinate else None,
                text=text,
            )
            return CLIResult(
                output=result.get("output") if result else "",
                error=result.get("error") if result else None,
                base64_image=result.get("base64_image") if result else None,
                system=result.get("system") if result else None,
            )
        except Exception as e:
            raise ToolError(str(e)) from None


class EditTool(BaseTool):
    """A filesystem editor tool that allows the agent to view, create, and edit files."""

    api_type: Literal["text_editor_20241022"] = "text_editor_20241022"
    name: Literal["str_replace_editor"] = "str_replace_editor"

    def __init__(self):
        super().__init__()

    def to_params(self) -> BetaToolTextEditor20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
        }

    def call(self, kwargs: dict, instance: Instance) -> ToolResult:
        command = kwargs.pop("command")
        path = kwargs.pop("path")
        file_text = kwargs.pop("file_text", None)
        view_range = kwargs.pop("view_range", None)
        old_str = kwargs.pop("old_str", None)
        new_str = kwargs.pop("new_str", None)
        insert_line = kwargs.pop("insert_line", None)

        try:
            result = instance.edit(
                command=command,
                path=path,
                file_text=file_text,
                view_range=view_range,
                old_str=old_str,
                new_str=new_str,
                insert_line=insert_line,
            )
            return CLIResult(
                output=result.get("output") if result else "",
                error=result.get("error") if result else None,
                base64_image=result.get("base64_image") if result else None,
                system=result.get("system") if result else None,
            )
        except Exception as e:
            raise ToolError(str(e)) from None


class BashTool(BaseTool):
    """A shell execution tool that allows the agent to run bash commands."""

    api_type: Literal["bash_20241022"] = "bash_20241022"
    name: Literal["bash"] = "bash"

    def __init__(self):
        super().__init__()

    def to_params(self) -> BetaToolBash20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
        }

    def call(self, kwargs: dict, instance: Instance) -> ToolResult:
        command = kwargs.pop("command")
        restart = kwargs.pop("restart", False)

        try:
            result = instance.bash(command=command, restart=restart)
            return CLIResult(
                output=result.get("output") if result else "",
                error=result.get("error") if result else None,
                base64_image=result.get("base64_image") if result else None,
                system=result.get("system") if result else None,
            )
        except Exception as e:
            raise ToolError(str(e)) from None
