import pandas as pd


class ProductCatalog(object):
    def __init__(self):
        df = pd.read_csv("Products1.txt", sep="|")
        df["BasePrice"] = df["BasePrice"].replace("[\$,]", "", regex=True).astype(float)
        df["itemType"] = df["itemType"].str.upper()

        strict_categories = [
            "MILK",
            "BABY FOOD",
            "CEREAL",
            "DIAPERS",
            "BREAD",
            "PEANUT BUTTER",
            "JELLY/JAM",
        ]
        self.other_products = df[~df["itemType"].isin(strict_categories)]
        self.strict_products = df[df["itemType"].isin(strict_categories)]

    def get_random_item(self, item_type=None):
        if item_type:
            return self.strict_products.loc[
                self.strict_products["itemType"] == item_type
            ].sample()

        return self.other_products.sample()
