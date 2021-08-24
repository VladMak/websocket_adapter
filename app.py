from flask import Flask, request
from functions import add_user, get_user_last_visit, change_password, check_user_exists, change_user_status, check_user_status, get_all_groups_names, add_user_to_group, check_user_in_group, add_user_to_courses_group
from pay import first_register_do, register_do, paymentOrderBinding_do, getBindings_do, getOrderStatusExtended_do, final_getOrderStatusExtended_do

app = Flask(__name__)

@app.route("/add_user", methods=["POST"])
def add_user_func():
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    name = request.form.get('name')
    email = request.form.get('email')
    company = request.form.get('company')
    jobtitle = request.form.get('jobtitle')
    jobsection = request.form.get('jobsection')
    comment = request.form.get('comment')

    if login == None or passwd == None or name == None or email == None or company == None or jobtitle == None or jobsection == None or comment == None:
        return "Invalid params"
    
    return add_user(login, passwd, name, email, company, jobtitle, jobsection, comment)

@app.route("/check_activity", methods=["POST"])
def check_activity_func():
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    email = request.form.get('email')
    if email == None:
        return "Invalid params"

    return get_user_last_visit(login, passwd, email)

@app.route("/change_password", methods=["POST"])
def change_password_func():
    email = request.form.get('email')
    password = request.form.get("password")
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    if email == None or password == None:
        return "Invalid params"

    return change_password(login, passwd, email, password)
   
 

@app.route("/check_user_exists", methods=["POST"])
def check_user_exists_func():
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    email = request.form.get('email')
    if email == None:
        return "Invalid params"

    return check_user_exists(login, passwd, email)

@app.route("/change_user_status", methods=["POST"])
def change_user_status_func():
    email = request.form.get('email')
    status = request.form.get("status")
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    if email == None or status == None:
        return "Invalid params"

    return change_user_status(login, passwd, email, status)

@app.route("/add_user_to_group", methods=["POST"])
def add_user_to_group_func():
    email = request.form.get('email')
    title = request.form.get("title")
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    if email == None or title == None:
        return "Invalid params"

    return add_user_to_group(login, passwd, email, title)

@app.route("/add_user_to_courses_group", methods=["POST"])
def add_user_to_courses_group_func():
    email = request.form.get('email')
    title = request.form.get("title")
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    if email == None or title == None:
        return "Invalid params"

    return add_user_to_courses_group(login, passwd, email, title)

@app.route("/check_user_in_group", methods=["POST"])
def check_user_in_group_func():
    email = request.form.get('email')
    title = request.form.get("title")
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    if email == None or title == None:
        return "Invalid params"

    return check_user_in_group(login, passwd, email, title)

@app.route("/check_user_status", methods=["POST"])
def check_user_status_func():
    email = request.form.get('email')
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    if email == None:
        return "Invalid params"

    return check_user_status(login, passwd, email)

@app.route("/get_all_groups", methods=["POST"])
def get_all_groups_func():
    login = request.form.get('login')
    passwd = request.form.get('passwd')

    return get_all_groups_names(login, passwd)




# первоначальная оплата
@app.route("/set_first_pay", methods=["POST"])
def set_first_pay():
    orderNumber = request.form.get('orderNumber')
    amount = request.form.get('amount')
    clientId = request.form.get('clientId')

    return first_register_do(orderNumber, amount, clientId)

# сведения о платеже. Тут получаем BindingId, только после оплаты
@app.route("/get_binding", methods=["POST"])
def get_binding():
    orderId = request.form.get('orderId')

    return getOrderStatusExtended_do(orderId)

# платеж с настройками автоплатежа.
@app.route("/set_rec_pay", methods=["POST"])
def set_rec_pay():
    bindingId = request.form.get('bindingId')

    return register_do(odredId)

# активация связки
@app.route("/activate_binding", methods=["POST"])
def activate_binding():
    bindingId = request.form.get('bindingId')
    mdOrder = request.form.get('mdOrder')
    ip = request.form.get('ip')

    return paymentOrderBinding_do(bindingId, mdOrder, ip)

# финальный статус
@app.route("/final_status", methods=["POST"])
def final_status():
    orderId = request.form.get('orderId')

    return final_getOrderStatusExtended_do(orderId)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port="8080")