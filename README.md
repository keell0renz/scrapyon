# ScrapyOn: Claude computer use with Scrapybara

ScrapyOn is a convenient wrapper which makes easy to run computer use agents with Scrapybara as a back-end.

## Basic Usage

```python
import scrapyon

result = scrapyon.launch(
    cmd="Please find who is Deitz Nuutsen",
    url="https://google.com",
    instance_type="small",
    verbose=True  # Set to True to see detailed progress
)
```

When you specify `url`, before it launches an agent it programmatically starts the browser with the url specified, so agent spends less time opening browser and typing manually.

## Structured Data Retrieval

You can use ScrapyOn for intelligent information retrieval with structured output using Pydantic models:

```python
from pydantic import BaseModel, Field
import scrapyon

class SearchQuery(BaseModel):
    """Search for information about a person and analyze the results"""

    response: str = Field(description="Detailed natural language response about findings")
    source: str = Field(description="Source URL or website where information was found")
    confidence_score: int = Field(
        description="Confidence score from 1-10 about the reliability of information",
        ge=1,
        le=10
    )
    is_notable: bool = Field(description="Whether the person has significant online presence")

# Execute the search
result: SearchQuery = scrapyon.scrape(
    query=SearchQuery,
    url="https://google.com",
    cmd="Find information about Marie Curie",
    instance_type="small",
    verbose=True
)

print(f"Response: {result.response}")
print(f"Source: {result.source}")
print(f"Confidence: {result.confidence_score}/10")
print(f"Notable Person: {result.is_notable}")
```

## Parameters

Both `launch()` and `scrape()` functions accept these common parameters:

- `cmd`: The command or instruction for the agent to execute
- `url`: Optional URL to open in browser before launching the agent
- `tools`: Optional collection of custom tools for the agent (defaults to ComputerTool, BashTool, and EditTool)
- `instance_type`: Size of the instance ("small", "medium", or "large"). Defaults to "small"
- `verbose`: If True, prints detailed progress information including assistant responses and tool usage. Defaults to False

### Additional Parameters for `scrape()`

The `scrape()` function has some specific parameters:

- `query`: A Pydantic model class that defines the structure of the expected response
- `cmd`: Optional command that overrides the query model's docstring command

## Custom Tools

You can create and use custom tools with ScrapyOn by using prebuilt tools or by extending `BaseAnthropicTool`:

```python
from scrapyon.tools import ToolCollection, BaseAnthropicTool, CLIResult, ToolError, Instance
from typing import Literal, Optional

class CustomTool(BaseAnthropicTool):
    api_type: Literal["custom_type"] = "custom_type"
    name: Literal["custom_tool"] = "custom_tool"

    def __init__(self):
        self.instance = None
        super().__init__()

    def set_instance(self, instance: Instance):
        self.instance = instance

    def to_params(self) -> dict:
        return {
            "name": self.name,
            "type": self.api_type,
        }

    def __call__(self, **kwargs) -> CLIResult:
        try:
            # Implement your custom logic here
            result = {"output": "Custom tool execution"}
            return CLIResult(
                output=result.get("output"),
                error=None,
                base64_image=None,
                system=None
            )
        except Exception as e:
            raise ToolError(str(e)) from None

# Use custom tools with launch() or scrape()
tools = ToolCollection(CustomTool())

result = scrapyon.launch(
    cmd="Execute task with custom tool",
    tools=tools,
    verbose=True
)
```

Custom tools must implement:

- `api_type`: Literal type identifier for the tool
- `name`: Literal name identifier for the tool
- `set_instance()`: Method to set the Scrapybara instance
- `to_params()`: Method that returns the tool's parameters
- `__call__()`: Method that implements the tool's functionality, returning a `CLIResult`

The default tools provided are:

- `ComputerTool`: For browser and computer interaction (mouse/keyboard control)
- `BashTool`: For executing shell commands
- `EditTool`: For file system operations (view/create/edit files)

Each tool returns a `CLIResult` containing:

- `output`: Command output string
- `error`: Error message if any
- `base64_image`: Base64 encoded image if applicable
- `system`: System information if applicable
