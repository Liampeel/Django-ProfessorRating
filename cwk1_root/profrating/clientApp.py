import requests
import json
from prettytable import PrettyTable


def login(s):
    username = input("username ")
    password = input("password ")
    logininfo = {"username": username, "password": password}

    resp = s.post('http://127.0.0.1:8000/profrating/login/', json=logininfo)
    if resp.status_code != 200:
        print(str(resp.status_code) + " error")

    else:
        print(resp.text)


def register():
    username = input("username ")
    email = input("email ")
    password = input("password ")
    logininfo = {"username": username, "email": email, "password": password}
    resp = requests.post('http://127.0.0.1:8000/profrating/register/', json=logininfo)
    if resp.status_code != 200:
        print(str(resp.status_code))
        print('error')
    else:
        print('registered user')


def logout():
    resp = requests.post('http://127.0.0.1:8000/profrating/logout/')
    if resp.status_code != 200:
        print(str(resp.status_code))
        print('error')
    else:
        print('logged out user')


def module(s):
    resp = s.get('http://127.0.0.1:8000/profrating/moduleinstance/')

    if resp.status_code != 200:
        print(str(resp.status_code))
        print('error')
    else:

        jsonlist = json.loads(resp.text)

        table = PrettyTable(['Module Code', 'Module Name', 'Year', 'Semester', 'Taught by'])

        for data in jsonlist:

            module_code = []
            name = []
            year = str(data['year'])
            semester = str(data['semester'])
            prof = []

            for professor in data['professor']:
                prof.append(str(professor['professor_id']) + " " + str(professor['name']))

            module_code.append(data['module']['module_code'])
            name.append(data['module']['module_name'])

            table.add_row([module_code[0], name[0], year, semester, ', '.join(prof)])

        print(table)


def getrating(s):
    resp = s.get('http://127.0.0.1:8000/profrating/ovrrating/')

    if resp.status_code != 200:
        print(str(resp.status_code))
        print('error')
    else:
        jsonlist = json.loads(resp.text)

        for i in jsonlist:
            print(i)


def averageRating(s):
    professor = input("Professor ID: ")
    module = input("Module Code: ")
    send = {"professor": professor, "module": module}
    resp = s.post('http://127.0.0.1:8000/profrating/modrating/', json=send)
    if resp.status_code != 200:
        print(resp.json)
        print("error")
    else:
        jsonlist = json.loads(resp.text)
        for i in jsonlist:
            print(i)


def postRating(s):
    professor = input("Professor Code: ")
    module = input("Module Code: ")
    year = input("Year ")
    semester = input("Semester: ")
    rating = input("Rating: ")

    sendJson = {"professor": professor, "module": module, "year": year, "semester": semester, "rating": rating}
    resp = s.post('http://127.0.0.1:8000/profrating/postrating/', json=sendJson)
    if resp.status_code != 200:
        print(str(resp.status_code) + " error")

    else:
        print(resp.text)


users_input = ""

while True:
    s = requests.Session()
    users_input = input(" Enter command\n - register, login, logout, list, view, "
                        "average, list, rate\n")

    if users_input == "quit":
        break
    if users_input == "register":
        register()

    if users_input == "login":
        login(s)
        users_input = input("Enter request\n")

        while True:
            if users_input == "":
                break
            if users_input == "average":
                averageRating(s)
                users_input = input("Enter request\n")

            if users_input == "view":
                getrating(s)
                users_input = input("Enter request\n")

            if users_input == "rate":
                postRating(s)
                users_input = input("Enter request\n")

            if users_input == "list":
                module(s)
                users_input = input("Enter request\n")

            if users_input == "logout":
                logout()
                break
