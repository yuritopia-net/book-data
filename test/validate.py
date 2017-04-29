#!/usr/bin/env python

import argparse
import os
import sys
import traceback
import json

from cerberus import Validator
import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=argparse.FileType("r"))
    parser.add_argument("input", type=argparse.FileType("r"))

    args = parser.parse_args()

    schema = yaml.load(args.schema)

    try:
        data = yaml.load(args.input)
    except yaml.parser.ParserError:
        print("parse erorr:")
        print(traceback.format_exc())
        return 1

    assert isinstance(data, list)
    index_map = dict((i, x["id"]) for i, x in enumerate(data))

    validator = Validator({"#root": schema})

    if not validator.validate({"#root": data}):
        print(validator.errors)
        print("-"*80)
        for item in validator.errors["#root"]:
            for key in item.keys():
                print("#{}:".format(key), index_map[key])
        print("error!")
        return 1

    print("passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
