# ELK Note

## Deploy ELK by Docker-Compose

```
cd deploy
docker-compose up -d
```
result
```
λ docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                                            NAMES
fe3b53893579        logstash:7.9.2        "/usr/local/bin/dock…"   47 hours ago        Up 24 hours         5044/tcp, 0.0.0.0:5000->5000/tcp, 9600/tcp       elk-note_logstash_1
5c5802465864        kibana:7.9.2          "/usr/local/bin/dumb…"   47 hours ago        Up 24 hours         0.0.0.0:5601->5601/tcp                           elk-note_kibana_1
7e5e9fe9c111        elasticsearch:7.9.2   "/tini -- /usr/local…"   47 hours ago        Up 24 hours         0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   elk-note_elasticsearch_1
```