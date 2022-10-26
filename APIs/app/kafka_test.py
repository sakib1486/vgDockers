from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['broker:29092'])
producer.send('session_data', b'kafka test')
print("DONE")
