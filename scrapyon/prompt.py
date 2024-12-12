import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

env = Environment(loader=FileSystemLoader("templates"))


def launch_prompt() -> str:
    template = env.get_template("launch.jinja")
    return template.render(time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def scrape_prompt(json_schema: dict) -> str:
    template = env.get_template("scrape.jinja")
    return template.render(
        time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        json_schema=json.dumps(json_schema),
    )
