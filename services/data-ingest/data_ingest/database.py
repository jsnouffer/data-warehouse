import mariadb
import pandas as pd
from dependency_injector.wiring import Provide
from .config import ConfigContainer, ConfigService


class Database(object):
    def __init__(
        self, config: ConfigService = Provide[ConfigContainer.config_svc].provider()
    ):
        self.connection = mariadb.connect(
            host=config.property("mariadb.host"),
            user=config.property("mariadb.user"),
            database=config.property("mariadb.database"),
            autocommit=True,
        )
        self.cursor = self.connection.cursor()

        if config.property("create-new-database", False):
            self.cursor.execute("DROP TABLE IF EXISTS transactions")
            self.cursor.execute("DROP TABLE IF EXISTS catalog")
            self.cursor.execute(
                """
                CREATE TABLE catalog (
                    manufacturer TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    size TEXT NOT NULL,
                    item_type TEXT,
                    sku INT UNSIGNED NOT NULL PRIMARY KEY,
                    base_price DECIMAL(65,2) UNSIGNED NOT NULL,
                    INDEX (manufacturer(255)),
                    INDEX (product_name(255)),
                    INDEX (item_type(255)),
                    INDEX description (manufacturer(255), product_name(255))
                )
                """
            )
            self.cursor.execute(
                """
                CREATE TABLE transactions
                (
                    id INT PRIMARY KEY auto_increment,
                    transaction_id BIGINT UNSIGNED NOT NULL,
                    customer_id BIGINT UNSIGNED NOT NULL,
                    sku INT UNSIGNED NOT NULL,
                    sale_price DECIMAL(65,2) UNSIGNED NOT NULL,
                    transaction_date DATE NOT NULL,
                    INDEX (transaction_id),
                    INDEX (customer_id),
                    INDEX (sku),
                    CONSTRAINT `fk_sku` FOREIGN KEY (sku) REFERENCES catalog (sku)
                )
                """
            )

            df = pd.read_csv("Products1.txt", sep="|")
            df.columns = df.columns.str.replace(" ", "")
            df.fillna('', inplace=True)
            df["BasePrice"] = (
                df["BasePrice"].replace("[\$,]", "", regex=True).astype(float)
            )
            df["itemType"] = df["itemType"].str.upper()

            for row in df.itertuples():
                self.cursor.execute(
                    "INSERT INTO catalog (manufacturer, product_name, size, item_type, sku, base_price) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        row.Manufacturer,
                        row.ProductName,
                        row.Size,
                        row.itemType,
                        row.SKU,
                        row.BasePrice,
                    ),
                )

    def insert(self, transaction):
        self.cursor.execute(
            "INSERT INTO transactions (transaction_id, customer_id, sku, sale_price, transaction_date) VALUES (?,?,?,?,?)",
            (
                transaction["transaction_id"],
                transaction["customer_id"],
                transaction["sku"],
                transaction["sale_price"],
                transaction["date"],
            ),
        )

    def close(self):
        self.cursor.close()
        self.connection.close()
