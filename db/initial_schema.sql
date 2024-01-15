CREATE TABLE IF NOT EXISTS BrandManager (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    contact_email VARCHAR UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' OR contact_email IS NULL)
);

CREATE TABLE IF NOT EXISTS Brand (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE NOT NULL UNIQUE,
    name VARCHAR UNIQUE NOT NULL UNIQUE,
    brand_manager_id BIGINT NOT NULL,
    acquired_at DATE NOT NULL CHECK (acquired_at <= CURRENT_DATE),
    FOREIGN KEY (brand_manager_id) REFERENCES BrandManager(id) ON UPDATE CASCADE ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS Item (
    id BIGSERIAL PRIMARY KEY,
    product_title VARCHAR CHECK (LENGTH(product_title) >= 3 OR product_title IS NULL),
    brand_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    country_of_sales_id BIGINT,
    unit_price_local_currency FLOAT NOT NULL,
    sales_margin FLOAT CHECK (sales_margin > -1 and sales_margin < 1),
    launched_at DATE CHECK (launched_at <= CURRENT_DATE),
    size VARCHAR NOT NULL CHECK (size IN ('S', 'M', 'L', 'XL')),
    item_type VARCHAR CHECK (item_type IN ('A', 'B', 'C', 'D')),
    in_stock BOOLEAN NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES Brand(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES Category(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (country_of_sales_id) REFERENCES Country(id) ON UPDATE CASCADE ON DELETE SET NULL,
);


CREATE TABLE IF NOT EXISTS Category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS ItemCategory (
    item_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Item(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Category(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (item_id, category_id)
);


CREATE TABLE IF NOT EXISTS Region (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS Country (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    currency VARCHAR(3) NOT NULL,
    exchange_rate_eu FLOAT CHECK (exchange_rate_eu > 0),
    region_id BIGINT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Region(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS City (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    country_id BIGINT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES Country(id) ON UPDATE CASCADE ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS Marketplace (
    id BIGSERIAL PRIMARY KEY,
    country_id BIGINT NOT NULL,
    url_domain VARCHAR NOT NULL CHECK (url_domain LIKE 'www.%'),
    FOREIGN KEY (country_id) REFERENCES Country(id) ON UPDATE CASCADE ON DELETE SET NULL
        -- so orders from any marketplace can still be placed and sent to a different country
);

CREATE TABLE IF NOT EXISTS SalesOrder (
    id BIGSERIAL PRIMARY KEY,
    buyer_id BIGINT NOT NULL,
    shipping_city_id BIGINT NOT NULL,
    shipping_country_id BIGINT, -- trade off between redundancy and performance
    marketplace_id BIGINT,
    order_date DATE,
    total_amount FLOAT CHECK (total_amount > 0),
    FOREIGN KEY (buyer_id) REFERENCES Buyer(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (shipping_city_id) REFERENCES City(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (shipping_country_id) REFERENCES Country(id) ON UPDATE CASCADE ON DELETE RESTRICT, -- restrict deletion of country mock_data for analytics purposes
    FOREIGN KEY (marketplace_id) REFERENCES Marketplace(id) ON UPDATE CASCADE ON DELETE NULL
);

CREATE TABLE IF NOT EXISTS ItemOrdered (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    quantity INTEGER CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES SalesOrder(id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS MarketplaceUser (
    id BIGSERIAL PRIMARY KEY,
    user_name VARCHAR UNIQUE,
    full_name VARCHAR,
    email VARCHAR NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    marketplace_id BIGINT,
    last_updated DATE,
    FOREIGN KEY (marketplace_id) REFERENCES Marketplace(id) ON UPDATE CASCADE ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS Buyer (
    id BIGSERIAL PRIMARY KEY,
    marketplace_user_id BIGINT NOT NULL,
    billing_city_id BIGINT,
    tax_id VARCHAR,
    FOREIGN KEY (marketplace_user_id) REFERENCES MarketplaceUser(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (billing_city_id) REFERENCES City(id) ON UPDATE CASCADE ON DELETE SET NULL
);




CREATE INDEX idx_item_brand ON Item (brand_id);

CREATE INDEX idx_salesorder_date ON SalesOrder (order_date);

-- indexed for item_ordered to optimize the retrieve of data for SalesOrder operations (e.g. get sales per brand, get sales per item)
CREATE INDEX idx_itemordered_item ON ItemOrdered (item_id);
CREATE INDEX idx_itemordered_order ON ItemOrdered (order_id);

CREATE INDEX idx_salesorder_shipping_country ON SalesOrder (shipping_country_id);
