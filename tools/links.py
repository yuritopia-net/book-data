#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

import argparse
import datetime
import os
import re
import readline
import sys
import uuid

from lxml import html
import requests
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


def test_encoding(text):
    try:
        test = text.encode("iso-8859-1")
        return test.decode("iso-8859-1") == text
    except:
        return False

def force_decode(text):
    for encoding in ["iso-2022-jp", "euc-jp", "cp932", "utf-8"]:
        try:
            return text.encode("iso-8859-1").decode(encoding)
        except:
            continue
    return None

def ndl2name(text, kana):
    texts = list(map(lambda x: x.strip(), text.split(",")))
    kanas = list(map(lambda x: x.strip(), kana.split(",")))
    return [{
        "type": "full",
        "text": "".join(texts[:2]),
        "kana": "".join(kanas[:2]),
    }, {
        "type": "last",
        "text": texts[0],
        "kana": kanas[0],
    }, {
        "type": "first",
        "text": texts[1],
        "kana": kanas[1] if len(kanas) > 1 else "",
    }]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")

    args = parser.parse_args()

    links = []
    for url in args.urls:
        resp = requests.get(url)
        if resp.status_code != 200:
            continue
        data = resp.text
        try:
            dom = html.fromstring(data)
            elems = dom.xpath("//title/text()")
            title = str(elems[0])
            if test_encoding(title):
                title = force_decode(title)
            links.append({
                "url": url,
                "title": title,
                "last_visit": datetime.datetime.now().strftime("%Y-%m-%d"),
                "state": "active",
            })
        except:
            links.append({
                "url": url,
                "title": "",
                "last_visit": datetime.datetime.now().strftime("%Y-%m-%d"),
                "state": "active",
            })

    print(yaml.dump([{"dummy": None, "links": links}], allow_unicode=True, default_flow_style=False, indent=1, default_style='"'))

    return 0


if __name__ == "__main__":
    sys.exit(main())
