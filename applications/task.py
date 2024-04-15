from .workers import *
from weasyprint import HTML, CSS
from jinja2 import Template
import os
from dateutil.relativedelta import relativedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from .model import *
import requests
from sqlalchemy import func
from pathlib import Path


SMTP_SERVER_HOST = "localhost"
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = "vedanshi@email.com"
SENDER_PASSWORD = ""


@celery.task()
def reminder():
    url = "https://chat.googleapis.com/v1/spaces/AAAAAsdtTc4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=mw9wLNF3_x_ZDT3S9vah00JYwndq9iYRTtF0h7m3ceM"
    users = User.query.all()
    today_date = date.today()
    for user in users:
        if user.roles == []:  # to check if they are not admin or store manager
            orders = Order.query.filter_by(customer_id=user.id, date=today_date).all()
            if orders == []:
                msg = f""" Dear {user.first_name},\nWe have noticed that you haven't ordered anything today please order now \nThank you """
                response = requests.post(url, json={"text": msg})
                print(response.status_code)
                return True


@celery.task()
def mail_report():
    BasePath = Path(__file__).parent.parent
    f = open(os.path.join(BasePath, "templates", "report.html"), "r")
    template = Template(f.read())
    users = User.query.all()
    first_of_this_month = date.today().replace(day=1)
    first_of_next_month = first_of_this_month + relativedelta(months=1)
    for user in users:
        orders = Order.query.filter(
            (Order.date >= first_of_this_month)
            & (Order.date < first_of_next_month)
            & (Order.customer_id == user.id)
        ).all()
        if orders != [] and user.roles == []:
            products = []
            total_spend = 0
            for order in orders:
                order_item = OrderItem.query.filter_by(order_id=order.id).first()
                product = Product.query.get(order_item.product_id)
                d = {}
                d["name"] = product.p_name
                d["quantity"] = order_item.quantity
                d["order_date"] = order.date.strftime("%Y-%m-%d")
                d["cost"] = order.total_amount
                total_spend += order.total_amount
                products.append(d)
            html = template.render(
                firstname=user.first_name, products=products, total_spend=total_spend
            )
            pdf = HTML(string=html).write_pdf()
            msg = MIMEMultipart()
            msg["From"] = SENDER_ADDRESS
            msg["To"] = user.email
            msg["Subject"] = "Monthly Spend Report"
            message = f"Dear {user.first_name},\nPlease Find attachment Containing Monthly Spend Report.\nThank You"
            msg.attach(MIMEText(message, "plain"))
            attach = MIMEApplication(pdf, _subtype="pdf")
            attach.add_header(
                "Content-Disposition", "attachment; filename=MonthlySpendReport.pdf"
            )
            msg.attach(attach)

            s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SERVER_SMTP_PORT)
            s.login(user=SENDER_ADDRESS, password=SENDER_PASSWORD)
            s.send_message(msg)
            s.quit()


@celery.task(name="export_csv")
def export_csv(storemanager_email):
    try:
        csv = "name,stock remaining,description,price,number of units sold\n"
        products = Product.query.all()
        for product in products:
            total_ordered_quantity = (
                db.session.query(func.coalesce(func.sum(OrderItem.quantity), 0))
                .filter(OrderItem.product_id == product.p_id)
                .scalar()
            )
            stock_remaining = product.quantity - total_ordered_quantity
            s = f"{product.p_name},{str(stock_remaining)},{product.details},{str(product.rate_per_unit)},{str(total_ordered_quantity)}\n"
            csv += s
        csv = csv.encode()
        msg = MIMEMultipart()
        msg["From"] = SENDER_ADDRESS
        msg["To"] = storemanager_email
        msg["Subject"] = "Monthly Spend Report"
        message = f"Please Find attachment Containing csv file of products.\nThank You"
        msg.attach(MIMEText(message, "plain"))
        attach = MIMEApplication(csv, _subtype="csv")
        attach.add_header("Content-Disposition", "attachment; filename=Products.csv")
        msg.attach(attach)
        s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SERVER_SMTP_PORT)
        s.login(user=SENDER_ADDRESS, password=SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
        return True
    except Exception as e:
        print(e)
        return False


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, reminder.s(), name='Order Reminder') # this will send reminder every 10 sec
    #sender.add_periodic_task(
    #    crontab(minute=00, hour=13), reminder.s(), name="Order Reminder"))
     # this will send every day at 13:00 utc which is 6:30 pm IST
    # sender.add_periodic_task(10.0, mail_report.s(), name='Monthly Spend Report')
    sender.add_periodic_task(
        crontab(minute=0, hour=0, day_of_month=28),
        mail_report.s(),
        name="Monthly Spend Report",
    )
