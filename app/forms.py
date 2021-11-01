from app.models import Category

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, URL, Optional
from wtforms.fields.html5 import EmailField, URLField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={'placeholder': "Your first name"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={'placeholder': "Your last name"})
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': "Your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': "Your password"})
    submit = SubmitField('Confirm')


class UserLoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': "Your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': "Your password"})
    submit = SubmitField('Confirm')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={'placeholder': "Category name"})
    submit = SubmitField('Confirm')


def get_all_categories():
    return Category.query


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={'placeholder': "Product name"})
    sku = StringField('Sku', validators=[DataRequired()], render_kw={'placeholder': "SKU ID"})
    price = FloatField('Price', validators=[DataRequired()], render_kw={'placeholder': "Price of the product"})
    cost = FloatField('Cost', validators=[DataRequired()], render_kw={'placeholder': "Cost of the product"})
    description = StringField('Description', validators=[Optional(strip_whitespace=True)], render_kw={'placeholder': "Description of the product"})
    img_url = URLField('Image URL of the product', validators=[Optional(strip_whitespace=True), URL()],
                       render_kw={'placeholder': "Image URL of the product"})
    status = IntegerField('Status', validators=[Optional(strip_whitespace=True)], render_kw={'placeholder': "Status of the product"})
    quantity = IntegerField('Quantity', validators=[Optional(strip_whitespace=True)], render_kw={'placeholder': "Available quantity"})
    category = QuerySelectMultipleField('Category', query_factory=get_all_categories)
    submit = SubmitField('Confirm')


class AddressForm(FlaskForm):
    street_name_number = StringField('Street name and number', validators=[DataRequired()], render_kw={'placeholder': "Street name and number"})
    apt = StringField('apt', render_kw={'placeholder': "Apt number"})
    street_2 = StringField('street address 2', render_kw={'placeholder': "street address 2"})
    zip_code = StringField('Zip Code', validators=[DataRequired()], render_kw={'placeholder': "zip code"})
    province = StringField('Province', validators=[DataRequired()], render_kw={'placeholder': "Province"})
    country = StringField('Country', validators=[DataRequired()], render_kw={'placeholder': "Country"})
    submit = SubmitField('Confirm')
