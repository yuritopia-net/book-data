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
    parser.add_argument("--input", type=argparse.FileType("r"), default=os.path.join(BASE_PATH, "data/authors.yml"))

    args = parser.parse_args()

    for item in yaml.load(args.input):
        test = ",".join([x["text"] for x in item["name"] if x["type"] == "full"])
        for word in args.search:
            if word in test:
                print("id:"+item["id"])
                print("\tname:", test)
                break

    return 0


if __name__ == "__main__":
    sys.exit(main())
