import mariadb
import pandas as pd
from dependency_injector.wiring import Provide
from .config import ConfigContainer, ConfigService


class Database(object):
    def __init__(
        self, config: ConfigService = Provide[ConfigContainer.config_svc].provider()
    ) -> None:
        self.connection: mariadb.connection = mariadb.connect(
            host=config.property("mariadb.host"),
            user=config.property("mariadb.user"),
            database=config.property("mariadb.database"),
            autocommit=True,
        )
        self.cursor: mariadb.connection.cursor = self.connection.cursor()
        self.averages_table: str = config.property("mariadb.averages-table")

    def get_daily_averages(self) -> pd.DataFrame:
        self.cursor.execute(
            "SELECT sku as SKU, count as DailyAverage FROM {averages_table}".format(
                averages_table=self.averages_table
            )
        )

        columns: list = [desc[0] for desc in self.cursor.description]
        df: pd.DataFrame = pd.DataFrame(data=self.cursor.fetchall(), columns=columns)
        return df.astype({"SKU": "int64"})

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()
