import csv
import random
from faker import Faker

fake = Faker()

# Mock mock_data for each table
brand_managers = [{"id": i, "full_name": fake.name(), "contact_email": fake.email()} for i in range(1, 11)]

brands = [{"id": i, "code": fake.bothify(text='???'), "name": fake.company(),
           "brand_manager_id": random.randint(1, 10), "acquired_at": fake.date()} for i in range(1, 11)]

items = [{"id": i, "product_title": fake.catch_phrase(), "brand_id": random.randint(1, 10),
          "category_id": random.randint(1, 5), "country_of_sales_id": random.randint(1, 5),
          "unit_price_local_currency": round(random.uniform(10, 1000), 2),
          "sales_margin": round(random.uniform(-0.99, 0.99), 2),
          "size": random.choice(['S', 'M', 'L', 'XL']), "item_type": random.choice(['A', 'B', 'C', 'D']),
          "launched_at": fake.date(), "in_stock": fake.boolean()} for i in range(1, 21)]

categories = [{"id": i, "name": fake.word()} for i in range(1, 6)]

countries = [{"id": i, "name": fake.country(), "currency": fake.currency_code(),
              "exchange_rate_eu": round(random.uniform(0.5, 2), 2), "region_id": random.randint(1, 3)} for i in
             range(1, 6)]

regions = [{"id": i, "name": fake.city_suffix()} for i in range(1, 4)]

cities = [{"id": i, "name": fake.city(), "country_id": random.randint(1, 5)} for i in range(1, 11)]

marketplaces = [{"id": i, "country_id": random.randint(1, 5), "url_domain": 'www.' + fake.domain_name()} for i in
                range(1, 11)]

users = [{"id": i, "user_name": fake.user_name(), "full_name": fake.name(), "email": fake.email(),
          "last_updated": fake.date()} for i in range(1, 11)]

buyers = [{"id": i, "user_id": random.randint(1, 10), "billing_city_id": random.randint(1, 10),
           "tax_id": fake.bothify(text='??-########')} for i in range(1, 11)]

sales_orders = [{"id": i, "buyer_id": random.randint(1, 10), "shipping_country_id": random.randint(1, 5),
                 "shipping_city_id": random.randint(1, 10), "marketplace_id": random.randint(1, 10),
                 "order_date": fake.date(), "total_amount": round(random.uniform(100, 10000), 2)} for i in range(1, 21)]

item_ordered = [{"id": i, "order_id": random.randint(1, 20), "item_id": random.randint(1, 20),
                 "quantity": random.randint(1, 100)} for i in range(1, 41)]

# Paths for CSV files
brand_manager_path = 'mock_data/brand_manager.csv'
brand_path = 'mock_data/brand.csv'
item_path = 'mock_data/item.csv'
category_path = 'mock_data/category.csv'
country_path = 'mock_data/country.csv'
region_path = 'mock_data/region.csv'
city_path = 'mock_data/city.csv'
marketplace_path = 'mock_data/marketplace.csv'
user_path = 'mock_data/user.csv'
buyer_path = 'mock_data/buyer.csv'
sales_order_path = 'mock_data/sales_order.csv'
item_ordered_path = 'mock_data/item_ordered.csv'


def write_to_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Write mock mock_data to CSV files
write_to_csv(brand_manager_path, brand_managers, ["id", "full_name", "contact_email"])
write_to_csv(brand_path, brands, ["id", "code", "name", "brand_manager_id", "acquired_at"])
write_to_csv(item_path, items, ["id", "product_title", "brand_id", "category_id", "country_of_sales_id",
                                "unit_price_local_currency", "sales_margin", "size", "item_type",
                                "launched_at", "in_stock"])
write_to_csv(category_path, categories, ["id", "name"])
write_to_csv(country_path, countries, ["id", "name", "currency", "exchange_rate_eu", "region_id"])
write_to_csv(region_path, regions, ["id", "name"])
write_to_csv(city_path, cities, ["id", "name", "country_id"])
write_to_csv(marketplace_path, marketplaces, ["id", "country_id", "url_domain"])
write_to_csv(user_path, users, ["id", "user_name", "full_name", "email", "last_updated"])
write_to_csv(buyer_path, buyers, ["id", "user_id", "billing_city_id", "tax_id"])
write_to_csv(sales_order_path, sales_orders, ["id", "buyer_id", "shipping_country_id", "shipping_city_id",
                                              "marketplace_id", "order_date", "total_amount"])
write_to_csv(item_ordered_path, item_ordered, ["id", "order_id", "item_id", "quantity"])

# Returning paths of all generated CSV files
(brand_manager_path, brand_path, item_path, category_path, country_path, region_path, city_path, marketplace_path, user_path, buyer_path, sales_order_path, item_ordered_path)
