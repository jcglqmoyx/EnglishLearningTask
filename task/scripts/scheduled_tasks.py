import datetime
import os

import requests


def get_date_str():
    yesterday_now = datetime.datetime.now() - datetime.timedelta(days=1)
    year, month, day = yesterday_now.year, yesterday_now.month, yesterday_now.day
    res = '%d-' % year
    if month < 10:
        res += '0'
    res += '%d-' % month
    if day < 10:
        res += '0'
    res += '%d' % day
    return res


def get_token():
    body = {
        'username': 'Chintsai',
        'password': '********'
    }
    res = requests.post('http://127.0.0.1:8000/task/auth/token/', data=body)
    return res.json()['access']


def update_github_page():
    yesterday_date_str = get_date_str()
    requests.get('http://127.0.0.1:8000/task/info/report', headers={'Authorization': 'Bearer ' + get_token()})
    path = '/home/lighthouse/EnglishLearningTask/task/templates/markdown/%s_*.md' % yesterday_date_str

    os.system('mv %s %s' % (path, '/home/lighthouse/report/'))

    file = open('/home/lighthouse/report/index.md', 'w')
    file.write('# %s 打卡情况\n' % yesterday_date_str)

    group_count = requests.get('http://127.0.0.1:8000/task/info/group/count').json()['group_count']
    for group_id in range(1, group_count + 1):
        file.write('[%d群](%s_%d.md)' % (group_id, yesterday_date_str, group_id))
        file.write('\n')
        file.write('<br>')
    file.close()
    os.system('cd /home/lighthouse/report && git add . && git commit -m "update report" && git push')


if __name__ == '__main__':
    update_github_page()
