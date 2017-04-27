#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

import argparse
import datetime
import os
import re
import sys
import uuid

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


def kata2hira(text):
    return re.sub(r"[ァ-ヴ]", lambda x: chr(ord(x.group(0))-0x60), text)

def normalize_space(text):
    return "".join(text.split())

def normalize(text):
    return normalize_space(kata2hira(text))


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

    now = datetime.datetime.now()

    temp = OrderedDict()
    temp["id"] = str(uuid.uuid4())
    temp["title"] = OrderedDict([
        ("name", data["title"][0]["value"]),
        ("kana", normalize(data["title"][0]["transcription"])),
    ])
    temp["creator"] = []
    for creator in data["creator"]:
        temp["creator"].append(OrderedDict([
            ("id", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"),
            ("name", creator["name"]),
            ("kana", normalize(creator["transcription"])),
        ]))
    temp["identifier"] = [
        {
            "domain": "iss.ndl.go.jp",
            "id": id,
        },
        {
            "domain": "isbn",
            "id": data["identifier"]["ISBN"][0].replace("-", "")
        }
    ]
    temp["publish"] = {}
    if "volume" in data:
        temp["publish"]["volume"] = data["volume"][0]
    if "seriesTitle" in data:
        temp["publish"]["publisher"] = data["seriesTitle"][0]["value"].split(";")[0].strip()
    if "date" in data:
        temp["publish"]["issued"] = data["date"][0].replace(".", "-")
    if "extent" in data:
        temp["publish"]["page"] = data["extent"][0].split("p")[0].strip()
    if "price" in data:
        temp["price"] = [
            {
                "n": data["price"],
                "country": "jp",
                "last_visit": now.strftime("%Y-%m-%d"),
                "source": "iss.ndl.go.jp",
            }
        ]
    temp["last_update"] = now.strftime("%Y-%m-%d")

    print(yaml.dump([temp], allow_unicode=True, default_flow_style=False, indent=1, default_style='"'))

    return 0


if __name__ == "__main__":
    sys.exit(main())
