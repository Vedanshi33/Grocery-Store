from flask_sqlalchemy import SQLAlchemy
from flask_security import (
    UserMixin,
    RoleMixin,
    SQLAlchemySessionUserDatastore,
    Security,
)
from flask import current_app as app
from datetime import date

db = SQLAlchemy()


class Categories(db.Model):
    c_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)
    products = db.relationship(
        "Product",
        backref=db.backref("category_rel"),
        lazy="subquery",
        cascade="all, delete-orphan",
    )


class CategoriesRequest(db.Model):
    __tablename__ = "categoriesrequest"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer)
    u_id = db.Column(db.Integer)
    request_type = db.Column(db.String(50))
    status = db.Column(db.String(50))


class Product(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(100), nullable=False)
    p_image = db.Column(db.String(50), nullable=False)
    manufacturing_date = db.Column(db.DateTime, nullable=False)
    rate_per_unit = db.Column(db.Float, nullable=False)
    details = db.Column(db.String(40))
    quantity = db.Column(db.Float, nullable=False, default=0)
    quantity_unit = db.Column(db.String(20))
    demand_factor = db.Column(db.Float, default=1.0)

    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.c_id"), nullable=False
    )
    category = db.relationship(
        "Categories",
        backref=db.backref("products_rel", cascade="all, delete-orphan"),
        lazy="subquery",
    )


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey("product.p_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.c_id"))
    quantity = db.Column(db.Integer)

    product = db.relationship("Product", backref="cart_items")
    category = db.relationship("Categories", backref="cart_items")
    # order_item = db.relationship('OrderItem', back_populates='cart')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=date.today())

    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    # cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.p_id"), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.c_id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", foreign_keys=[product_id])
    category = db.relationship("Categories")
    # cart = db.relationship('Cart', back_populates='order_item')


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users"))
    

class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)


class SMRequest(db.Model):
    __tablename__ = "smrequest"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
