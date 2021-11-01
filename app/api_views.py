from flask import Blueprint, jsonify, request
from .models import User, Transaction, Order, Cart, Product, Address
from .api_schemas import UserSchema, ProductSchema, CartSchema, TransactionSchema, OrderSchema, AddressSchema
from flask_login import current_user

from app import db

api = Blueprint('api', __name__)


@api.route("/api/get_client", methods=['GET'])
def get_current_client():
    if current_user.is_authenticated:
        schema = UserSchema()
        client_to_return = current_user
        return schema.dump(client_to_return)
    return jsonify({"status": "no user"}), 200


@api.route("/api/get_address/<int:client_id>", methods=['GET', "POST", "PUT"])
def get_address(client_id):
    if request.method == 'POST':
        if Address.query.get(User.query.get(client_id).address_id):
            address_to_delete = Address.query.get(User.query.get(client_id).address_id)
            db.session.delete(address_to_delete)
        new_address = Address(street_name_number=request.form['street_name_number'], apt=request.form['apt'],
                              street_2=request.form['street_2'], zip_code=request.form['zip_code'],
                              province=request.form['province'], country=request.form['country'])
        user = User.query.get(client_id)
        db.session.add(new_address)
        user.address = new_address
        db.session.commit()
        return jsonify(response={"success": "Successfully created the address."}), 200
    if request.method == 'PUT':
        address_to_update = Address.query.get(User.query.get(client_id).address_id)
        address_to_update.street_name_number = request.form['street_name_number']
        address_to_update.apt = request.form['apt']
        address_to_update.street_2 = request.form['street_2']
        address_to_update.zip_code = request.form['zip_code']
        address_to_update.province = request.form['province']
        address_to_update.country = request.form['country']
        db.session.commit()
        return jsonify(response={"success": "Successfully edited the address."}), 200
    else:
        schema = AddressSchema()
        address_to_return = Address.query.get(User.query.get(client_id).address_id)
        return schema.dump(address_to_return)


@api.route("/api/get_products", methods=['GET'])
def get_products():
    schema = ProductSchema(many=True)
    products_to_return = Product.query.all()
    if request.args.get("id"):
        products_to_return = Product.query.filter_by(id=request.args.get("id"))
    return jsonify(schema.dump(products_to_return))


@api.route("/api/get_transactions/<int:client_id>", methods=['GET'])
def get_transactions(client_id):
    schema = TransactionSchema(many=True)
    transactions_to_return = Transaction.query.filter_by(user=User.query.get(client_id))
    result = schema.dump(transactions_to_return)
    return jsonify(result)


@api.route("/api/get_orders", methods=['GET'])
def get_order():
    schema = OrderSchema(many=True)
    orders_to_return = Order.query.all()
    if request.args.get("id"):
        orders_to_return = Order.query.filter_by(transaction=Transaction.query.get(request.args.get("id")))
    return jsonify(schema.dump(orders_to_return))


@api.route("/api/get_cart/<int:client_id>", methods=['GET'])
def get_cart(client_id):
    if current_user.is_authenticated:
        cart_to_return = Cart.query.filter_by(user=User.query.get(client_id)).first()
        if cart_to_return:
            schema = CartSchema()
            return schema.dump(cart_to_return)
        return jsonify({"status": "no cart"}), 200
    return jsonify({"status": "no user"}), 200


@api.route("/api/add_to_cart/<int:client_id>", methods=['POST'])
def create_cart(client_id):
    cart_to_update = Cart(user=User.query.get(client_id))
    db.session.add(cart_to_update)
    db.session.commit(cart_to_update)
    return jsonify({"success": "Cart successfully created."}), 200


@api.route("/api/add_to_cart", methods=['PUT'])
def add_to_cart():
    product_to_add = Product.query.get(request.args.get('product_id'))
    if product_to_add and product_to_add.quantity != 0:
        cart_to_update = Cart.query.filter_by(user=User.query.get(request.args.get('client_id'))).first()
        cart_to_update.products.append(product_to_add)
        db.session.commit()
        return jsonify({"success": "Item successfully added."}), 200
    else:
        return jsonify({"not possible": "Item not available"}), 200


@api.route("/api/delete_cart_item/<int:client_id>", methods=['DELETE'])
def delete_cart_item(client_id):
    cart_to_update = Cart.query.filter_by(user=User.query.get(client_id)).first()
    cart_to_update.products.remove(Product.query.get(request.args.get('product_id')))
    db.session.commit()
    return jsonify({"success": "Item successfully removed."}), 200
