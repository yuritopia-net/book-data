#!/usr/bin/env python3

from collections import OrderedDict

import argparse
import datetime
import os
import sys
import uuid

import requests
import yaml


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

    temp = {}#OrderedDict()
    temp["id"] = str(uuid.uuid4())
    temp["title"] = {
        "name": data["title"][0]["value"],
        "kana": data["title"][0]["transcription"],
    }
    temp["creator"] = []
    for creator in data["creator"]:
        temp["creator"].append({
            "id": "",
            "name": creator["name"],
            "kana": creator["transcription"],
        })
    temp["identifier"] = [
        {
            "domain": "iss.ndl.go.jp",
            "id": id,
        },
        {
            "domain": "isbn",
            "id": data["identifier"]["ISBN"][0]
        }
    ]
    temp["publish"] = {}
    if "volume" in data:
        temp["publish"]["volume"] = data["volume"][0]
    if "seriesTitle" in data:
        temp["publish"]["publisher"] = data["seriesTitle"][0]["value"]
    if "date" in data:
        temp["publish"]["issued"] = data["date"][0]
    if "extent" in data:
        temp["publish"]["page"] = data["extent"][0]
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

    print(yaml.dump([temp], allow_unicode=True, default_flow_style=False, indent=1))

    return 0


if __name__ == "__main__":
    sys.exit(main())
