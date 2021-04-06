FROM rabbitmq:3-management
RUN apt update
RUN apt install -y  wget
RUN wget -O /opt/rabbitmq/plugins/elixir-1.10.4.ez https://github.com/noxdafox/rabbitmq-message-deduplication/releases/download/0.5.0/elixir-1.10.4.ez
RUN wget -O /opt/rabbitmq/plugins/rabbitmq_message_deduplication-0.5.0.ez https://github.com/noxdafox/rabbitmq-message-deduplication/releases/download/0.5.0/rabbitmq_message_deduplication-0.5.0.ez
RUN rabbitmq-plugins enable rabbitmq_message_deduplication
