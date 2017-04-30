#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import yaml


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search", nargs="+")
    parser.add_argument("--input", type=argparse.FileType("r"), default=os.path.join(BASE_PATH, "data/books.yml"))

    args = parser.parse_args()

    for item in yaml.load(args.input):
        for word in args.search:
            if word in item["title"]["name"]:
                print("id:"+item["id"])
                print("\ttitle:", item["title"]["name"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
