# Этот скрипт очищает все данные

import json


with open("log.txt", "w") as log:
    log.close()


data = {
    "waiting_to_send": {},
    "addresses": {},
    "answer_on_message": {}
}

with open("db.json", "w") as db:
    json.dump(data, db, indent=4)
