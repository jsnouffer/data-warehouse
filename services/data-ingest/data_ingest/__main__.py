import json
import mariadb
from dependency_injector.wiring import Provide
from kafka import KafkaConsumer
from .config import ConfigContainer, ConfigService


def main(config: ConfigService = Provide[ConfigContainer.config_svc].provider()):
    connection = mariadb.connect(
        host=config.property("mariadb.host"), user=config.property("mariadb.user"), database=config.property("mariadb.database"), autocommit=True
    )
    cursor = connection.cursor()

    if config.property("create-new-database", False):
        cursor.execute("DROP TABLE IF EXISTS transactions")
        cursor.execute(
            """
            CREATE TABLE transactions
            (
            transaction_id INT PRIMARY KEY auto_increment,
            customer_id BIGINT,
            sku INT,
            sale_price FLOAT,
            transaction_date DATE
            )"""
        )

    consumer = KafkaConsumer(
        config.property("kafka.topic"),
        bootstrap_servers=config.property("kafka.brokers"),
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id=config.property("kafka.group-id"),
    )
    for message in consumer:
        transaction = message.value
        cursor.execute(
            "INSERT INTO transactions (customer_id, sku, sale_price, transaction_date) VALUES (?,?,?,?)",
            (
                transaction["customer_id"],
                transaction["sku"],
                transaction["sale_price"],
                transaction["date"],
            ),
        )

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
