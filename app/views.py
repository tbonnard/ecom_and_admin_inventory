from app import db

from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import login_required, current_user
import os

from .forms import CategoryForm, ProductForm
from .models import Product, Category, Order, Transaction, Cart, User
from .login_views import admin_only

main = Blueprint('main', __name__)

import stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


# ROUTES
@main.route("/admin", methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.is_authenticated and current_user.type != "User":
        return redirect(url_for('ecom.index'))
    all_users = User.query.filter_by(type='User')
    return render_template("index.html", users=all_users)


@main.route('/admin/category', methods=['GET', 'POST'])
@login_required
@admin_only
def category():
    all_categories = Category.query.all()
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('main.category'))
    return render_template("category.html", form=form, categories=all_categories)


@main.route('/admin/product', methods=['GET', 'POST'])
@login_required
@admin_only
def product():
    all_products = Product.query.all()
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, sku=form.sku.data, price=form.price.data,
                              description=form.description.data, quantity=form.quantity.data,
                              img_url=form.img_url.data, cost=form.cost.data, categories=form.category.data)
        db.session.add(new_product)
        new_prod_stripe = stripe.Product.create(name=new_product.name)
        new_product.product_stripe_id = new_prod_stripe['id']
        new_prod_price = new_prod_stripe['id']
        new_prod_price_stripe = stripe.Price.create(
            unit_amount=int((new_product.price)*100),
            currency="cad",
            product=new_prod_price,
        )
        new_product.product_price_stripe_id = new_prod_price_stripe['id']
        db.session.commit()
        return redirect(url_for('main.product'))
    return render_template("product.html", form=form, products=all_products)


@main.route('/admin/product_edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def product_edit(product_id):
    product_to_edit = Product.query.get(product_id)
    if product_to_edit:
        form = ProductForm(obj=product_to_edit, category=product_to_edit.categories)
        if form.validate_on_submit():
            product_to_edit.price = form.price.data
            product_to_edit.name = form.name.data
            product_to_edit.description = form.description.data
            product_to_edit.sku = form.sku.data
            product_to_edit.img_url = form.img_url.data
            product_to_edit.quantity = form.quantity.data
            product_to_edit.categories = form.category.data
            db.session.commit()
            return redirect(url_for('main.product'))
        return render_template("product_edit.html", product=product_to_edit, form=form)
    return redirect(url_for('main.product'))


@main.route("/admin/cart", methods=['GET', 'POST'])
@login_required
@admin_only
def cart():
    client_cart = Cart.query.filter_by(user=current_user).first()
    all_carts = Cart.query.all()
    return render_template("cart.html", carts=all_carts, cart=client_cart)


@main.route("/admin/add_cart", methods=['POST'])
@login_required
@admin_only
def add_to_cart():
    cart_to_update = Cart.query.filter_by(user=current_user).first()
    if not cart_to_update:
        cart_to_update = Cart(user=current_user)
    product_to_add = Product.query.get(request.args.get('product_id'))
    if product_to_add and product_to_add.quantity > 0:
        cart_to_update.products.append(product_to_add)
        db.session.commit()
        return redirect(url_for('main.cart'))
    return redirect(url_for('main.product', product_id=product_to_add))


@main.route('/admin/delete_product_cart', methods=["GET",'POST'])
@login_required
@admin_only
def delete_product_cart():
    cart_to_update = Cart.query.get(request.args.get("cart_id"))
    product_to_remove = Product.query.get(request.args.get("product_id"))
    cart_to_update.products.remove(product_to_remove)
    if len(cart_to_update.products) == 0:
        db.session.delete(cart_to_update)
    db.session.commit()
    return redirect(url_for('main.cart'))


@main.route('/admin/buy', methods=['GET', 'POST'])
@login_required
@admin_only
def buy():
    cart_id = request.args.get('cart_id')
    products_to_buy = Cart.query.get(cart_id).products
    total_price_transaction = 0
    for i in products_to_buy:
        total_price_transaction += i.price
    new_transaction = Transaction(status=1, total_price=total_price_transaction, user=current_user)
    db.session.add(new_transaction)
    for i in products_to_buy:
        new_order = Order(transaction=new_transaction, product=i, product_price=i.price)
        db.session.add(new_order)
        i.quantity -= 1
    cart_to_update = Cart.query.get(cart_id)
    db.session.delete(cart_to_update)
    db.session.commit()
    return redirect(url_for('main.home'))


@main.route('/admin/client', methods=["GET", 'POST'])
@login_required
@admin_only
def client():
    all_clients = User.query.all()
    return render_template("client.html", clients=all_clients)


@main.route("/admin/order", methods=['GET', 'POST'])
@login_required
@admin_only
def order():
    all_orders = Order.query.all()
    return render_template("order.html", orders=all_orders)


@main.route("/admin/transaction", methods=['GET', 'POST'])
@login_required
@admin_only
def transaction():
    all_transactions = Transaction.query.all()
    return render_template("transaction.html", transactions=all_transactions)
