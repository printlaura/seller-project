### SE 05 - Relational Databases

# Seller Project

## Description
This project was thought as if it was developed for an e-Commerce aggregator called Seller Project. An e-commerce aggregator is a business that acquires and consolidates multiple smaller online retailers or brands, typically operating in the same marketplaces (e.g. Amazon.pl, Amazon.com, Amazon.es, Shopify, Walmart.com).

So far, Seller Project has already acquired several brands. 

## Disclaimer
The project was built to showcase Relational Databases development learnings, so all other aspects of the development of the Application should not be considered as finished or fully handled.
For aspects of the development that are not assessed in this module (e.g. templating, scripting for the generation of random data, guidelines for this documentation, etc.), ChatGPT has been used as a helpful resource.

## Table of Contents

1. [High level data model](#high-level-business-explanation-for-better-understanding-of-the-data-model)
1. [ERD](#ERD)
1. [Use Cases](#use-cases)
1. [Set up the development environment](#setting-up-the-development-environment)
   1. [Prerequisites](#prerequisites)
   1. [Installation](#installation)
   1. [Running the app](#running-the-application)
1. [Contribution list](#contribution-list)

## High level business explanation for better understanding of the data model
- **Brands and Brand Managers**:
  - Each `Brand` sells one or more `Items`.
  - Each Brand is overseen by one `Brand Managers`.
  - `Brand Managers`can oversee several Brands.

- **Items and Categories**:
  - `Items` represent individual products.
  - Items are categorized into `Categories`. An item can belong to multiple categories, and each category can contain multiple items.

- **Geographical Structure**:
  - The business operates in different `Countries`, with specific **currencies**.
  - `Countries` are grouped into `Regions`.
  - `Cities` within countries are also tracked.

- **Marketplaces and Sales**:
  - `Marketplaces` operate in specific `Countries` and are identified by a unique domain URL.
  - The database tracks `Sales Orders`.
  - A Sales Order may consist of different `Items` sold.

- **Users and Buyers**:
  - `Marketplace Users` represent a user account created in a Marketplace.
  - When a Marketplace User performs a purchase, it becomes a `Buyer`. 


## Entity-Relationship Model
![ERD](ERD.png)


## Use Cases
Use cases handled in this project:
- **Get all Items by Brand Manager**: get all records from Item table whose `brand_id` belongs to a specific `brand_manager_id`
- **Get Sales Orders by date**: get all Sales Orders that took place in a specific year & month.
- **Get Sales Orders per date**: get the count of Sales Orders per each date.
- **Get Items sold per brand by date**: get the count of Items sold and the total sales margin earned per each brand, for a specific year & month.
- **Add Brand**: add a newly acquired Brand to the database.
- **Update Brand Manager**: change the Brand Manager for a Brand. For example, for a scenario where the original Brand Manager quits and is replaced by a new one.
- **Delete unsold items**: delete from the database all items that haven't sold any units in the last 9 months..

## Setting Up the Development Environment


### Prerequisites
- **Python**: Version 3.10 or higher
- **PostgreSQL Database**

### Installation

1. **Set up a [PostgreSQL Database](https://www.postgresql.org/docs/current/tutorial-install.html)**

   - Ensure to take note of the connection URL to the database (e.g.: postgresql://johndoe:somepassword@localhost:5432/mydb)

2. **Clone the repository:** 

```shell
git clone https://github.com/printlaura/seller-project.git
```

3. **Create a Virtual Environment:**

macOS/Linux
```shell
python3 -m venv venv
```
Windows
```shell
python -m venv venv
```

4. **Activate the Virtual Environment**

macOS/Linux
```shell
source venv/bin/activate

```
Windows
```shell
.\venv\Scripts\activate
```

5. Navigate to the project directory

6. **Install dependencies:** 

```shell
pip3 install -r requirements.txt
```

7. Create a .env file: Generate a .env file in the project directory and add the following variables: 

```shell
SECRET_KEY=<secret_key>
DATABASE_URI=<database_connection_url_from_step_1>
```

8. **Initial database setup:** 

```shell 
create-db
```

9. **Initialize the migrations directory** (only the first time):

```shell
 flask db init
```

10. **To create a new migration** after a model change: 

```shell
flask db migrate -m "message describing the migration"
```

11. **To apply the migration** to the database:

```shell
 flask db upgrade
```

   - The `create_db` command used for creating database tables might overlap with Flask-Migrate's functionality. Flask-Migrate handles the creation and management of tables based on the migration scripts. 
   - `create_db` can be used for initial database setup, but for schema changes, prefer using Flask-Migrate's `migrate` and `upgrade` commands for more controlled and versioned database alterations.
12. (Optional) Navigate to the root directory and run `python3 scripts/generate_mock_data.py` to generate random data for testing purposes.

13. (Optional) Save Database backup:

```shell
  python backup_db.py
```

## Running the Application

1. Start the server: `python3 run.py` *for macOS/Linux*
2. Access the application at: `http://127.0.0.1:5000/`

## Contribution List
SE_05 Relational Databases contributions:

 - Application of the concepts of relational databases to the project
 - **Design** and implementation of the database schema, including the definition of tables, columns, primary and foreign keys, and relationships
 - **Normalization** of the database schema (1N, 2N, 3N)
- Use of **indexes** (and evaluation of trade off)
 - use of **constraints** for data integrity enforce
 - Use of basic SQL statements
 - Use `SQLAlchemy` ORM library and theoretical implementation of `Alembic`, a database migration tool
 - User passwords hashing with `bcrypt`
 - **Prevent SQL injections**: in SQLAlchemy's `filter()` and `filter_by()` functions, arguments are automatically escaped
- **Database backup**: `backup_db` script for manual backup in `/db/backups` dir.

### Missing:
- Securing the database with implementations like access controls, definition of user roles and prevention of client-side SQL injection.
- Automate database backup

