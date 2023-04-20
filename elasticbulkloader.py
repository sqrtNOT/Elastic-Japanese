#!/usr/bin/python3
import os
from elasticsearch import helpers, Elasticsearch


def parsecc100(path):
    dataset = open(path, "r")
    doc = ""
    while True:
        line = dataset.readline()
        if line == "":
            return doc
        if line == "\n":
            yield doc
            doc = ""
        else:
            doc = doc + line


def chunkparsecc100(path, chunksize):
    dataset = parsecc100(path)
    chunk = ""  # for limiting the size of the payload
    actions = []  # return object
    id = 0
    for doc in dataset:
        id = id + 1
        rownum = 0
        for sentence in doc.split("\n"):
            rownum = rownum + 1
            source = {"document_id": id, "sentence_id": rownum, "sentence": sentence}
            action = {"_index": "jpnsearch", "_source": source}
            actions.append(action)
        chunk += doc
        if chunk.__sizeof__() >= chunksize:
            yield actions
            actions = []
            chunk = ""


client = Elasticsearch(f"http://{os.environ.get('ELASTIC_PASS')}@localhost:9250")

MiB = 64
data = chunkparsecc100("/datasets/cc-100/ja.txt", MiB * 1024**2)
i = 0
for actions in data:
    i = i + 1
    helpers.bulk(client, actions)
    print(f"{i*MiB}MiB loaded")
