# import telebot
# import requests
#
#
#
# TOKEN = '1314633248:AAFv6dBnI0vsJA4Uetfra3EtEC29rbrFn2g'
# TelegramBot = telebot.TeleBot(TOKEN)
# CHAT_ID = "-1001416713211"
# URL = 'https://api.telegram.org/bot'
#
#
# def send_massages(text):
#     requests.get(f'{URL}{TOKEN}/sendMessage',
#                  params=dict(
#                      chat_id=CHAT_ID,
#                      text=text
#                  ))
#     return 'Сообщение отправленно'


# def send_massages_to_telegram(text):
#     token = TOKEN
#     url = "https://api.telegram.org/bot"
#     channel_id = "@test_CRAFT_bot"
#     url += token
#     method = url + "/sendMessage"
#
#     r = requests.post(method, data={
#         "chat_id": channel_id,
#         "text": text
#     })
#
#     if r.status_code != 200:
#         raise Exception("post_text error")
