import datetime

import requests
from clickhouse_driver import Client
import pandas

from ozon_test.celery import app

@app.task
def task_parse(id_user, api_key):
    from_date = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    to_date = (datetime.datetime.today() - datetime.timedelta(days=4)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    headers = {'Client-Id': id_user,
               'Api-Key': api_key}
    url = 'https://api-seller.ozon.ru/v1/posting/global/etgb'
    json_body = {
        "date": {
            "from": from_date,
            "to": to_date,
        }
    }
    response = requests.post(url, headers=headers, json=json_body)

    client = Client(host='localhost')

    schema = {
        'posting_number': 'String',
        'etgb_number': 'String',
        'date': 'String',
        'url': 'String',
    }

    client.execute(
        'CREATE TABLE IF NOT EXISTS etgb3 (posting_number String, etgb_number String, date String, url String) '
        'ENGINE = ReplacingMergeTree() ORDER BY (posting_number)')

    df_list = []

    for posting in response['result']:
        row = {
            'posting_number': posting['posting_number'],
            'etgb_number': posting['etgb']['number'],
            'date': posting['etgb']['date'],
            'url': posting['etgb']['url'],
        }
        df_list.append(row)

    data_frame = pandas.DataFrame(df_list, columns=schema.keys())
    data = [i for _, i in data_frame.iterrows()]
    client.execute('INSERT INTO etgb3 (posting_number, etgb_number, date, url) VALUES', data)
    client.execute('OPTIMIZE TABLE etgb3 DEDUPLICATE')
    result = client.execute("SELECT * FROM etgb3")
