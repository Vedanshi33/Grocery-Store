from weasyprint import HTML, CSS
from jinja2 import Template
import os
from dateutil.relativedelta import relativedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from app import *


SMTP_SERVER_HOST = "localhost"
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = "vedanshi@email.com"
SENDER_PASSWORD = ""


@celery.task()
def mail_report():
    BasePath = os.path.abspath(os.path.dirname(__file__))
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
