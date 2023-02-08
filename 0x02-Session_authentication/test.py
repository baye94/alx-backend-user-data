#!/usr/bin/env python3

import requests


def print_characters(index, arr):
    """Print all the characters from the api"""
    if index == len(arr):
        return
    res = requests.get(arr[index])
    print(res.json().get('name'))
    print_characters(index + 1, arr)

res = requests.get('https://swapi-api.hbtn.io/api/films/3')
arr = res.json().get('characters')
print_characters(0, arr)
