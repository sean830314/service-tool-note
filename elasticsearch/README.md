1. Create record

```
POST /accounts/_doc/1
{
  "name": "james",
  "lastname": "lee"
}

```
result
```
{
  "_index" : "accounts",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 0,
  "_primary_term" : 1
}
```

2. Get record

```
GET /accounts/_doc/1
```
result
```
{
  "_index" : "accounts",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 1,
  "_seq_no" : 0,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "name" : "james",
    "lastname" : "lee"
  }
}
```
```
GET /accounts/_search?pretty=true
```
result
```
{
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "accounts",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "name" : "james",
          "lastname" : "lee"
        }
      }
    ]
  }
}
```

3. Update record

```
POST /accounts/_update/1
{
"doc":{
  "lastname":"li"
  }
}
```
result
```
{
  "_index" : "accounts",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 4,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 3,
  "_primary_term" : 1
}

```

4. Delete account

```
DELETE /accounts
```

result
```
{
  "_index" : "accounts",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 4,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 3,
  "_primary_term" : 1
}

```