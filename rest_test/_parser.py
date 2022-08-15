import asyncio
import yaml
import os

from .checkers import Checker, JSONChecker


class YAMLParser:
    def __init__(self, yaml_file: str):
        if not (os.path.isfile(yaml_file) or os.path.isdir(yaml_file)):
            print(f"{yaml_file} not found!")
            exit()

        if os.path.isdir(yaml_file):
            files = map(lambda yaml: f"{yaml_file}/{yaml}", os.listdir(yaml_file))
        else:
            files = (yaml_file,)

        self.checkers = list(map(self.parsef, files))

    def parsef(self, yaml_file_name: str) -> Checker:
        with open(yaml_file_name) as file:
            _yaml = yaml.safe_load(file)
       
        name = _yaml["name"]

        _url = _yaml["url"]
        _response = _yaml["response"]
        
        _format = _yaml["format"] if "" in _yaml else "json"
        _method = _yaml["method"] if "" in _yaml else "get"
        _fullmatch = _yaml["fullmatch"] if "fullmatch" in _yaml else False
        _data = _yaml["data"] if "data" in _yaml else None
        _json_data = _yaml["json_data"] if "json_data" in _yaml else None
        
        if _format == "json":
            return JSONChecker(name, _url, _method,  _response, _data, 
                               _json_data, _fullmatch)
    
    def run_checkers(self):
        return asyncio.run(self._run_checkers())

    async def _run_checkers(self):
        return list(map(str, await asyncio.gather(*[ch.check() for ch in self.checkers])))
