from elasticsearch import Elasticsearch

"""
# curl localhost:9200/my_index/my_type/s_X2S3cB1BlXf_Yvwfj1
# res = es.search(index="my_index",doc_type="my_type")
# res = es.index(index="my_index", doc_type="my_type", body={"key1": "Hello123."})
# res = es.get(index="my_index",doc_type="my_type",  id ="s_X2S3cB1BlXf_Yvwfj1")
# res = es.delete(index="my_index",doc_type="my_type", id ="s_X2S3cB1BlXf_Yvwfj1")
# res = es.update(index="my_index", doc_type="my_type", id='s_X2S3cB1BlXf_Yvwfj1', body={"doc": {"key1": "Hello456."}})
"""


def load_datas():
    datas = list()
    with open('elasticsearch/student.csv', 'r',encoding="utf-8") as f:
        for data in f.readlines():
            sid, name, age, class_ = data.replace('\n', '').split(',')
            datas.append(
                {
                    "sid": sid,
                    "name": name,
                    "age": int(age),
                    "class": class_
                }
            )
    return datas


def create_data(es, datas):
    for data in datas:
        es.index(index='school',   body=data)  

def search_all_docs():
    print("***"*100)
    res = es.search(index="school",  body={"query": {"match_all": {}}})
    print(res)


def search_by_text(key, value):
    print("***"*100)
    res = es.search(index="school",  body={"query": {"match": {key: value}}})
    print(res)


def search_by_keyword(key, value):
    print("***"*100)
    res = es.search(index="school",  body={"query": {"match": {key: value}}})
    print(res)
    

def delet_record(es, id):
    es.delete(index='school',  id=id)   
    

def update_record(es, id):
    body = {
        "doc": {
            "name": "張正男"
        }
    }
    es.update(index='school',  id=id, body=body)   
    

def create_index(es):
    body = dict()
    body['settings'] = get_setting()
    body['mappings'] = get_mappings()
    print(body)
    es.indices.create(index="school", body=body)


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
                "type": "text"
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


def delete_index(es):
    es.indices.delete(index='school', ignore=[400, 404])


if __name__ == "__main__":
    es = Elasticsearch(host="localhost", port=9200)
    # delete_index(es)
    # create_index(es)
    # datas = load_datas()
    # create_data(es, datas)
    search_all_docs()
    search_by_text("name", "王")
    search_by_keyword("class", "資工A班")
    # delet_record(es, "4QFkNnUBbpMOu06EawYp")
    # update_record(es, "3wFkNnUBbpMOu06EawYC")
    