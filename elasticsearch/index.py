from elasticsearch import Elasticsearch
import json


def create_index(es):
    body = dict()
    body['settings'] = get_setting()
    body['mappings'] = get_mappings()
    es.indices.create(index='school_members', body=body)


def get_setting():
    settings = {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 2
        }
    }

    return settings


def get_mappings():
    mappings = {
        "properties": {
            "sid": {
                "type": "integer"
            },
            "name": {
                "type": "text"
            },
            "age": {
                "type": "integer"
            },
            "class": {
                "type": "keyword"
            }
        }
    }

    return mappings

def change_mappings(es):
    body = get_teacher_mappings()
    es.indices.put_mapping(index='school_members', body=body)

def get_teacher_mappings():
    mappings = {
        "properties": {
            "tid": {
                "type": "integer"
            },
            "name": {
                "type": "text"
            },
            "age": {
                "type": "integer"
            },
            "class": {
                "type": "keyword"
            },
            "salary": {
                "type": "integer"
            }
        }
    }
    return mappings


if __name__ == "__main__":
    es = Elasticsearch(host="localhost", port=9200)
    result = es.indices.exists(index='school_members')
    if not result:
        print("create index")
        create_index(es)
    result = es.indices.get(index='school_members')
    print(result)
    # print("***"*100)
    # print("change mappings")
    # change_mappings(es)
    # result = es.indices.get(index='school_members')
    # print(result)
    # print("***"*100)
    # print("alias")
    # es.indices.put_alias(index='school_members', name='school')
    # result = es.indices.get(index='school')
    # print(result)
    # print("***"*100)
    # print("delete alias")
    # es.indices.delete_alias(index='school_members', name='school') 
    # result = es.indices.get(index='school')
    # print(result)