from flask import Flask, render_template, abort, jsonify, Blueprint, request, url_for, redirect, flash, session
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app.models.brand import Brand
from app.models.marketplace_user import MarketplaceUser
from app.models.buyer import Buyer
from app.models.brand_manager import BrandManager
from app.models.category import Category
from app.models.marketplace import Marketplace
from app.models.sales_order import SalesOrder
from app.models.item import Item
from app.models.item_ordered import ItemOrdered
from app.models.city import City
from app.models.country import Country
from app.models.region import Region
from app.models.item_category import ItemCategory

from app.forms.forms import BrandManagerSignupForm, BrandManagerLogInForm
from werkzeug.security import generate_password_hash, check_password_hash


from .database import db

bp = Blueprint('main_bp', __name__)

model_mapping = {
    'item': Item,
    'brand': Brand,
    'category': Category,
    'user': MarketplaceUser,
    'buyer': Buyer,
    'brand_manager': BrandManager,
    'marketplace': Marketplace,
    'sales_order': SalesOrder,
    'item_ordered': ItemOrdered,
    'city': City,
    'country': Country,
    'region': Region
}


@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = BrandManagerSignupForm(request.form)
    if request.method == 'POST' and form.validate():
        existing_user = BrandManager.query.filter_by(contact_email=form.email.data).first()
        if existing_user is None:
            hashed_password = generate_password_hash(form.password.data)
            new_user = BrandManager(
                full_name=form.full_name.data,
                contact_email=form.email.data,
                password_hash=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful. You can now log in.', 'success')
            return redirect(url_for('brand_manager.login'))
        else:
            flash('Email already exists.', 'error')

    return render_template('sign_up.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = BrandManagerLogInForm()
    if form.validate_on_submit():
        user = BrandManager.query.filter_by(contact_email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):

            session['user_id'] = user.id  # example
            return redirect(url_for('index'))  # Redirect to a dashboard or home page
        else:
            flash('Invalid email or password', 'error')

    return render_template('log_in.html', form=form)

@bp.route('/brand_managers/<int:brand_manager_id>/items')
def get_items_by_brand_manager(brand_manager_id):
    items_with_brands = (db.session.query(Item.id, Item.product_title, Item.launched_at, Brand.name)
                         .join(Brand, Item.brand_id == Brand.id)
                         .filter(Brand.brand_manager_id == brand_manager_id)
                         .all())

    if not items_with_brands:
        abort(404, description="No items found for this brand manager.")

    items_data = []
    for item_id, product_title, launched_at, brand_name in items_with_brands:
        item_data = {
            'item_id': item_id,
            'product_title': product_title,
            'launched_at': launched_at,
            'brand_id': brand_name,
        }
        items_data.append(item_data)

    return render_template('items_by_brand_manager.html', items=items_data)


@bp.route('/sales/<int:year>/<int:month>')
def get_sales_by_year_month(year, month):
    sales_by_date = (db.session.query(SalesOrder)
                     .filter(func.extract('year', SalesOrder.order_date) == str(year),
                             func.extract('month', SalesOrder.order_date) == str(month))
                     .with_entities(SalesOrder.id, SalesOrder.order_date)
                     .order_by(SalesOrder.order_date)
                     .all())

    if not sales_by_date:
        abort(404, description="No sales found for this year and month.")

    sales_data = []
    for sales_id, order_date in sales_by_date:
        sale_data = {
            'order_id': sales_id,
            'order_date': order_date
        }
        sales_data.append(sale_data)

    return render_template('sales_by_year_month.html', year=year, month=month, sales=sales_data)


@bp.route('/sales/total_per_date')
def get_total_sales_per_date():
    total_sales_per_date = (db.session.query(func.count(SalesOrder.id), SalesOrder.order_date)
                            .group_by(SalesOrder.order_date)
                            .order_by(SalesOrder.order_date.desc())
                            .all())

    if not total_sales_per_date:
        abort(404, description="No sales found.")

    sales_data = []
    for count_sales, date in total_sales_per_date:
        sale_data = {
            'total_sales': count_sales,
            'date': date
        }
        sales_data.append(sale_data)

    return render_template('total_sales_per_date.html', sales=sales_data)


@bp.route('/brands/sales/<int:year>/<int:month>')
def get_items_sold_per_brand_by_year_month(year, month):
    sales_by_brand = (db.session.query(Brand.name,
                                       Brand.code,
                                       func.count(ItemOrdered.id).label('sales_count'),
                                       func.sum(Item.sales_margin).label('total_sales_margin'))
                      .join(Item, Brand.id == Item.brand_id)
                      .join(ItemOrdered, Item.id == ItemOrdered.item_id)
                      .join(SalesOrder, ItemOrdered.order_id == SalesOrder.id)
                      .filter(func.extract('year', SalesOrder.order_date) == str(year),
                              func.extract('month', SalesOrder.order_date) == str(month))
                      .group_by(Brand.name, Brand.code)
                      .all())

    if not sales_by_brand:
        abort(404, description="No sales found.")

    sales_data = []
    for brand, brand_code, sales_count, margin_sum in sales_by_brand:
        sale_data = {
            'brand': brand,
            'brand_code': brand_code,
            'sales_count': sales_count,
            'total_margin': margin_sum,
        }
        sales_data.append(sale_data)

    return render_template('sales_per_brand_by_year_month.html', year=year, month=month, sales=sales_data)


@bp.route('/add_brand', methods=['GET', 'POST'])
def add_brand():
    if request.method == 'POST':
        if not request.json:
            abort(400, description="No data provided.")

        name = request.json.get('name')
        code = request.json.get('code').upper()
        brand_manager_id = request.json.get('brand_manager_id')
        acquired_at = request.json.get('acquired_at',
                                       datetime.now().strftime("%Y-%m-%d"))  # Default to current date if not provided

        if not name or not code:
            abort(400, description="Name and code are required for the brand.")

        # Check if already exists
        if Brand.query.filter((Brand.name.upper() == name.upper()) | (Brand.code == code)).first():
            abort(400, description="Brand already exists.")

        new_brand = Brand(
            name=name,
            code=code,
            brand_manager_id=brand_manager_id,
            acquired_at=acquired_at
        )

        db.session.add(new_brand)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=str(e))

        return jsonify({'message': 'Brand added successfully.'}), 201

    return render_template('add_brand.html')
@bp.route('/update_brand_manager', methods=['GET', 'POST'])
def update_brand_manager():
    if request.method == 'POST':
        if not request.json or 'brand_name' not in request.json or 'brand_manager_full_name' not in request.json:
            abort(400, description="Brand name and Brand Manager's full name are required.")

        brand_name = request.json['brand_name']
        brand_manager_full_name = request.json['brand_manager_full_name']

        # Find the BrandManager by full_name
        brand_manager = BrandManager.query.filter_by(full_name=brand_manager_full_name).first()
        if not brand_manager:
            abort(404, description="Brand Manager not found.")

        # Find the Brand by name
        brand = Brand.query.filter_by(name=brand_name).first()
        if not brand:
            abort(404, description="Brand not found.")

        # Update the Brand's brand_manager_id
        brand.brand_manager_id = brand_manager.id

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=str(e))

        return jsonify({'message': 'Brand Manager updated successfully'}), 200

    return render_template('update_brand_manager.html')

@bp.route('/delete_unsold_items')
def delete_unsold_items():
    # Calculate the date 9 months ago --> fixed business requirement to consider an item as unsold
    nine_months_ago = datetime.now() - timedelta(days=9*31)

    # Find items that have been sold in the last 9 months
    sold_item_ids = db.session.query(ItemOrdered.item_id).join(SalesOrder).filter(SalesOrder.order_date >= nine_months_ago).distinct()

    # Find items that have not been sold in the last 9 months
    unsold_items = Item.query.filter(~Item.id.in_(sold_item_ids)).all()

    if not unsold_items:
        return jsonify({'message': 'No unsold items found'}), 404

    try:
        for item in unsold_items:
            db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

    return jsonify({'message': f'{len(unsold_items)} items deleted successfully'}), 200
