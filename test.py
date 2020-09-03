from elasticapm import Client

client = Client(service_name="test")

if __name__ == "__main__":
    data = {
        'name': 'Joe Bloggs'
    }

    client.capture_message('Test Message3', custom=data)
