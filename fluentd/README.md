# Fluentd

Fluentd is an open-source data collector for a unified logging layer. Fluentd allows you to unify data collection and consumption for better use and understanding of data.
##  Key features
* Unified Logging with JSON
* Pluggable Architecture
* Minimum Resources Required
* Built-in Reliability
## Fluentd has eight types of plugins:
* [Input](https://docs.fluentd.org/input)
* [Parser](https://docs.fluentd.org/output)
* [Filter](https://docs.fluentd.org/filter)
    ```
    <source> 
      @type http
      port 9880 
    </source> 
    <filter myapp.access> 
      @type   record_transformer 
      <record> 
        host_param "#{Socket.gethostname}" 
      </record> 
    </filter> 
    <match myapp.access> 
      @type file 
      path /var/log/fluent/access 
    </match>
    # input: http://this.host:9880/myapp.access?json={"event":"data"}
    # output: {"event": "data", "host_param": "#{Socket.gethostname}"}
    ```
    ```
    <filter foo.bar>
    @type grep

    <regexp>
        key message
        pattern /cool/
    </regexp>

    <regexp>
        key hostname
        pattern /^web\d+\.example\.com$/
    </regexp>

    <exclude>
        key message
        pattern /uncool/
    </exclude>
    </filter>
    ## Hence, the following events are kept:
    ## {"message":"It's cool outside today", "hostname":"web001.example.com"}
    ## {"message":"That's not cool", "hostname":"web1337.example.com"}
    ## whereas the following examples are filtered out:
    ## {"message":"I am cool but you are uncool", "hostname":"db001.example.com"}
    ## {"hostname":"web001.example.com"}
    ## {"message":"It's cool outside today"}
    ```
* [Output](https://docs.fluentd.org/parser)
* [Formatter](https://docs.fluentd.org/formatter)
* [Storage](https://docs.fluentd.org/storage)
* [Buffer](https://docs.fluentd.org/buffer)

```
docker build -t ekko771/fluentd-mogo:latest . -f Dockerfile
```

```
docker-compose up -d
```

# Reference
* [EFK(6) - 使用 docker 包裝 Fluentd](https://codingluka.com/use-docker-to-build-efk-stack/)
* [fluentd-vs-fluent-bit](https://logz.io/blog/fluentd-vs-fluent-bit/)
* [Monitoring by Prometheus](https://docs.fluentd.org/monitoring-fluentd/monitoring-prometheus)
* [Email Alerting like Splunk](https://docs.fluentd.org/how-to-guides/splunk-like-grep-and-alert-email)
* [fluentd quickstart](https://docs.fluentd.org/quickstart)
* [fluentd plugins](https://www.fluentd.org/plugins/all)
* [mongo plugins example configuration](https://docs.fluentd.org/output/mongo)
* [fluent-logger-python github](https://github.com/fluent/fluent-logger-python)
* [fluent-plugin-redis-store github](https://github.com/pokehanai/fluent-plugin-redis-store)
* [fluent-plugin-mongo github](https://github.com/fluent/fluent-plugin-mongo)
* [fluentd docker](https://hub.docker.com/r/fluent/fluentd)
