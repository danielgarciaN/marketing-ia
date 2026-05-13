"""
Generate a realistic synthetic dataset mimicking the UCI Online Retail Dataset.
~50K transactions, ~2000 customers, multiple countries, realistic products and patterns.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# --- Products catalog ---
PRODUCTS = [
    ("85123A", "WHITE HANGING HEART T-LIGHT HOLDER", 2.55),
    ("71053", "WHITE METAL LANTERN", 3.39),
    ("84406B", "CREAM CUPID HEARTS COAT HANGER", 2.75),
    ("84029G", "KNITTED UNION FLAG HOT WATER BOTTLE", 3.39),
    ("84029E", "RED WOOLLY HOTTIE WHITE HEART.", 3.39),
    ("22752", "SET 7 BABUSHKA NESTING BOXES", 7.65),
    ("21730", "GLASS STAR FROSTED T-LIGHT HOLDER", 4.25),
    ("22633", "HAND WARMER UNION JACK", 1.85),
    ("22632", "HAND WARMER RED POLKA DOT", 1.85),
    ("84879", "ASSORTED COLOUR BIRD ORNAMENT", 1.69),
    ("22745", "POPPY'S PLAYHOUSE BEDROOM", 2.10),
    ("22748", "POPPY'S PLAYHOUSE KITCHEN", 2.10),
    ("22749", "FELTCRAFT PRINCESS CHARLOTTE DOLL", 3.75),
    ("22310", "IVORY KNITTED MUG COSY", 1.65),
    ("84969", "BOX OF 6 ASSORTED COLOUR TEASPOONS", 4.25),
    ("22623", "BOX OF VINTAGE JIGSAW BLOCKS", 4.95),
    ("22411", "JUMBO SHOPPER VINTAGE RED PAISLEY", 2.08),
    ("22386", "JUMBO BAG PINK POLKADOT", 1.95),
    ("21232", "STRAWBERRY CERAMIC TRINKET BOX", 1.25),
    ("22382", "LUNCH BAG SPACEBOY DESIGN", 1.65),
    ("22383", "LUNCH BAG SUKI DESIGN", 1.65),
    ("10002", "INFLATABLE POLITICAL GLOBE", 0.85),
    ("22492", "MINI PAINT SET VINTAGE", 0.65),
    ("22551", "PLASTERS IN TIN SPACEBOY", 1.65),
    ("22552", "PLASTERS IN TIN STRONGMAN", 1.65),
    ("22326", "ROUND SNACK BOXES SET OF4 WOODLAND", 2.95),
    ("22629", "SPACEBOY LUNCH BOX", 1.95),
    ("22659", "LUNCH BAG CARS BLUE", 1.65),
    ("22697", "GREEN REGENCY TEACUP AND SAUCER", 2.95),
    ("22698", "PINK REGENCY TEACUP AND SAUCER", 2.95),
    ("47566", "PARTY BUNTING", 4.95),
    ("21928", "JUMBO BAG WOODLAND ANIMALS", 2.08),
    ("22086", "PAPER CHAIN KIT 50'S CHRISTMAS", 2.95),
    ("22910", "PAPER CHAIN KIT VINTAGE CHRISTMAS", 2.95),
    ("22423", "REGENCY CAKESTAND 3 TIER", 12.75),
    ("22467", "GUMBALL COAT RACK", 2.55),
    ("22469", "HEART OF WICKER SMALL", 1.65),
    ("22470", "HEART OF WICKER LARGE", 2.95),
    ("21175", "GIN + TONIC DIET METAL SIGN", 2.10),
    ("21176", "CHOCOLATE HOT WATER BOTTLE", 4.25),
    ("23084", "RABBIT NIGHT LIGHT", 1.79),
    ("23298", "SPOTTY BUNNY DOORSTOP", 4.95),
    ("23300", "GARDENERS KNEELING PAD CUP OF TEA", 2.10),
    ("23301", "GARDENERS KNEELING PAD KEEP CALM", 2.10),
    ("23355", "HOT WATER BOTTLE KEEP CALM", 4.95),
    ("23356", "HOT WATER BOTTLE TEA AND SYMPATHY", 4.95),
    ("22993", "SET OF 4 PANTRY JELLY MOULDS", 1.25),
    ("22722", "SET OF 6 SOLDIER SKITTLES", 5.95),
    ("22579", "WOODEN TREE CHRISTMAS SCANDINAVIAN", 1.25),
    ("22580", "ADVENT CALENDAR GINGHAM SACK", 2.95),
]

COUNTRIES = {
    "United Kingdom": 0.82,
    "Germany": 0.035,
    "France": 0.035,
    "Spain": 0.02,
    "Netherlands": 0.015,
    "Belgium": 0.012,
    "Switzerland": 0.01,
    "Portugal": 0.008,
    "Italy": 0.008,
    "Australia": 0.007,
    "Norway": 0.006,
    "Sweden": 0.005,
    "Denmark": 0.004,
    "Japan": 0.003,
    "Finland": 0.003,
    "Austria": 0.003,
    "USA": 0.003,
    "Canada": 0.002,
    "Ireland": 0.001,
}

N_CUSTOMERS = 2000
N_INVOICES = 12000
START_DATE = datetime(2010, 12, 1)
END_DATE = datetime(2011, 12, 9)

def generate_customers():
    """Generate customer profiles with purchasing behavior patterns."""
    customers = []
    countries = list(COUNTRIES.keys())
    country_weights = list(COUNTRIES.values())

    for i in range(N_CUSTOMERS):
        cid = 12346 + i
        country = np.random.choice(countries, p=country_weights)

        # Customer archetype determines behavior
        archetype = np.random.choice(
            ["vip", "loyal", "regular", "occasional", "one_time"],
            p=[0.05, 0.15, 0.30, 0.30, 0.20]
        )

        if archetype == "vip":
            avg_orders = np.random.randint(20, 60)
            avg_items = np.random.randint(8, 25)
            price_mult = np.random.uniform(1.0, 1.5)
            recency_bias = 0.8  # recent purchases likely
        elif archetype == "loyal":
            avg_orders = np.random.randint(10, 25)
            avg_items = np.random.randint(4, 15)
            price_mult = np.random.uniform(0.9, 1.2)
            recency_bias = 0.7
        elif archetype == "regular":
            avg_orders = np.random.randint(4, 12)
            avg_items = np.random.randint(2, 8)
            price_mult = np.random.uniform(0.8, 1.1)
            recency_bias = 0.5
        elif archetype == "occasional":
            avg_orders = np.random.randint(2, 5)
            avg_items = np.random.randint(1, 5)
            price_mult = np.random.uniform(0.7, 1.0)
            recency_bias = 0.3
        else:  # one_time
            avg_orders = 1
            avg_items = np.random.randint(1, 4)
            price_mult = np.random.uniform(0.6, 1.0)
            recency_bias = 0.2

        customers.append({
            "CustomerID": cid,
            "Country": country,
            "archetype": archetype,
            "avg_orders": avg_orders,
            "avg_items": avg_items,
            "price_mult": price_mult,
            "recency_bias": recency_bias,
        })
    return customers


def generate_transactions(customers):
    """Generate realistic transaction data."""
    rows = []
    invoice_counter = 536365
    total_days = (END_DATE - START_DATE).days

    for cust in customers:
        n_orders = max(1, int(np.random.normal(cust["avg_orders"], cust["avg_orders"] * 0.3)))
        n_orders = min(n_orders, 80)

        for _ in range(n_orders):
            # Date biased toward recent for active customers
            if np.random.random() < cust["recency_bias"]:
                day_offset = int(np.random.beta(2, 1) * total_days)
            else:
                day_offset = np.random.randint(0, total_days)
            inv_date = START_DATE + timedelta(days=day_offset)
            inv_date += timedelta(hours=np.random.randint(7, 20), minutes=np.random.randint(0, 60))

            invoice_no = str(invoice_counter)
            invoice_counter += 1

            # Items per order
            n_items = max(1, int(np.random.normal(cust["avg_items"], 2)))
            n_items = min(n_items, 30)

            selected_products = random.sample(PRODUCTS, min(n_items, len(PRODUCTS)))

            for stock_code, desc, base_price in selected_products:
                qty = max(1, int(np.random.lognormal(1.0, 0.8)))
                qty = min(qty, 200)
                price = round(base_price * cust["price_mult"] * np.random.uniform(0.9, 1.1), 2)
                price = max(0.10, price)

                rows.append({
                    "InvoiceNo": invoice_no,
                    "StockCode": stock_code,
                    "Description": desc,
                    "Quantity": qty,
                    "InvoiceDate": inv_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "UnitPrice": price,
                    "CustomerID": float(cust["CustomerID"]),
                    "Country": cust["Country"],
                })

    # Add ~5% cancelled invoices (prefix 'C')
    df = pd.DataFrame(rows)
    n_cancel = int(len(df) * 0.02)
    cancel_idx = np.random.choice(df.index, size=n_cancel, replace=False)
    df.loc[cancel_idx, "InvoiceNo"] = "C" + df.loc[cancel_idx, "InvoiceNo"]
    df.loc[cancel_idx, "Quantity"] = -df.loc[cancel_idx, "Quantity"].abs()

    # Add ~3% missing CustomerID
    n_missing = int(len(df) * 0.03)
    missing_idx = np.random.choice(df.index, size=n_missing, replace=False)
    df.loc[missing_idx, "CustomerID"] = np.nan

    # Add some zero-price rows (~1%)
    n_zero = int(len(df) * 0.01)
    zero_idx = np.random.choice(df.index, size=n_zero, replace=False)
    df.loc[zero_idx, "UnitPrice"] = 0.0

    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


if __name__ == "__main__":
    print("Generating customers...")
    customers = generate_customers()
    print(f"  {len(customers)} customer profiles created")

    print("Generating transactions...")
    df = generate_transactions(customers)
    print(f"  {len(df)} transaction rows generated")

    out_dir = os.path.join(os.path.dirname(__file__), "app", "data", "raw")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "online_retail.csv")
    df.to_csv(out_path, index=False)
    print(f"  Saved to {out_path}")
    print(f"\nDataset shape: {df.shape}")
    print(f"Unique customers: {df['CustomerID'].nunique()}")
    print(f"Unique invoices: {df['InvoiceNo'].nunique()}")
    print(f"Date range: {df['InvoiceDate'].min()} - {df['InvoiceDate'].max()}")
    print(f"Countries: {df['Country'].nunique()}")
    print(f"Missing CustomerID: {df['CustomerID'].isna().sum()}")
    print(f"Cancelled invoices: {df[df['InvoiceNo'].str.startswith('C')].shape[0]} rows")
