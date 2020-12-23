# RabbitMQ

## Introduction
AMQP，即 Advanced Message Queuing Protocol，高階訊息佇列協議，是應用層協議的一個開放標準，為面向訊息的中介軟體設計。訊息中介軟體主要用於元件之間的解耦和通訊。

AMQP的主要特徵是面向訊息、佇列、路由（包括點對點和釋出/訂閱）、可靠性、安全。

RabbitMQ是一個開源的AMQP實現，伺服器端用 Erlang 語言編寫，支援多種客戶端，如：Python、Ruby、.NET、Java、JMS、C、PHP、ActionScript、XMPP、STOMP等，支援AJAX。用於在分散式系統中儲存轉發訊息，具有很高的易用性和可用性。

# Term and Concept
* Queue.

    存放訊息的地方,跟一般資料結構的Queue一樣具有fist-in-first-out特性，且每個Queue都有自己的id
* Producer.

    負責將訊息丟到Queue裡面，若有定義Exchange，則通過Exchange決定要進哪個Queue
* Consumer.

    負責接收Queue裡面的訊息
* Exchange.

    用來決定Producer丟過來的資料要送給哪個Queue，主要有四種方式
    
    1. direct: 直接丟給指定的 Queue
    ![Alt text](./png/prefetch-count.webp)
    [work queue code](./work_queue)
    2. topic: 類似 regular expression，設定 binding 規則，丟給符合的 Queue
    3. headers: 透過傳送資料的 header 來特別指定所要的 Queue
    4. fanout: 一次丟給全部負責的 Queue
* Binding.

    跟 Exchange 成對搭配，主要是告訴 Exchange 他負責哪些 Queue

# Common commands
1. list queues
```
rabbitmqctl list_queues
```
2. list jobs by queue name
```
rabbitmqadmin get queue=document_analysis requeue=true count=10
```

# Tips
* Setting Message durability

    1. make message persistent
        ```
        channel.basic_publish(exchange='',
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
        ``` 
    2. make queue persistent
        ```
        channel.queue_declare(queue='task_queue', durable=True)
        ```
* Fair dispatch

    調度無法完全按照我們的要求進行。例如在有兩名工人的情況下，當奇數的消息都很重，而偶數消息很輕時，一位工人將一直忙碌而另一位工人將幾乎不做任何工作。RabbitMQ對此一無所知，並且仍將平均分派消息。

    發生這種情況是因為RabbitMQ在消息進入隊列時才調度消息。 它不會查看消費者的未確認消息數。 它只是盲目地將每第n條消息發送給第n個使用者。

    ![Alt text](./png/prefetch-count.webp)

    為了解決這個問題，我們可以將Channel＃basic_qos通道方法與prefetch_count = 1設置一起使用。這使用basic.qos協議方法來告訴RabbitMQ一次不向工作人員發送多條消息。
    ```
    channel.basic_qos(prefetch_count=1)
    ```
