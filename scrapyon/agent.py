from scrapybara.anthropic import BashTool, ComputerTool, EditTool
from scrapyon.helpers import ToolCollection, make_tool_result
from scrapybara.client import Instance
from anthropic import Anthropic


async def run_agent(
    system_prompt: str, 
    user_prompt: str, 
    instance: Instance,
    verbose: bool = False
) -> str:

    tools = ToolCollection(
        ComputerTool(instance), BashTool(instance), EditTool(instance)
    )

    anthropic = Anthropic()

    messages = []
    messages.append(
        {"role": "user", "content": [{"type": "text", "text": user_prompt}]}
    )

    while True:
        # Get Claude's response
        response = anthropic.beta.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=messages,
            system=[{"type": "text", "text": system_prompt}],
            tools=tools.to_params(),
            betas=["computer-use-2024-10-22"],
        )

        # Process tool usage
        tool_results = []
        for content in response.content:
            if content.type == "text":
                if verbose:
                    print(f"Assistant: {content.text}")
            elif content.type == "tool_use":
                if verbose:
                    print(f"Running tool: {content.name}")
                    print(f"Tool input: {content.input}")
                
                result = await tools.run(name=content.name, tool_input=content.input)  # type: ignore

                if result:
                    if verbose and result.output:
                        print(f"Tool output: {result.output}")
                    tool_result = make_tool_result(result, content.id)
                    tool_results.append(tool_result)

        # Add assistant's response and tool results to messages
        messages.append(
            {"role": "assistant", "content": [c.model_dump() for c in response.content]}
        )

        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    text = ""
    last_message = messages[-1]
    if last_message["role"] == "assistant":
        for content in last_message["content"]:
            if content["type"] == "text":
                text = content["text"]

    return text
