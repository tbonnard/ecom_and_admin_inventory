from app import db

from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
import datetime

Base = declarative_base()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)
    address = db.relationship('Address', backref=db.backref('user', lazy=True))


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    street_name_number = db.Column(db.String, nullable=False)
    apt = db.Column(db.String, nullable=True)
    street_2 = db.Column(db.String, nullable=True)
    zip_code = db.Column(db.String, nullable=False)
    province = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)


ProductCategory = db.Table('ProductCategory',
                           db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                           db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                           )

ProductCart = db.Table('ProductCart',
                       db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                       db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True)
                       )


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000))
    img_url = db.Column(db.String)
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.Integer, default=1)
    product_stripe_id = db.Column(db.String, nullable=True)
    product_price_stripe_id = db.Column(db.String, nullable=True)

    categories = db.relationship("Category", secondary=ProductCategory, backref="products")


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.name


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    status = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    stripe_session_id = db.Column(db.String, nullable=False)
    stripe_payment_intent = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transaction', lazy=True))


class Order(db.Model):
    __tablename__ = 'order'
    # 1 record per product of a transaction to keep histo of the price at the moment of the transaction
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    transaction = db.relationship('Transaction', backref=db.backref('order', lazy=True))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('order', lazy=True))
    product_price = db.Column(db.Float, nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    stripe_session_id = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart', lazy=True))
    products = db.relationship("Product", secondary=ProductCart, backref="carts")

