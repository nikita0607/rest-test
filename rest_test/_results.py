#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RestError(Exception):
    def __init__(self, check: "Checker", server_response):
        self.message = "Test {check.name} is wrong!"
        
        self.checker = check
        self.server_response = server_response
        self.test_response = check._resp

    def __str__(self):
        return f"RestError(name: {self.checker.name}, " \
               f"test_response: {self.test_response}, " \
               f"response: {self.server_response})"


class RestPassed:
    def __init__(self, check: "Checker", server_response):
        self.checker = check
        self.server_response = server_response
        self.test_response = check._resp

    def __str__(self):
        return f"RestPassed(name: {self.checker.name}, " \
               f"test_response: {self.test_response}, " \
               f"response: {self.server_response})"
