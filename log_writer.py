from aiogram import types


async def save_log(message: types.Message, *arg):
    match arg[0]:
        case "start_waiting_to_write":
            with open("log.txt", "a", encoding="utf-8") as fil:
                fil.write(
                    f"Wait to send message from id = {message.chat.id} username = {message.from_user.username} "
                    f"to id = {arg[1]} username = {arg[2]}\n")

        case "satrt_get_message":
            with open("log.txt", "a", encoding="utf-8") as fil:
                fil.write(
                    f"Start to get messages from id = {message.chat.id} username = {message.from_user.username}\n")

        case "send_anon_message":
            with open("log.txt", "a", encoding="utf-8") as fil:
                fil.write(f"Send message from id = {message.chat.id} username = {message.from_user.username} "
                          f"to id = {arg[1]} username = {arg[2]} : {message.html_text}\n")

        case "send_anon_answer":
            with open("log.txt", "a", encoding="utf-8") as fil:
                fil.write(f"Answer on message id = {message.chat.id} username = {message.from_user.username} "
                          f"to id = {arg[1]} : {message.html_text}\n")

        case "bad_address":
            with open("log.txt", "a", encoding="utf-8") as fil:
                fil.write(f"Bad request to send message to {arg[1]} from id = {arg[2]} username = {arg[3]}\n")

        case "stop_wait":
            with open("log.txt", "a", encoding="utf-8") as fil:
                fil.write(f"Stop waiting from id = {message.chat.id} username = {message.from_user.username}\n")

        case "message":
            with open("log.txt", "a", encoding="utf-8") as fil:
                fil.write(f"Just message from id = {message.chat.id} username = {message.from_user.username} : {message.html_text}\n")

