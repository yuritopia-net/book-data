#!/usr/bin/env python3

from collections import OrderedDict

import argparse
import json
import os
import sys

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("id")

    args = parser.parse_args()

    id = args.id
    if id.startswith("http://iss.ndl.go.jp/books/"):
        id = id[len("http://iss.ndl.go.jp/books/"):]

    resp = requests.get(
        "http://iss.ndl.go.jp/books/{}.json".format(id),
        headers={
            "User-Agent": "lilybot +http://www.yuritopia.net/policy/bot.html",
        }
    )

    if resp.status_code == 404:
        print("Not found:", args.id)
        return 1

    data = resp.json()

    print(json.dumps(data, indent=1, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
