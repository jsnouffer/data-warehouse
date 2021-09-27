import json
from dependency_injector.wiring import Provide
from kafka import KafkaConsumer, TopicPartition
from .config import ConfigContainer, ConfigService
from .database import Database


def main(config: ConfigService = Provide[ConfigContainer.config_svc].provider()):
    database: Database = Database()

    consumer = KafkaConsumer(
        bootstrap_servers=config.property("kafka.brokers"),
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id=config.property("kafka.group-id"),
        auto_offset_reset="earliest",
    )
    tp = TopicPartition(topic=config.property("kafka.topic"), partition=0)
    consumer.assign([tp])
    consumer.seek(tp, 0)

    for message in consumer:
        database.insert(message.value)

    database.close()


if __name__ == "__main__":
    main()
