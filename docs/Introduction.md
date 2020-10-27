# Elastic-APM

## OpenTracing

     OpenTracing is comprised of an API specification, frameworks and libraries that have implemented the specification, and documentation for the project. OpenTracing allows developers to add instrumentation to their application code using APIs that do not lock them into any one particular product or vendor.

## Distributed Tracing

     Most mental models for tracing descend from Google’s Dapper paper. OpenTracing uses similar nouns and verbs.

        1.Trace: The description of a transaction as it moves through a distributed system.
        2.Span: A named, timed operation representing a piece of the workflow. Spans accept key:value tags as well as fine-grained, timestamped, structured logs attached to the particular span instance.
        3.Span context: Trace information that accompanies the distributed transaction, including when it passes the service to service over the network or through a message bus. The span context contains the trace identifier, span identifier, and any other data that the tracing system needs to propagate to the downstream service.# Elastic-APM
---------------------------------------
## OpenTracing

OpenTracing is comprised of an API specification, frameworks and libraries that have implemented the specification, and documentation for the project. OpenTracing allows developers to add instrumentation to their application code using APIs that do not lock them into any one particular product or vendor.

## Distributed Tracing

Most mental models for tracing descend from Google’s Dapper paper. OpenTracing uses similar nouns and verbs.

1. Trace: The description of a transaction as it moves through a distributed system.

2. Span: A named, timed operation representing a piece of the workflow. Spans accept key:value tags as well as fine-grained, timestamped, structured logs attached to the particular span instance.

3. Span context: Trace information that accompanies the distributed transaction, including when it passes the service to service over the network or through a message bus. The span context contains the trace identifier, span identifier, and any other data that the tracing system needs to propagate to the downstream service.

## APM Components

APM consists of four main components that work together to monitor application performance. These components are as follows:

### APM Server

The APM Server receives data from APM agents and transforms them into Elasticsearch documents. It does this by exposing an HTTP server endpoint to which agents stream the APM data they collect. After the APM Server has validated and processed events from the APM agents, the server transforms the data into Elasticsearch documents and stores them in corresponding Elasticsearch indices.

### Elasticsearch

Elasticsearch is the distributed search and analytics engine at the heart of the Elastic Stack, and provides near real-time search and analytics for all types of data. Whether you have structured or unstructured text, numerical data, or geospatial data, Elasticsearch can efficiently store and index it in a way that supports fast searches. You can go far beyond simple data retrieval and aggregate information to discover trends and patterns in your data. And as your data and query volume grows, the distributed nature of Elasticsearch enables your deployment to grow seamlessly right along with it.

### Kibana

We have two options in Kibana to visualize APM data. The first option is to use the dedicated APM UI that is available under the APM link in the left-hand side menu. The second option is to use the default Kibana dashboard, which is mainly used to visualize other data sources. We can visualize and search the APM performance metrics data in Kibana.

### APM agents

Elastic APM agents are open source libraries that can be configured in Elastic supported languages and frameworks. Once the APM agent is configured, it can be used to collect data, metrics, errors, and more from the application at runtime. The APM agent can buffer the data for some time and then send it to the APM Server. Currently, APM agents are supported for the following:

* Go
* Java
* .NET
* Node.js
* Python
* Ruby
* Javascript
