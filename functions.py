import requests, json
from datetime import datetime
from dateutil.parser import parse
from websocket import create_connection


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

def get_all_groups(ws):
    ws.send('4231["api",["DepartmentsGetAll",null]]')
    data = ws.recv()
    return json.loads(data[10:-1])

def get_all_groups_names(login, passwd):
    token = auth_with_password(login, passwd)
    ws = auth_with_token(token)
    groups = get_all_groups(ws)
    ws.close()

    names = ""
    for group in groups:
        names += group["title"]
        names += "\n"
    
    return names

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

def check_user_status(login, passwd, email):
    ws, user = get_user_if_exists(login, passwd, email)

    if user == "Invalid login or password":
        return user

    ws.close()

    if user == None:
        return "No such user"
    else:
        return user["access"]

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

def change_user_status(login, passwd, email, status):
    if status not in ["manager", "student"]:
        return "Invalid status"

    ws, user = get_user_if_exists(login, passwd, email)

    if user == "Invalid login or password":
        return user

    if user == None:
        ws.close()
        return "No such user"
    if user["access"] == status:
        ws.close()
        return f"User is already a {status}"

    user["access"] = status
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
    try:
        date_time = user["last_visit"]
        date = parse(date_time)
        current_date = datetime.now()
        diff = current_date.date() - date.date()

        return f'Заходил {date.date().strftime("%d/%m/%y")} в {date.time().strftime("%H:%M")}, {plural_days(diff.days)} назад'
    except:
        return "Этот пользователь еще не заходил"

def plural_days(n):
    days = ['день', 'дня', 'дней']
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]
