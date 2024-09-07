import json
from pathlib import Path


def get_african_countries():

    path = Path.cwd() / "config.json"
    countries_json = path.read_text()
    countries_dict = json.loads(countries_json)

    return countries_dict["countries"]
