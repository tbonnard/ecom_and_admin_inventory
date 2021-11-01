from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import current_user
import os
from jinja2 import environment

from .forms import AddressForm
from .models import Address, User, Cart, Product, Transaction, Category, Order
from app import db

ecom = Blueprint('ecom', __name__)

import stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)

environment.DEFAULT_FILTERS['datetime_format'] = datetime_format


@ecom.route("/", methods=['GET'])
def index():
    all_categories = Category.query.all()
    if request.args.get('cat_id'):
        if request.args.get('cat_id') == '0':
            all_products = Product.query.all()
        else:
            category_selected = Category.query.get(request.args.get('cat_id'))
            all_products_list = Product.query.all()
            all_products = []
            for i in all_products_list:
                if category_selected in i.categories:
                    all_products.append(i)
    else:
        all_products = Product.query.all()
    return render_template("ecom/home.html", products=all_products, categories=all_categories)


@ecom.route("/profile", methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        if Address.query.all():
            if Address.query.get(User.query.get(current_user.id).address_id):
                user_address = Address.query.get(User.query.get(current_user.id).address_id)
                form = AddressForm(obj=user_address)
            else:
                user_address = None
                form = AddressForm()
        else:
            user_address = None
            form = AddressForm()
        all_user_transactions = Transaction.query.filter_by(user=current_user)
        if form.validate_on_submit():
            if not user_address:
                new_address = Address(street_name_number=form.street_name_number.data, apt=form.apt.data,
                                      street_2=form.street_2.data, zip_code=form.zip_code.data,
                                      province=form.province.data, country=form.country.data)
                user = User.query.get(current_user.id)
                db.session.add(new_address)
                user.address = new_address
            else:
                user_address.street_name_number=form.street_name_number.data
                user_address.apt = form.apt.data
                user_address.street_2 = form.street_2.data
                user_address.zip_code = form.zip_code.data
                user_address.province = form.province.data
                user_address.country = form.country.data
            db.session.commit()
            return redirect(url_for('ecom.profile'))
        return render_template("ecom/profile.html", address=user_address, form=form, transactions=all_user_transactions)
    return redirect(url_for('auth.login_ecom'))


@ecom.route("/cart")
def cart():
    if current_user.is_authenticated:
        user_cart = Cart.query.filter_by(user_id=current_user.id).first()
        total_price=0
        if user_cart:
            for i in user_cart.products:
                total_price+=i.price
        return render_template("ecom/cart_ecom.html", cart=user_cart, total_price=total_price)
    return render_template("ecom/cart_ecom.html", cart=None, total_price=None)


@ecom.route("/add_item")
def add_item():
    if current_user.is_authenticated:
        user_cart = Cart.query.filter_by(user_id=current_user.id).first()
        product_to_add = Product.query.get(request.args.get('product_id'))
        if product_to_add and product_to_add.quantity > 0:
            if not user_cart:
                user_cart=Cart(user_id=current_user.id)
            user_cart.products.append(product_to_add)
        db.session.commit()
        if user_cart and request.args.get('buy'):
            return redirect(url_for('ecom.cart'))
        return redirect(url_for('ecom.index'))
    return redirect(url_for('auth.login_ecom'))


@ecom.route("/delete_item")
def delete_item():
    if current_user.is_authenticated:
        user_cart = Cart.query.filter_by(user_id=current_user.id).first()
        user_cart.products.remove(Product.query.get(request.args.get('product_id')))
        db.session.commit()
        return redirect(url_for('ecom.cart'))
    return redirect(url_for('auth.login_ecom'))


@ecom.route("/thank_you")
def thanks():
    if current_user.is_authenticated:
        user_cart = Cart.query.filter_by(user_id=current_user.id).first()
        if user_cart:
            cart_id = Cart.query.filter_by(user_id=current_user.id).first().id
            session_status = stripe.checkout.Session.retrieve(user_cart.stripe_session_id)
            print(session_status)
            if session_status.payment_status == 'paid':
                products_to_buy = Cart.query.get(cart_id).products
                total_price_transaction = 0
                for i in products_to_buy:
                    total_price_transaction += i.price
                new_transaction = Transaction(status=1, total_price=total_price_transaction, user=current_user,
                                              stripe_session_id=session_status.id,
                                              stripe_payment_intent=session_status.payment_intent)
                db.session.add(new_transaction)
                for i in products_to_buy:
                    new_order = Order(transaction=new_transaction, product=i, product_price=i.price)
                    db.session.add(new_order)
                    i.quantity -= 1
                cart_to_update = Cart.query.get(cart_id)
                db.session.delete(cart_to_update)
                db.session.commit()
                return render_template("ecom/thank_you.html")
            return redirect(url_for('ecom.cart'))
        return redirect(url_for('ecom.index'))
    return redirect(url_for('ecom.index'))


@ecom.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    user_cart = Cart.query.filter_by(user_id=current_user.id).first()
    items = []
    for i in user_cart.products:
        dict = {'price': i.product_price_stripe_id, 'quantity': 1}
        items.append(dict)
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url=request.host_url + 'thank_you',
            cancel_url=request.host_url + 'cart',
        )
    except Exception as e:
        return str(e)
    else:
        user_cart.stripe_session_id = checkout_session['id']
        db.session.commit()
    return redirect(checkout_session.url, code=303)

