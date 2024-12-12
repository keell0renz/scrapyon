# ScrapyOn: Claude computer use with Scrapybara

Important: Not yet tested! It is a prototype and concept. You better run it in jupyter notebook for now.

ScrapyOn is a convenient wrapper which makes easy to run computer use agents with Scrapybara as a back-end.

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

Also, you can try to use it as an intelligent information retriever, for retrieving info which requires some agentic behavior.

```python
from pydantic import BaseModel
import scrapyon

class Query(BaseModel):
    """Please find out who is Deitz Nuutsen and estimate how true it is (1 to 10)"""

    response: str
    how_true: int

result: Query = scrapyon.scrape(
    query=Query,
    url="https://google.com",
    cmd="Command here overwrites Query docstring command.",
    instance_type="small",
    verbose=True  # Set to True to see detailed progress
)

print(result.response)
print(result.how_true)
```

## Parameters

Both `launch()` and `scrape()` functions accept these common parameters:

- `url`: Optional URL to open in browser before launching the agent
- `instance_type`: Size of the instance ("small", "medium", or "large"). Defaults to "small"
- `verbose`: If True, prints detailed progress information including assistant responses and tool usage. Defaults to False
