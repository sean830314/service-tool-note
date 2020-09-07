import elasticapm
import time
client = elasticapm.Client(service_name="train_model")
# a=CPUMetricSet(MetricsRegistry(client))
# elasticapm.instrument()

@elasticapm.capture_span("load data",span_type="db.mysql.query", labels={"type": "load_data"})
def load_data(data):
    try:
        time.sleep(4)
        elasticapm.label(ecommerce=True, db_label="get_data")
        client.capture_message(message="load data ok", custom=data)
    except Exception as e:
        client.capture_exception()

@elasticapm.capture_span("preprocess data",span_type="python.pandas", labels={"type": "preprocess_data"})
def preprocess_data(data):
    try:
        time.sleep(5)
        client.capture_message(message="preprocess data ok", custom=data)
    except Exception as e:
        client.capture_exception()

@elasticapm.capture_span("train model",span_type="python.tensorflow", labels={"type": "train_model"})
def train_model(data):
    try:
        time.sleep(15)
        data = {
            "architectures": [
                "BertForMaskedLM"
            ],
            "attention_probs_dropout_prob": 0.1,
            "hidden_act": "gelu",
            "hidden_dropout_prob": 0.1,
            "hidden_size": 768,
            "initializer_range": 0.02,
            "intermediate_size": 3072,
            "layer_norm_eps": 1e-12,
            "max_position_embeddings": 512,
            "model_type": "bert",
            "num_attention_heads": 12,
            "num_hidden_layers": 12,
            "pad_token_id": 0,
            "type_vocab_size": 2,
            "vocab_size": 30522
        }
        elasticapm.label(ecommerce=True, train_label="train_bert")
        client.capture_message(message="train model ok", custom=data)
    except Exception as e:
        client.capture_exception()

@elasticapm.capture_span("write data",span_type="db.mysql.query", labels={"type": "write_data"})
def write_data(data):
    try:
        time.sleep(1)
        elasticapm.label(ecommerce=True, db_label="write_data")
        client.capture_message(message="write data ok", custom=data)
    except Exception as e:
        client.capture_exception()

if __name__ == "__main__":
    data = {
        "custom_field": "test_value"
    }
    for i in range(100):
        client.begin_transaction(transaction_type="track-do-thing")
        time.sleep(4)
        load_data(data)
        preprocess_data(data)
        train_model(data)
        write_data(data)
        time.sleep(4)
        client.end_transaction("finish-do-thing", "success")
    client.capture_message(message="Done", custom=data)
