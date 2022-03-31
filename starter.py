# -*- coding: utf-8 -*-

import datetime, json, time, logging
import main

#Загрузка всех аккаунтов для авторизаций
with open('configurations/accounts_config.json', 'r') as openfile:
    accounts = json.load(openfile)

captcha_key = "КЛЮЧ ОТ CAPMONSTERCLOUD"

# Log path to filename, with today date
log_path = r'logs/logs_{}{}'.format(str(time.strftime('%d-%m-%Y')), '.log')

# Logging config file
logging.basicConfig(filename=log_path, level=logging.INFO,
                    format='%(asctime)s : %(levelname)s : %(message)s')

def schedule_script(timestamp):
    start_time = f"{datetime.date.today().strftime('%Y-%m-%d')} {timestamp}"
    script_exc_timestamp = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    return int(script_exc_timestamp.timestamp())

print(f"Текущее время на вашем сервере/пк {datetime.datetime.fromtimestamp(int(time.time())):%d.%m.%Y %H:%M:%S}")

requests_timestamp = input("Укажите время для запуска покупки (Пример: 10:00:12): ")

for i in range(len(accounts)):
    main.GameFiBuy(captcha_key, accounts[i], schedule_script(requests_timestamp)).start()