#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
import aiohttp
import asyncio

from typing import Union

from ._results import RestError, RestPassed


class Checker(abc.ABC):
    def __init__(self, name, url: str, _method: str, _resp, _data = None, 
                _json_data = None, fullmatch: bool = False):
        self.name = name

        self.url = url
        self._method = _method
        
        self._json_data = _json_data
        self._data = _data
        self._resp = _resp
        self._fullmatch = fullmatch

    async def check(self) -> Union[RestPassed, RestError]:
        async with aiohttp.ClientSession() as session:
            if self._method == "post":
                req = session.post(self.url, data=self._data, json=self._json_data)
            else:
                req = session.get(self.url, data=self._data, json=self._json_data)
            async with req as response:
                return await self._check(response)
    
    def __str__(self):
        return f"{self.__class__}(url: {self.url})"

    @abc.abstractmethod
    def _check_sync(self) -> Union[RestPassed, RestError]:
        pass

    @abc.abstractmethod
    async def _check(self, response) -> Union[RestPassed, RestError]:
        pass


class JSONChecker(Checker):
    async def _check(self, response: aiohttp.ClientResponse) -> Union[RestPassed, RestError]:
        resp = await response.json()
        
        if self._fullmatch:
            return RestPassed(self, resp) if self._resp == resp else RestError(self, resp)
        
        if isinstance(self._resp, dict):
            for key, val in self._resp.items():
                if key not in resp or val != resp[key]:
                    return RestError(self, resp)

        elif isinstance(self._resp, list):
            for val in self._resp:
                if val not in resp:
                    return RestError(self, resp)

        return RestPassed(self, resp)

    def _check_sync(self) -> Union[RestPassed, RestError]:
        return None


if __name__ == "__main__":
    ch = JSONChecker("http://127.0.0.1:8000", "get", True, data=None, json=None)
    print(asyncio.run(ch.check()))
