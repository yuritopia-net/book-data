#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

import argparse
import datetime
import os
import re
import sys
import uuid

import isbnlib
import yaml


# http://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order
def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.add_representer(OrderedDict, represent_ordereddict)

# http://stackoverflow.com/questions/38369833/
def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

yaml.add_representer(str, quoted_presenter)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r"))

    args = parser.parse_args()

    temp = []
    for item in yaml.load(args.input):
        store = OrderedDict([
            ("id", item["id"]),
            ("title", item["title"]["name"]),
            ("links", []),
        ])
        for identifier in item["identifier"]:
            if identifier["domain"] != "isbn":
                continue
            store["links"].append({
                "domain": "amazon.co.jp",
                "url": "https://www.amazon.co.jp/dp/{}".format(isbnlib.to_isbn10(identifier["id"])),
                "id": isbnlib.to_isbn10(identifier["id"]),
            })
            store["links"].append({
                "domain": "kindle.amazon.co.jp",
                "url": "https://www.amazon.co.jp/dp/",
                "id": "",
            })
        temp.append(store)

    print(yaml.dump(temp, allow_unicode=True, default_flow_style=False, indent=1))

    return 0


if __name__ == "__main__":
    sys.exit(main())
