from flask import Flask, request
from functions import add_user, get_user_last_visit, change_password, check_user_exists, change_user_status, check_user_status, get_all_groups_names

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

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port="8080")