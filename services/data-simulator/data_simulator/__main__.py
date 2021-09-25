import random
import json

from .ProductCatalog import ProductCatalog
from .config import ConfigContainer, ConfigService
from datetime import date, timedelta
from dependency_injector.wiring import Provide
from kafka import KafkaProducer

config: ConfigService = Provide[ConfigContainer.config_svc].provider()

producer = KafkaProducer(
    bootstrap_servers=config.property("kafka.brokers"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    batch_size=config.property("kafka.batch-size"),
)

random.seed(config.property("simulation.seed"))
MIN_DAILY_CUSTOMER_COUNT = config.property("simulation.min-daily-customer-count")
MAX_DAILY_CUSTOMER_COUNT = config.property("simulation.max-daily-customer-count")
WEEKEND_CUSTOMER_INCREASE = config.property("simulation.weekend-customer-increase")
PRICE_MULTIPLIER = config.property("simulation.price-multiplier")
MAX_ITEMS_PER_CUSTOMER = config.property("simulation.max-items-per-customer")
product_catalog = ProductCatalog()


def buy_milk(customer_id, date_bought):
    items_bought_count = 0
    # First see if we should buy milk
    if random.randint(1, 100) <= 70:
        # Should buy milk
        milk_to_buy = product_catalog.get_random_item("MILK")
        buy_item(customer_id, date_bought, milk_to_buy)
        items_bought_count += 1
        # Half of these people should also buy cereal
        if random.randint(1, 100) <= 50:
            cereal_to_buy = product_catalog.get_random_item("CEREAL")
            buy_item(customer_id, date_bought, cereal_to_buy)
            items_bought_count += 1
    elif (
        random.randint(1, 100) <= 5
    ):  # 5% of customers that don't buy milk will buy cereal
        cereal_to_buy = product_catalog.get_random_item("CEREAL")
        buy_item(customer_id, date_bought, cereal_to_buy)
        items_bought_count += 1
    return items_bought_count


def buy_baby_food(customer_id, date_bought):
    items_bought_count = 0
    if random.randint(1, 100) <= 20:
        # Should buy baby food
        baby_food_to_buy = product_catalog.get_random_item("BABY FOOD")
        buy_item(customer_id, date_bought, baby_food_to_buy)
        items_bought_count += 1
        if random.randint(1, 100) <= 80:
            # Also buy diapers
            diapers_to_buy = product_catalog.get_random_item("DIAPERS")
            buy_item(customer_id, date_bought, diapers_to_buy)
            items_bought_count += 1
    elif random.randint(1, 100) <= 1:
        # Didn't buy baby food, but should buy diapers
        diapers_to_buy = product_catalog.get_random_item("DIAPERS")
        buy_item(customer_id, date_bought, diapers_to_buy)
        items_bought_count += 1
    return items_bought_count


def buy_bread(customer_id, date_bought):
    items_bought_count = 0
    if random.randint(1, 100) <= 50:
        bread_to_buy = product_catalog.get_random_item("BREAD")
        buy_item(customer_id, date_bought, bread_to_buy)
        items_bought_count += 1
    return items_bought_count


def buy_peanut_butter(customer_id, date_bought):
    items_bought_count = 0
    if random.randint(1, 100) <= 10:
        peanut_butter_to_buy = product_catalog.get_random_item("PEANUT BUTTER")
        buy_item(customer_id, date_bought, peanut_butter_to_buy)
        items_bought_count += 1
        if random.randint(1, 100) <= 90:
            jelly_to_buy = product_catalog.get_random_item("JELLY/JAM")
            buy_item(customer_id, date_bought, jelly_to_buy)
            items_bought_count += 1
    elif random.randint(1, 100) <= 5:
        jelly_to_buy = product_catalog.get_random_item("JELLY/JAM")
        buy_item(customer_id, date_bought, jelly_to_buy)
        items_bought_count += 1
    return items_bought_count


def buy_item(customer_id, date_bought, item_bought):
    sale_price = round(item_bought["BasePrice"].item() * PRICE_MULTIPLIER, 2)
    transaction = {
        "date": date_bought.isoformat(),
        "customer_id": customer_id,
        "sku": item_bought["SKU"].item(),
        "sale_price": sale_price,
    }
    producer.send(config.property("kafka.topic"), transaction)


def main():
    current_date: date = config.date("simulation.start-date")
    stop_date: date = config.date("simulation.stop-date")
    current_customer_id = 0  # TODO: should we re-use some customer IDs?
    while current_date <= stop_date:
        print("DAY %s " % current_date.isoformat())
        increase = 0
        if current_date.weekday() > 5:  # Saturday, Sunday return 6, 7
            increase = WEEKEND_CUSTOMER_INCREASE
        for _ in range(
            random.randint(
                min(MIN_DAILY_CUSTOMER_COUNT + increase, MAX_DAILY_CUSTOMER_COUNT),
                MAX_DAILY_CUSTOMER_COUNT,
            )
        ):
            # Iterate for each customer
            current_customer_id += 1
            items_bought = 0
            items_bought += buy_milk(current_customer_id, current_date)
            items_bought += buy_baby_food(current_customer_id, current_date)
            items_bought += buy_bread(current_customer_id, current_date)
            items_bought += buy_peanut_butter(current_customer_id, current_date)

            for __ in range(random.randint(1, MAX_ITEMS_PER_CUSTOMER - items_bought)):
                # We've already bought milk and other things we are supposed to buy
                # Let's buy some other SKUs
                random_item_to_buy = product_catalog.get_random_item()
                buy_item(current_customer_id, current_date, random_item_to_buy)

        current_date = current_date + timedelta(days=1)

    producer.flush()
    print("done")

if __name__ == "__main__":
    main()
