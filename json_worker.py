import json


# Добавить в ожидание отправки
def add_in_order_of_waiting(from_chat: int, to_chat: int):
    from_chat = str(from_chat)
    with open("db.json", "r") as db:
        diction = json.load(db)
        diction["waiting_to_send"][from_chat] = to_chat

    with open("db.json", "w") as db:
        json.dump(diction, db, indent=4)


# Удалить из ожидания отправки
def del_from_order_of_waiting(from_chat: int):
    from_chat = str(from_chat)
    with open("db.json", "r") as db:
        diction = json.load(db)
        if from_chat in diction["waiting_to_send"]:
            del diction["waiting_to_send"][from_chat]

    with open("db.json", "w") as db:
        json.dump(diction, db, indent=4)


# Узнать получателя
def get_chat(from_chat: int) -> int:
    from_chat = str(from_chat)
    with open("db.json", "r") as db:
        diction = json.load(db)
        if from_chat in diction["waiting_to_send"]:
            return diction["waiting_to_send"][from_chat]


# Есть ли ожидание на отправку
def is_message_on_order(from_chat: int) -> bool:
    from_chat = str(from_chat)
    with open("db.json", "r") as db:
        diction = json.load(db)
        return from_chat in diction["waiting_to_send"]


# Добавить нового адресата в список
def add_new_address(chat_id: int, username: str):
    chat_id = str(chat_id)

    with open("db.json", "r") as db:
        diction = json.load(db)
        if chat_id not in diction["addresses"]:
            diction["addresses"][chat_id] = username

    with open("db.json", "w") as db:
        json.dump(diction, db, indent=4)


# Есть ли адресат в списке
def is_address_in_list(chat_id: int) -> bool:
    chat_id = str(chat_id)

    with open("db.json", "r") as db:
        diction = json.load(db)
        return chat_id in diction["addresses"]


# Получить имя адресата
def get_username(chat_id: int) -> str:
    chat_id = str(chat_id)

    with open("db.json", "r") as db:
        diction = json.load(db)
        return diction["addresses"][chat_id]


# Добавить сообщение в список для ответов
def add_new_message_to_ans(mes_to_ans: int, chat_id: int, mes_id: int):
    mes_to_ans = str(mes_to_ans)

    with open("db.json", "r") as db:
        diction = json.load(db)
        diction["answer_on_message"][mes_to_ans] = [chat_id, mes_id]
    with open("db.json", "w") as db:
        json.dump(diction, db, indent=4)


# Получить chat_id и message_id для ответа
def get_data_to_ans(mes_to_ans: int) -> [int, int]:
    mes_to_ans = str(mes_to_ans)

    with open("db.json", "r") as db:
        diction = json.load(db)
        return diction["answer_on_message"][mes_to_ans]


# Есть ли сообщение в списке для ответов
def is_mes_in_ans_list(mes_to_ans: int) -> bool:
    mes_to_ans = str(mes_to_ans)

    with open("db.json", "r") as db:
        diction = json.load(db)
        return mes_to_ans in diction["answer_on_message"]
