from flask import Flask, render_template, url_for, request, jsonify,g
from flask_security import current_user,login_required,hash_password,roles_required,verify_password,auth_required,roles_accepted

from sqlalchemy import func
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from flask_cors import CORS
import matplotlib.ticker as mticker
from flask_cors import CORS
from applications.model import *
from applications.workers import *
from applications.caching import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///GroceryStore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config["SECRET_KEY"] = "secretkey"
app.config["SECURITY_PASSWORD_HASH"] = "bcrypt"
app.config["SECURITY_PASSWORD_SALT"] = "vedanshi"
app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"] = "Authentication-Token"
app.config["SECURITY_REGISTERABLE"] = False
app.config["SECURITY_CONFIRMABLE"] = False
app.config["SECURITY_SEND_REGISTER_EMAIL"] = False
app.config["SECURITY_UNAUTHORIZED_VIEW"] = None
app.config["WTF_CSRF_ENABLED"] = False

app.config["CELERY_BROKER_URL"] = "redis://127.0.0.1:6379/1"
app.config["CELERY_RESULT_BACKEND"] = "redis://127.0.0.1:6379/2"
app.config["REDIS_URL"] = "redis://localhost:6379"
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 3000
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 3
CORS(app)
cache.init_app(app)
app.app_context().push()


######### PATH FOR STORING IMAGES ######
UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)
app.app_context().push()


from applications.task import *


app.app_context().push()

celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
)
celery.Task = ContextTask


########HOME PAGE#########
@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "GET":
        return render_template("home.html")


########USER LOGIN#############


@app.route("/user_login", methods=["POST"])
def user_login():
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    
    user = User.query.filter_by(email=email).first()

    if user and verify_password(password, user.password):
       
        access_token = user.get_auth_token()
        role = "user"
        if user.roles != []:
            role = user.roles[0].name
        print(role)
        return (
            jsonify(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "role": role,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {"error": "Invalid credentials"},
            ),
            401,
        )


#########USER REGISTER############


@app.route("/user_register", methods=["POST"])
def user_register():
    if current_user.is_authenticated:
        return jsonify({"message": "User is already authenticated"}), 400

    email = request.get_json().get("email")
    password = request.get_json().get("password")
    first_name = request.get_json().get("first_name")
    last_name = request.get_json().get("last_name")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email is already registered"}), 400

    user = user_datastore.create_user(
        email=email,
        password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
    )
    db.session.commit()

    return (
        jsonify({"message": "Registration successful", "token": user.get_auth_token()}),
        201,
    )





##########ADMIN LOGIN###########


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return jsonify({"message": "Admin is already authenticated"}), 400
    if request.method == "POST":
        email = request.get_json().get("email")
        password = request.get_json().get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            access_token = user.get_auth_token()

            if verify_password(password, user.password):
                role = "user"
                if user.roles != []:
                    role = user.roles[0].name
                print(role)
                return (
                    jsonify(
                        {
                            "message": "Login successful",
                            "access_token": access_token,
                            "role": role,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Wrong Password"}), 401
    else:
        return jsonify({"error": "Admin doesn't exist"}), 404

    return jsonify({"error": "Login failed"}), 400


##########Request ###########

@app.route("/storemanager_request", methods=["POST", "DELETE"])
@auth_required("token")
def storemanager_request():
    if request.method == "POST":
        print(current_user.id)
        if current_user.roles != []:
            return jsonify({"error": "invalid request already have role"})
        smr = SMRequest.query.filter_by(user_id=current_user.id).first()
        if smr is not None:
            return jsonify({"error": "request already exist"}), 400
        smr = SMRequest(user_id=current_user.id)
        db.session.add(smr)
        db.session.commit()
        return jsonify({"message": "Store manager request has been made"}), 200
    if request.method == "DELETE":
        smr = SMRequest.query.filter_by(user_id=current_user.id).first()
        if smr is None:
            return jsonify({"error": "request does not exist"}), 400
        db.session.delete(smr)
        db.session.commit()
        return jsonify({"message": "Store manager request has been delete"}), 200

####### ADMIN GET SM REQUEST############

@app.route("/admin/get_storemanager_request", methods=["GET"])
@roles_required("admin")
@auth_required("token")
def get_smrequests():
    if request.method == "GET":
        smr = SMRequest.query.all()
        data = []
        for r in smr:
            d = {}
            u = User.query.get(r.user_id)
            d["id"] = r.user_id
            d["email"] = u.email
            d["first_name"] = u.first_name
            d["last_name"] = u.last_name
            data.append(d)
        return jsonify({"sm_request": data})

###### ADMIN STORE MANAGER REQUEST######

@app.route("/admin/storemanager_request/<int:user_id>", methods=["POST", "DELETE"])
@auth_required("token")
@roles_required("admin")
def approve_store_manager_request(user_id):
    if request.method == "POST":
        smr = SMRequest.query.filter_by(user_id=user_id).first()
        if smr is None:
            return jsonify({"error": "request does not exist"}), 400
        user = User.query.get(user_id)
        SMRole = Role.query.filter_by(name="store manager").first()
        if user and user.roles == []:
            user.roles.append(SMRole)
            db.session.delete(smr)
            db.session.commit()
            return jsonify({"message": "Store manager request approved"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    if request.method == "DELETE":
        smr = SMRequest.query.filter_by(user_id=user_id).first()
        if smr is None:
            return jsonify({"error": "request does not exist"}), 400
        db.session.delete(smr)
        db.session.commit()
        return jsonify({"message": "Store manager request has been deleted"}), 200

########USER STATUS ###########

@app.route("/user_request_status", methods=["GET"])
@auth_required("token")
def user_request_status():
    if current_user.roles != []:
        return jsonify({"status": "accepted"})
    smr = SMRequest.query.filter_by(user_id=current_user.id).first()
    if smr is not None:
        return jsonify({"status": "pending"})
    else:
        return jsonify({"status": "rejected"})


########USER DASHBOARD#########

@app.route("/user_dashboard")
@auth_required("token")
def user_dashboard():
    categories = get_categories()
    print(categories)
    categories_list = [
        {"id": category.c_id, "name": category.name} for category in categories
    ]
    return jsonify(categories=categories_list)


###########ADMIN DASHBOARD############

@app.route("/admin_dashboard", methods=["GET", "POST"])
@auth_required("token")
@roles_required("admin")
def admin_dashboard():
    if request.method == "POST":
        category_id = request.get_json().get("category_id")
        if category_id:
            return jsonify(
                {"redirect_url": url_for("edit_product", category_id=category_id)}
            )

    categories = get_categories()
    categories_list = [
        {"id": category.c_id, "name": category.name} for category in categories
    ]
    return jsonify(categories=categories_list)


###########STORE MANAGER DASHBOARDD ################

@app.route("/sm_dashboard", methods=["GET", "POST"])
@auth_required("token")
@roles_required("store manager")
def sm_dashboard():
    if request.method == "POST":
        category_id = request.get_json().get("category_id")
        if category_id:
            return jsonify(
                {"redirect_url": url_for("edit_product", category_id=category_id)}
            )

    categories = get_categories()
    categories_list = [
        {"id": category.c_id, "name": category.name} for category in categories
    ]
    return jsonify(categories=categories_list)


###### CREATE CATEGORY #########

@app.route("/create_category", methods=["GET", "POST"])
@auth_required("token")
@roles_accepted("admin")
def create_category():
    if request.method == "POST":
     
        category_id = request.form.get("category_id")
        category_name = request.form.get("category_name")
        image = request.files.get("file")

        if category_id is None or category_name is None or image is None:
            return jsonify({"error": "Invalid data"}), 400

        image_filename = image.filename
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
        image.save(image_path)
        if current_user.roles[0].name == "store manager":
            cr = CategoriesRequest.query.filter_by(
                category_id=category_id,
                u_id=current_user.id,
                request_type="create",
                status="pending",
            ).first()
            if cr is not None:
                cr.name = category_name
                cr.image = image_filename
                db.session.commit()
                return jsonify({"message": "request has been sent to admin"})
            cr = CategoriesRequest(
                name=category_name,
                image=image_filename,
                category_id=category_id,
                u_id=current_user.id,
                request_type="create",
                status="pending",
            )
            db.session.add(cr)
            db.session.commit()
            return jsonify({"message": "request has been sent to admin"})
        category = Categories(
            c_id=category_id, name=category_name, image=image_filename
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({"message": "Category created successfully"}), 201


######EDIT CATEGORY ONLY ########

@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
@auth_required("token")
@roles_accepted("admin", "store manager")
def edit_category(category_id):
    category = Categories.query.filter_by(c_id=category_id).first()
    if request.method == "POST":
        category_name = request.form.get("category_name")
        image_filename = None
        if "image" in request.files:
            image = request.files["image"]
            if image:
                image_filename = image.filename
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
                image.save(image_path)
        if current_user.roles[0].name == "store manager":
            cr = CategoriesRequest.query.filter_by(
                category_id=category.c_id,
                u_id=current_user.id,
                request_type="edit",
                status="pending",
            ).first()
            if cr is not None:
                cr.name = category_name
                cr.image = image_filename
                db.session.commit()
                return jsonify({"message": "request has been sent to admin"})
            if image_filename is not None:
                cr = CategoriesRequest(
                    name=category_name,
                    image=image_filename,
                    category_id=category.c_id,
                    u_id=current_user.id,
                    request_type="edit",
                    status="pending",
                )
            else:
                cr = CategoriesRequest(
                    name=category_name,
                    image=category.image,
                    category_id=category.c_id,
                    u_id=current_user.id,
                    request_type="edit",
                    status="pending",
                )
            db.session.add(cr)
            db.session.commit()
            return jsonify({"message": "request has been sent to admin"})
        if image_filename is not None:
            category.image = image_filename
        category.name = category_name
        db.session.commit()
        response_data = {"message": "Category updated successfully!"}
        return jsonify(response_data), 200

    category_data = {"id": category.id, "name": category.name, "image": category.image}
    return jsonify(category_data)

###VIEW CATEGORIES ONLY########

@app.route("/categories", methods=["GET", "POST", "DELETE"])
@auth_required("token")
def view_categories():
    categories = get_categories()

    categories_list = [
        {
            "id": category.c_id,
            "name": category.name,
            "image": category.image,
            "products": [
                {"p_id": product.p_id, "p_name": product.p_name}
                for product in category.products
            ],
        }
        for category in categories
    ]

    return jsonify(categories=categories_list)


#####REMOVE CATEGORY#####

@app.route("/remove_category/<int:category_id>", methods=["POST", "DELETE"])
@auth_required("token")
@roles_accepted("admin", "store manager")
def remove_category(category_id):
    category = Categories.query.get_or_404(category_id)
    if current_user.roles[0].name == "store manager":
        cr = CategoriesRequest.query.filter_by(
            category_id=category.c_id, u_id=current_user.id, request_type="delete"
        ).first()
        if cr is not None:
            return jsonify({"message": "request already exitst"})
        cr = CategoriesRequest(
            name=category.name,
            image=category.image,
            category_id=category.c_id,
            u_id=current_user.id,
            request_type="delete",
            status="pending",
        )
        db.session.add(cr)
        db.session.commit()
        return jsonify({"message": "request has been sent to admin"})
    try:
        db.session.delete(category)
        db.session.commit()
        response_data = {
            "message": f'Category "{category.name}" has been deleted successfully.'
        }
        return jsonify(response_data), 200
    except Exception as e:
        db.session.rollback()
        response_data = {"error": "An error occurred while deleting the category."}
        return jsonify(response_data), 500

####### SM CATEGORY REQUESTS ############

@app.route("/category_requests", methods=["GET", "POST", "DELETE"])
@auth_required("token")
@roles_accepted("admin", "store manager")
def category_requests():
    if request.method == "GET":
        if current_user.roles[0].name == "store manager":
            cr = CategoriesRequest.query.filter_by(u_id=current_user.id).all()
        else:
            cr = CategoriesRequest.query.filter_by(status="pending").all()
        data = []
        for r in cr:
            d = {}
            d["id"] = r.id
            d["name"] = r.name
            d["image"] = r.image
            d["status"] = r.status
            d["request_type"] = r.request_type
            d["category_id"] = r.category_id
            if r.request_type != "create":
                c = Categories.query.get(r.category_id)
                if c is not None:
                    d["category_name"] = c.name
                    d["category_image"] = c.image
            if current_user.roles[0].name != "store manager":
                u = User.query.get(r.u_id)
                d["first_name"] = u.first_name
                d["last_name"] = u.last_name
                d["email"] = u.email
            data.append(d)
        return jsonify(data)
    if request.method == "POST":
        if current_user.roles[0].name == "store manager":
            return jsonify({"message": "only admin can access this"}), 404
        r_id = request.get_json().get("id")
        cr = CategoriesRequest.query.get(r_id)
        if cr.request_type == "delete":
            c = Categories.query.get(cr.category_id)
            db.session.delete(c)
            cr.status = "accepted"
            db.session.commit()
            return jsonify({"message": "Category has been Delete"}), 200
        if cr.request_type == "edit":
            c = Categories.query.get(cr.category_id)
            c.name = cr.name
            c.image = cr.image
            cr.status = "accepted"
            db.session.commit()
            return jsonify({"message": "Category has been updated"}), 200
        if cr.request_type == "create":
            c = Categories(c_id=cr.category_id, name=cr.name, image=cr.image)
            db.session.add(c)
            cr.status = "accepted"
            db.session.commit()
            return jsonify({"message": "Category has been updated"}), 200

    if request.method == "DELETE":
        r_id = request.get_json().get("id")
        # print(r_id)
        cr = CategoriesRequest.query.get(r_id)
        if current_user.roles[0].name == "store manager":
            if cr.u_id == current_user.id and cr.status == "pending":
                db.session.delete(cr)
                db.session.commit()
                return jsonify({"message": "your request has been cancel"}), 200
            return jsonify({"message": "this request doesnot belong to you"}), 404
        cr.status = "rejected"
        db.session.commit()
        return jsonify({"message": "request has been rejected"}), 200


######ADD PRODUCTS #######

@app.route("/add_product/<int:category_id>", methods=["GET", "POST"])
@auth_required("token")
@roles_required("store manager")
def add_product(category_id):
    category = Categories.query.filter_by(c_id=category_id).first()

    if request.method == "POST":
        id = request.form["p_id"]
        name = request.form["p_name"]
        rate_per_unit = request.form["rate_per_unit"]
        manufacturing_date = datetime.strptime(
            request.form["manufacturing_date"], "%Y-%m-%d"
        )
        details = request.form["details"]
        quantity = request.form["quantity"]
        quantity_unit = request.form["quantity_unit"]
        print(request.files)
        p_image = request.files["p_image"]

        image_f = p_image.filename
        image_p = os.path.join(app.config["UPLOAD_FOLDER"], image_f)
        p_image.save(image_p)

        product = Product(
            p_id=id,
            p_name=name,
            p_image=image_f,
            rate_per_unit=rate_per_unit,
            manufacturing_date=manufacturing_date,
            details=details,
            quantity=quantity,
            quantity_unit=quantity_unit,
            category=category,
        )
        db.session.add(product)
        db.session.commit()
        response_data = {"message": "Product added successfully!"}
        return jsonify(response_data), 200

    category_data = {
        "id": category.c_id,
        "name": category.name,
    }
    return jsonify(category=category_data)


###### EDIT PRODUCT #######

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@auth_required("token")
@roles_required("store manager")
def edit_product(product_id):
    product = get_product(product_id)
    category_id = product.category_id

    if request.method == "POST":
        name = request.form.get("p_name")
        rate_per_unit = request.form.get("rate_per_unit")
        manufacturing_date = datetime.strptime(
            request.form.get("manufacturing_date"), "%Y-%m-%d"
        )
        details = request.form.get("details")
        quantity = request.form.get("quantity")
        quantity_unit = request.form.get("quantity_unit")

        if "p_image" in request.files:
            p_image = request.files["p_image"]
            if p_image:
                image_filename = p_image.filename
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
                p_image.save(image_path)
                product.p_image = image_filename

        product.p_name = name
        product.rate_per_unit = rate_per_unit
        product.details = details
        product.quantity = quantity
        product.manufacturing_date = manufacturing_date
        product.quantity_unit = quantity_unit

        db.session.commit()
        response_data = {"message": "Product updated successfully!"}
        return jsonify(response_data), 200

    product_data = {
        "id": product.p_id,
        "p_name": product.p_name,
        "rate_per_unit": product.rate_per_unit,
        "manufacturing_date": product.manufacturing_date.strftime("%Y-%m-%d"),
        "details": product.details,
        "quantity": product.quantity,
        "quantity_unit": product.quantity_unit,
        "category_id": category_id,
    }
    return jsonify(product=product_data)


##VIEW PRODUCTS #####

@app.route("/category/<int:category_id>")
@auth_required("token")
def view_category(category_id):
    category = Categories.query.get(category_id)
    products = category.products
    cart_items = Cart.query.filter_by(customer_id=current_user.id).all()
   
    total_amount = 0

    for cart_item in cart_items:
        product = get_product(cart_item.product_id)
        if product:
            total_amount += product.rate_per_unit * cart_item.quantity

    response_data = {
        "category_id": category.c_id,
        "category_name": category.name,
        "products": [
            {
                "product_id": product.p_id,
                "product_name": product.p_name,
                "product_details": product.details,
                "p_image": product.p_image,
                "rate_per_unit": product.rate_per_unit,
                "unit": product.quantity_unit,
                "manufacturing_date": product.manufacturing_date,
                "demand_factor": product.demand_factor,
            }
            for product in products
        ],
        "cart_items": [
            {"product_id": cart_item.product_id, "quantity": cart_item.quantity}
            for cart_item in cart_items
        ],
        "total_amount": total_amount,
    }
   
    return jsonify(response_data)


#######DELETE PRODUCT#########

@app.route("/delete_product/<int:category_id>/<int:product_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("store manager")
def delete_product(category_id, product_id):
    if request.method == "DELETE":
        product = Product.query.filter_by(
            category_id=category_id, p_id=product_id
        ).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            response_data = {"message": "Product deleted successfully!"}
            return jsonify(response_data), 200
        else:
            response_data = {"error": "Product not found."}
            return jsonify(response_data), 404

    return jsonify({"error": "Invalid request method"}), 400


####   CART ######

@app.route("/cart")
@auth_required("token")
def cart():
    cart_items = Cart.query.filter_by(customer_id=current_user.id).all()
    total_amount = 0
    cart_data = []

    for cart_item in cart_items:
        product = get_product(cart_item.product_id)
        if product:
            total_amount += (
                product.rate_per_unit
                * cart_item.quantity
                * cart_item.product.demand_factor
            )

            cart_data.append(
                {
                    "cart_id": cart_item.id,
                    "product_id": product.p_id,
                    "product_name": product.p_name,
                    "quantity": cart_item.quantity,
                    "price": product.rate_per_unit * cart_item.product.demand_factor,
                    "total_price": product.rate_per_unit
                    * cart_item.quantity
                    * cart_item.product.demand_factor,
                }
            )

    response_data = {"cart_items": cart_data, "total_amount": total_amount}

    return jsonify(response_data)


def calculate_demand_factor(available_quantity, total_quantity):
    # Calculate the percentage of products sold
    percentage_sold = (total_quantity - available_quantity) / total_quantity * 100

    if percentage_sold < 20:
        return 0.9
    elif percentage_sold > 60:
        return 1.2
    else:
        return 1.0  # No change in price


####ADD TO CART ######

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
@auth_required("token")
def add_to_cart(product_id):
    # print(product_id)
    product = get_product(product_id)
    total_ordered_quantity = (
        db.session.query(func.coalesce(func.sum(OrderItem.quantity), 0))
        .filter(OrderItem.product_id == product_id)
        .scalar()
    )

    quantity_available = product.quantity - total_ordered_quantity
    demand_factor = calculate_demand_factor(quantity_available, product.quantity)
    print(demand_factor)
    product.demand_factor = demand_factor
    # print(request.get_json())
    quantity_requested = int(request.get_json()["quantity"])
    if quantity_requested > quantity_available:
        response_data = {"error": "Sorry, the product is currently out of stock."}
        return jsonify(response_data), 400

    if product:
        category_id = product.category_id
        quantity = int(request.get_json().get("quantity"))
        customer_id = current_user.id

        cart_item = Cart(
            customer_id=customer_id,
            product_id=product_id,
            category_id=category_id,
            quantity=quantity,
        )
        db.session.add(cart_item)
        db.session.commit()

        response_data = {"message": "Product added to cart successfully!"}
        return jsonify(response_data), 200

    response_data = {"error": "Product not found."}
    return jsonify(response_data), 404


#########   BILLING   #######

@app.route("/billing", methods=["GET", "POST"])
@auth_required("token")
def billing():
    if request.method == "POST":
        name = request.get_json().get("name")
        address = request.get_json().get("address")
        payment_info = request.get_json().get("payment_info")

        cart_items = Cart.query.filter_by(customer_id=current_user.id).all()
        total_amount = 0
        for item in cart_items:
            product = get_product(item.product_id)
            if product:
                total_amount += product.rate_per_unit * item.quantity

        order = Order(customer_id=current_user.id, total_amount=total_amount)
        db.session.add(order)
        db.session.commit()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                cart_id=item.id,
                product_id=item.product_id,
                category_id=item.category_id,
                quantity=item.quantity,
                amount_paid=0,
            )
            db.session.add(order_item)
        db.session.commit()

        for item in cart_items:
            db.session.delete(item)
        db.session.commit()

        response_data = {"message": "Billing successful!"}
        return jsonify(response_data), 200

    response_data = {"message": "Please provide billing information."}
    return jsonify(response_data)


####CONFIRMATION ######

@app.route("/confirmation", methods=["GET", "POST"])
@auth_required("token")
@login_required
def confirmation():
    if request.method == "POST":
        cart_items = Cart.query.filter_by(customer_id=current_user.id).all()
        customer_id = current_user.id
        for cart_item in cart_items:
            product = get_product(cart_item.product_id)
            total_amount = (
                product.rate_per_unit * cart_item.quantity
            ) * product.demand_factor
            order = Order(customer_id=customer_id, total_amount=total_amount)
            db.session.add(order)
            db.session.commit()

            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                category_id=product.category_id,
                quantity=cart_item.quantity,
            )
            db.session.add(order_item)
            db.session.commit()

        Cart.query.filter_by(customer_id=current_user.id).delete()
        db.session.commit()

        response_data = {"message": "Order confirmation successful!"}
        return jsonify(response_data), 200

    cart_items = Cart.query.filter_by(customer_id=current_user.id).all()
    total_amount = 0
    for item in cart_items:
        product = get_product(item.product_id)
        if product:
            total_amount += product.rate_per_unit * item.quantity

    response_data = {
        "cart_items": [
            {"product_id": item.product_id, "quantity": item.quantity}
            for item in cart_items
        ],
        "total_amount": total_amount,
    }

    return jsonify(response_data)


######SEARCH PRODUCTS ######

@app.route("/search_products", methods=["GET"])
@auth_required("token")
@login_required
def search_products():
    query = request.args.get("query")

    try:
        date_obj = datetime.strptime(query, "%Y-%m-%d")

    except ValueError:
        date_obj = None

    product_results = Product.query.filter(
        db.or_(
            Product.p_name.ilike(f"%{query}%"),
            db.cast(Product.rate_per_unit, db.String).ilike(f"%{query}%"),
        )
    ).all()

    category_results = Categories.query.filter(
        Categories.name.ilike(f"%{query}%")
    ).all()

    response_data = {
        "product_results": [
            {
                "p_id": product.p_id,
                "p_name": product.p_name,
                "p_image": product.p_image,
                "rate_per_unit": product.rate_per_unit,
                "unit": product.quantity_unit,
                "manufacturing_date": product.manufacturing_date,
                "quantity": product.quantity,
            }
            for product in product_results
        ],
        "category_results": [
            {"id": category.c_id, "name": category.name, "image": category.image}
            for category in category_results
        ],
    }

    return jsonify(response_data)


###### REMOVE ITEM FROM CART #######

@app.route("/remove_from_cart/<int:product_id>", methods=["DELETE", "POST"])
@auth_required("token")
@login_required
def remove_from_cart(product_id):
    cart = Cart.query.filter_by(
        customer_id=current_user.id, product_id=product_id
    ).first()

    if cart is None:
        response_data = {"error": "Cart not found for the user."}
        return jsonify(response_data), 404

    cart_item = Cart.query.filter_by(id=cart.id, product_id=product_id).first()

    if cart_item is None:
        response_data = {"error": "Product not found in the cart."}
        return jsonify(response_data), 404

    try:
       
        db.session.delete(cart_item)
        db.session.commit()

        response_data = {"message": "Product removed from cart successfully!"}
        return jsonify(response_data), 200

    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of an error
        response_data = {"error": "Failed to remove product from cart."}
        return jsonify(response_data), 500  # Internal Server Error


#####SUMMARY ######

@app.route("/admin/summary", methods=["GET"])
@auth_required("token")
@roles_required("admin")
def admin_summary():
    order_items = OrderItem.query.all()

    response_data = {
        "order_items": [
            {
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
            }
            for item in order_items
        ]
    }

    return jsonify(response_data)


####### USER ORDERS  #####

@app.route("/my_orders")
@auth_required("token")
def my_orders():
    order_items = (
        OrderItem.query.join(Order).filter(Order.customer_id == current_user.id).all()
    )

    if order_items:
        order_list = []
        for order_item in order_items:
            if order_item.product is not None:
                product_name = order_item.product.p_name
                total_bill = order_item.order.total_amount
                date = order_item.order.date.strftime(
                    "%Y-%m-%d"
                )  # Format the date as a string
                order_list.append(
                    {
                        "product_name": product_name,
                        "total_bill_paid": total_bill,
                        "date": date,
                    }
                )
            else:
                order_list.append(
                    {
                        "product_name": "Unknown Product",
                        "total_bill_paid": "N/A",
                        "date": "N/A",
                    }
                )

        return jsonify(order_list)
    else:
        message = "Sorry, you have no old orders"
        return jsonify({"message": message})

#########EXPORT 

@app.route("/export")
@auth_required("token")
@roles_required("store manager")
def export_product_csv():
    export_csv.apply_async(args=[current_user.email])
    return jsonify({"message": "Csv file will be sent to your mail id shortly"})


#####RUN APP #####

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
