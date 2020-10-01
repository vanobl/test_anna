import json
import requests
import urllib3

TOKEN = 'TT1Z4nxAreglZaAFMTDiEiiqUCqViwu'

REGISTRATION = 'http://127.0.0.1:8000/api/registration/'
AUTHORIZATION = 'http://127.0.0.1:8000/api/authorization/'
TASK_LIST = 'http://127.0.0.1:8000/api/get_task_list/'
TASK_CREATE = 'http://127.0.0.1:8000/api/create_task/'
TASK_INFO = 'http://127.0.0.1:8000/api/info_task/'
TASK_CHANGE = 'http://127.0.0.1:8000/api/change_task/'

my_data_registration = {
    'action': 'create',
    'user': {
        'username': 'vanobl',
        'password': 'zaqwsx123'
    }
}

my_data_authenticate = {
    'action': 'authenticate',
    'user': {
        'username': 'vanobl',
        'password': 'zaqwsx123'
    }
}

my_data_get_task_list = {
    'action': 'get_tasks_list',
    'filter_status': 'новая',
    'timeplane': ''
}

my_data_create_task = {
    'action': 'create_task',
    'task': {
        'name': 'пробная',
        'description': 'офигительное описание задачи',
        'timeplane': '2020-10-25 18:50',
    }
}

my_data_info_task = {
    'action': 'info_task',
    'uuid_task': 'b5c34b90-e1cc-48b2-96aa-7382dfc7491a'
}

my_data_change_task = {
    'action': 'change_task',
    'uuid_task': 'b5c34b90-e1cc-48b2-96aa-7382dfc7491a',
    'task': {
        'name': 'особая задача',
        'description': 'Допустим, вы летите из Москвы во Владивосток, а затем обратно, при полном безветрии. Затем вы совершаете точно такой же перелёт, но на этот раз на протяжении всего перелёта дует постоянный западный ветер: в одну сторону попутный, в обратную — лобовой.',
        # 'timeplane': '2020-12-30 23:59',
        'status': 4
    }
}

jdata = json.dumps(my_data_change_task)

url = TASK_CHANGE

client = requests.session()
# client.get(url)

myheaders = {'Content-type': 'application/json', 'Authorization': TOKEN}
resp = client.get(url=url, data=jdata, headers=myheaders)
text_content = resp.json()


print(text_content)