from flask import Flask, request
import requests, json
from datetime import datetime
from dateutil.parser import parse
from websocket import create_connection

app = Flask(__name__)

def auth_with_password(login, password):
    resp = requests.post(
                    "https://1460.unicraft.org/api/v2/auth/credentials", 
                    data = {"Content-Type": "application/json", 
                            "email": login,
                            "password": password}
                    )

    try:
        token = resp.json()["token"]
    except:
        return "Invalid login or password"
    return token

def auth_with_token(token):
    ws = create_connection("wss://1460.unicraft.org/socket.io/?EIO=3&transport=websocket")
    ws.send(f'420["auth","{token}"]'.encode())
    for _ in range(5):
        ws.recv()
    return ws

def add_user(login, passwd, name, email, company, jobtitle, jobsection, comment):
    token = auth_with_password(login, passwd)
    if token == "Invalid login or password":
        return token
    ws = auth_with_token(token)
    ws.send(f'4235["api",["UserUpdate",{{"name":"{name}","email":"{email}","access":"manager","avatar":"","company":"{company}","jobtitle":"{jobtitle}","jobsection":"{jobsection}","language":"","licencefree":false,"disableProfileEdit":false,"password":"","password_repeat":"","comment":"{comment}"}}]]')
    ws.recv()
    ws.close()
    return "Done"

def get_all_users(ws):
    ws.send('423["api",["UsersGetAll",null]]')
    data = ws.recv()
    return json.loads(data[9:-1])

def get_user_if_exists(login, passwd, email):
    token = auth_with_password(login, passwd)
    if token == "Invalid login or password":
        return None, token
    ws = auth_with_token(token)
    users = get_all_users(ws)
    for user in users:
        if user["email"] == email:
            return ws, user
    
    return ws, None

def check_user_exists(login, passwd, email):
    ws, user = get_user_if_exists(login, passwd, email)

    if user == "Invalid login or password":
        return user

    ws.close()

    if user == None:
        return "No such user"
    else:
        return "User exists"

def change_password(login, passwd, email, password):
    ws, user = get_user_if_exists(login, passwd, email)

    if user == "Invalid login or password":
        return user

    if user == None:
        ws.close()
        return "No such user"
    
    params = ["name", "email", "id"]
    user_dct = {}
    for p in params:
        user_dct[p] = user[p]

    user_dct["password"] = password
    user_dct["password_repeat"] = password

    ws.send(f"""4222["api",["UserUpdate", {str(user_dct).replace("'", '"')}]]""")
    ws.recv()
    ws.close()

    return "Done"

def change_user_status(login, passwd, email):
    ws, user = get_user_if_exists(login, passwd, email)

    if user == "Invalid login or password":
        return user

    if user == None:
        ws.close()
        return "No such user"
    if user["access"] != "manager":
        ws.close()
        return "User is not a manager"

    user["access"] = "student"
    params = ["name", "email", "access", "id"]
    user_dct = {}
    for p in params:
        user_dct[p] = user[p]

    ws.send(f"""4222["api",["UserUpdate", {str(user_dct).replace("'", '"')}]]""")
    ws.recv()
    ws.close()

    return "Done"

def get_user_last_visit(login, passwd, email):
    ws, user = get_user_if_exists(login, passwd, email)

    if user == "Invalid login or password":
        return user

    if user == None:
        ws.close()
        return "No such user"

    ws.close()
    date_time = user["last_visit"]
    date = parse(date_time)
    current_date = datetime.now()
    diff = current_date.date() - date.date()

    return f'Заходил {date.date().strftime("%d/%m/%y")} в {date.time().strftime("%H:%M")}, {plural_days(diff.days)} назад'

def plural_days(n):
    days = ['день', 'дня', 'дней']
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]

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
    login = request.form.get('login')
    passwd = request.form.get('passwd')
    if email == None:
        return "Invalid params"

    return change_user_status(login, passwd, email)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")