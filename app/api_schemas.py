from app import ma
from .models import User, Product, Category, Transaction, Order, Cart, Address


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    type = ma.auto_field()
    email = ma.auto_field()
    status = ma.auto_field()


class AddressSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Address

    id = ma.auto_field()
    street_name_number = ma.auto_field()
    apt = ma.auto_field()
    street_2 = ma.auto_field()
    zip_code = ma.auto_field()
    province = ma.auto_field()
    country = ma.auto_field()


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product

    id = ma.auto_field()
    name = ma.auto_field()
    sku = ma.auto_field()
    price = ma.auto_field()
    cost = ma.auto_field()
    description = ma.auto_field()
    img_url = ma.auto_field()
    quantity = ma.auto_field()
    status = ma.auto_field()
    categories = ma.auto_field()


class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order

    id = ma.auto_field()
    transaction_id = ma.auto_field()
    transaction = ma.auto_field()
    product_id = ma.auto_field()
    product = ma.auto_field()
    product_price = ma.auto_field()


class TransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction

    id = ma.auto_field()
    transaction_date = ma.auto_field()
    status = ma.auto_field()
    total_price = ma.auto_field()
    user_id = ma.auto_field()
    user = ma.auto_field()


class CartSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cart

    id = ma.auto_field()
    user_id = ma.auto_field()
    products = ma.auto_field()
    user = ma.auto_field()
