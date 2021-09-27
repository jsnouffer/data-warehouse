import random
import json

from .catalog import ProductCatalog
from .config import ConfigContainer, ConfigService
from datetime import date, timedelta
from dependency_injector.wiring import Provide
from kafka import KafkaProducer
from PyProbs import Probability as pr

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

CHANCE_OF_REGULAR_CUSTOMER = config.property(
    "simulation.chance-regular-customer-visits"
)
CHANCE_OF_KEEPING_NEW_CUSTOMER = config.property(
    "simulation.chance-new-customer-becomes-regular"
)
CHANCE_OF_LOSING_REGULAR_CUSTOMER = config.property(
    "simulation.chance-of-losing-regular-customer"
)

product_catalog = ProductCatalog()
customers = set(range(1, config.property("simulation.number-of-unique-customers") + 1))


def buy_milk():
    items_bought = []
    if pr.Prob(0.7):
        # Should buy milk
        milk_to_buy = product_catalog.get_random_item("MILK")
        items_bought.append(buy_item(milk_to_buy))
        # Half of these people should also buy cereal
        if pr.Prob(0.5):
            cereal_to_buy = product_catalog.get_random_item("CEREAL")
            items_bought.append(buy_item(cereal_to_buy))
    # 5% of customers that don't buy milk will buy cereal
    elif pr.Prob(0.05):
        cereal_to_buy = product_catalog.get_random_item("CEREAL")
        items_bought.append(buy_item(cereal_to_buy))
    return items_bought


def buy_baby_food():
    items_bought = []
    if pr.Prob(0.2):
        # Should buy baby food
        baby_food_to_buy = product_catalog.get_random_item("BABY FOOD")
        items_bought.append(buy_item(baby_food_to_buy))
        if pr.Prob(0.8):
            # Also buy diapers
            diapers_to_buy = product_catalog.get_random_item("DIAPERS")
            items_bought.append(buy_item(diapers_to_buy))
    elif pr.Prob(0.01):
        # Didn't buy baby food, but should buy diapers
        diapers_to_buy = product_catalog.get_random_item("DIAPERS")
        items_bought.append(buy_item(diapers_to_buy))
    return items_bought


def buy_bread():
    items_bought = []
    if pr.Prob(0.5):
        bread_to_buy = product_catalog.get_random_item("BREAD")
        items_bought.append(buy_item(bread_to_buy))
    return items_bought


def buy_peanut_butter():
    items_bought = []
    if pr.Prob(0.1):
        peanut_butter_to_buy = product_catalog.get_random_item("PEANUT BUTTER")
        items_bought.append(buy_item(peanut_butter_to_buy))
        if pr.Prob(0.9):
            jelly_to_buy = product_catalog.get_random_item("JELLY/JAM")
            items_bought.append(buy_item(jelly_to_buy))
    elif pr.Prob(0.05):
        jelly_to_buy = product_catalog.get_random_item("JELLY/JAM")
        items_bought.append(buy_item(jelly_to_buy))
    return items_bought


def buy_item(item_bought) -> dict:
    sale_price = round(item_bought["BasePrice"].item() * PRICE_MULTIPLIER, 2)
    item = {
        "sku": item_bought["SKU"].item(),
        "sale_price": sale_price,
    }
    return item


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


def main():
    current_date: date = config.date("simulation.start-date")
    stop_date: date = config.date("simulation.stop-date")

    transaction_id: int = 0
    while current_date <= stop_date:
        print("DAY %s " % current_date.isoformat())
        print("MAX %s SIZE %s" % (max(customers), len(customers)))
        
        weekday = current_date.strftime("%A")
        increase = WEEKEND_CUSTOMER_INCREASE if weekday == 'Saturday' or weekday == 'Sunday' else 0

        for _ in range(
            random.randint(
                MIN_DAILY_CUSTOMER_COUNT + increase,
                MAX_DAILY_CUSTOMER_COUNT + increase,
            )
        ):
            customer_id: int = get_customer()
            transaction_id += 1
            items_bought = []
            items_bought.extend(buy_milk())
            items_bought.extend(buy_baby_food())
            items_bought.extend(buy_bread())
            items_bought.extend(buy_peanut_butter())

            for __ in range(
                random.randint(1, MAX_ITEMS_PER_CUSTOMER - len(items_bought))
            ):
                random_item_to_buy = product_catalog.get_random_item()
                items_bought.append(buy_item(random_item_to_buy))

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
