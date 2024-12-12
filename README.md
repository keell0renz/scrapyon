# ScrapyOn: Claude computer use with Scrapybara

ScrapyOn is a convenient wrapper which makes easy to run computer use agents with Scrapybara as a back-end.

```python
import scrapyon

result = scrapyon.launch(
    cmd="Please find who is Deitz Nuutsen",
    url="https://google.com"
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
    url="https://google.com"
)

print(result.response)
print(result.how_true)
```
