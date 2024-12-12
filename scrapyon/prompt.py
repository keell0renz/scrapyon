import json
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pydantic import BaseModel
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "prompts"
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def launch_prompt() -> str:
    template = env.get_template("launch.jinja")
    return template.render(time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def scrape_prompt(json_schema: dict) -> str:
    template = env.get_template("scrape.jinja")
    return template.render(
        time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        json_schema=json.dumps(json_schema),
    )


def scrape_to_prompt(model: BaseModel, cmd: Optional[str] = None) -> tuple[dict, str]:
    schema = model.model_json_schema()
    cmd = model.__doc__ if cmd is None else cmd
    cmd = (
        cmd
        if cmd
        else """Instructions not specified. 
        In that case just scrape the information from the page you see opened, do not do any complex stuff.
        """
    )
    return schema, cmd
