import random
import json
import pandas as pd

from .catalog import ProductCatalog
from .config import ConfigContainer, ConfigService
from datetime import date, timedelta
from dependency_injector.wiring import Provide
from kafka import KafkaProducer
from PyProbs import Probability as pr
from typing import List

config: ConfigService = Provide[ConfigContainer.config_svc].provider()

producer = KafkaProducer(
    bootstrap_servers=config.property("kafka.brokers"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

random.seed(config.property("simulation.seed"))
MIN_DAILY_CUSTOMER_COUNT = config.property("simulation.min-daily-customer-count")
MAX_DAILY_CUSTOMER_COUNT = config.property("simulation.max-daily-customer-count")
WEEKEND_CUSTOMER_INCREASE = config.property("simulation.weekend-customer-increase")
PRICE_MULTIPLIER = config.property("simulation.price-multiplier")
MAX_ITEMS_PER_CUSTOMER = config.property("simulation.max-items-per-customer")

CHANCE_OF_REGULAR_CUSTOMER = config.property("simulation.chance-regular-customer-visits")
CHANCE_OF_KEEPING_NEW_CUSTOMER = config.property("simulation.chance-new-customer-becomes-regular")
CHANCE_OF_LOSING_REGULAR_CUSTOMER = config.property("simulation.chance-of-losing-regular-customer")

product_catalog: ProductCatalog = ProductCatalog()
customers: set = set(range(1, config.property("simulation.number-of-unique-customers") + 1))


def buy_milk(purchases: List[dict]) -> List[dict]:
    if pr.Prob(0.7):
        # Should buy milk
        make_purchase(purchases, "MILK")
        # Half of these people should also buy cereal
        if pr.Prob(0.5):
            make_purchase(purchases, "CEREAL")
    # 5% of customers that don't buy milk will buy cereal
    elif pr.Prob(0.05):
        make_purchase(purchases, "CEREAL")
    return purchases


def buy_baby_food(purchases: List[dict]) -> List[dict]:
    if pr.Prob(0.2):
        # Should buy baby food
        make_purchase(purchases, "BABY FOOD")
        if pr.Prob(0.8):
            # Also buy diapers
            make_purchase(purchases, "DIAPERS")
    elif pr.Prob(0.01):
        # Didn't buy baby food, but should buy diapers
        make_purchase(purchases, "DIAPERS")
    return purchases


def buy_bread(purchases: List[dict]) -> List[dict]:
    if pr.Prob(0.5):
        make_purchase(purchases, "BREAD")
    return purchases


def buy_peanut_butter(purchases: List[dict]) -> List[dict]:
    if pr.Prob(0.1):
        make_purchase(purchases, "PEANUT BUTTER")
        if pr.Prob(0.9):
            make_purchase(purchases, "JELLY/JAM")
    elif pr.Prob(0.05):
        make_purchase(purchases, "JELLY/JAM")
    return purchases


def make_purchase(purchases: List[dict], item_type: str = None) -> List[dict]:
    item_bought: pd.DataFrame = product_catalog.find_item_to_purchase(item_type)
    if item_bought is not None:
        sale_price: float = round(item_bought["BasePrice"].item() * PRICE_MULTIPLIER, 2)
        purchase = {
            "sku": item_bought["SKU"].item(),
            "sale_price": sale_price,
            "items_left": item_bought["CurrentStock"].item(),
            "total_cases_ordered": item_bought["CasesOrdered"].item(),
        }
        purchases.append(purchase)
    return purchases


def get_customer() -> int:
    customer: int = 0
    if pr.Prob(CHANCE_OF_REGULAR_CUSTOMER):
        customer = random.choice(tuple(customers))

        if pr.Prob(CHANCE_OF_LOSING_REGULAR_CUSTOMER):
            customers.remove(customer)
    else:
        customer = max(customers) + 1
        if pr.Prob(CHANCE_OF_KEEPING_NEW_CUSTOMER):
            customers.add(customer)
    return customer


def main() -> None:
    current_date: date = config.date("simulation.start-date")
    stop_date: date = config.date("simulation.stop-date")

    transaction_id: int = 0
    while current_date <= stop_date:
        previous_stock = product_catalog.total_inventory()
        product_catalog.refresh_stock(current_date)
        current_stock = product_catalog.total_inventory()
        print(
            "date: {date} \t total inventory: {inv} \t deliveries: {delivery}".format(
                date=current_date.strftime("%a, %b %d"),
                inv=current_stock,
                delivery=current_stock - previous_stock
            )
        )

        weekday = current_date.strftime("%A")
        increase = WEEKEND_CUSTOMER_INCREASE if weekday == "Saturday" or weekday == "Sunday" else 0

        for _ in range(
            random.randint(
                MIN_DAILY_CUSTOMER_COUNT + increase,
                MAX_DAILY_CUSTOMER_COUNT + increase,
            )
        ):
            customer_id: int = get_customer()
            transaction_id += 1
            items_bought = []
            buy_milk(items_bought)
            buy_baby_food(items_bought)
            buy_bread(items_bought)
            buy_peanut_butter(items_bought)

            for __ in range(random.randint(1, MAX_ITEMS_PER_CUSTOMER - len(items_bought))):
                make_purchase(items_bought)

            for purchase in items_bought:
                purchase["customer_id"] = customer_id
                purchase["transaction_id"] = transaction_id
                purchase["date"] = current_date.isoformat()
                producer.send(config.property("kafka.topic"), purchase)

        current_date = current_date + timedelta(days=1)

    producer.flush()
    print("done")


if __name__ == "__main__":
    main()
