import requests


def get_token():
    body = {
        'username': 'Chintsai',
        'password': '********'
    }
    res = requests.post('http://127.0.0.1:8000/task/auth/token/', data=body)
    return res.json()['access']


def get_report():
    res = requests.get('http://127.0.0.1:8000/task/info/report', headers={'Authorization': 'Bearer ' + get_token()})
    print('get report', res.text)


if __name__ == '__main__':
    get_report()
