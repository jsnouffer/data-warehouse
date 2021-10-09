import math
import pandas as pd

from .config import ConfigContainer, ConfigService
from .database import Database
from datetime import date
from dependency_injector.wiring import Provide
from typing import List

config: ConfigService = Provide[ConfigContainer.config_svc].provider()

DESIRED_STOCK_MODIFIER: float = config.property("simulation.desired-stock-modifier")
DESIRED_STOCK_MODIFIER_MILK: float = config.property("simulation.desired-stock-modifier-milk")
DELIVERY_DAYS: List[str] = config.property("simulation.delivery-days").split(",")
CASE_SIZE: int = config.property("simulation.case-size")


class ProductCatalog(object):
    def __init__(self) -> None:
        df: pd.DataFrame = pd.read_csv("Products1.txt", sep="|")
        df["BasePrice"] = df["BasePrice"].replace("[\$,]", "", regex=True).astype(float)
        df["itemType"] = df["itemType"].str.upper()
        df["CasesOrdered"] = 0

        # Retrieve daily averages
        db: Database = Database()
        averages: pd.DataFrame = db.get_daily_averages()
        db.close()
        df = df.join(averages.set_index("SKU"), on="SKU")

        # Populate desired and initial stock levels
        df["DesiredStock"] = df["DailyAverage"] * DESIRED_STOCK_MODIFIER
        df.loc[df["itemType"] == "MILK", ["DesiredStock"]] = (
            df["DailyAverage"] * DESIRED_STOCK_MODIFIER_MILK
        )
        df["CurrentStock"] = round(df["DesiredStock"]).astype("int32")

        strict_categories = [
            "MILK",
            "BABY FOOD",
            "CEREAL",
            "DIAPERS",
            "BREAD",
            "PEANUT BUTTER",
            "JELLY/JAM",
        ]
        self.other_products: pd.DataFrame = df[~df["itemType"].isin(strict_categories)]
        self.strict_products: pd.DataFrame = df[df["itemType"].isin(strict_categories)]

    def find_item_to_purchase(self, item_type: str = None) -> pd.DataFrame:
        item: pd.DataFrame = None
        if item_type:
            try:
                item = self.strict_products[
                    (self.strict_products["itemType"] == item_type)
                    & (self.strict_products["CurrentStock"] > 0)
                ].sample()
            except ValueError:
                print("Out of stock: " + item_type)
        else:
            item = self.other_products.loc[self.other_products["CurrentStock"] > 0].sample()

        if item is not None:
            item["CurrentStock"] -= 1

            if (self.strict_products.index == item.index.item()).any():
                self.strict_products.at[item.index.item(), "CurrentStock"] = item["CurrentStock"]
            else:
                self.other_products.at[item.index.item(), "CurrentStock"] = item["CurrentStock"]

        return item

    def refresh_stock(self, current_date: date) -> None:
        if current_date.strftime("%A") in DELIVERY_DAYS:
            self.other_products = self.other_products.apply(self.replenish_product, axis=1)
            self.strict_products = self.strict_products.apply(self.replenish_product, axis=1)
        else:
            self.strict_products = self.strict_products.apply(
                self.replenish_product, axis=1, type="MILK"
            )

    def replenish_product(self, row, **kwargs):
        if "type" in kwargs.keys() and row["itemType"] != kwargs["type"]:
            return row

        if row["CurrentStock"] < row["DesiredStock"]:
            cases = int(math.ceil((row["DesiredStock"] - row["CurrentStock"]) / float(CASE_SIZE)))
            row["CurrentStock"] += cases * CASE_SIZE
            row["CasesOrdered"] += cases
        return row

    def total_inventory(self) -> int:
        return (
            self.strict_products["CurrentStock"].sum() + self.other_products["CurrentStock"].sum()
        )
