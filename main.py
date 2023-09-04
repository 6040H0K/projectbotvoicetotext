import telebot
from voice import handler_voice
import json
from settings import bot
import random
# Зчитуємо інформацію про користувачів з JSON файлу (якщо він існує)
try:
	with open('users.json', 'r') as file:
		users = json.load(file)
except FileNotFoundError:
	users = {}



@bot.message_handler(commands=['start'])
def handle_start(message):
	user_id = str(message.from_user.id)
	if user_id:
		with open('users.json', 'r') as file:
			users_json = json.load(file)
		if user_id not in users_json.keys():
			users[user_id] = {'free_voice_messages': 10, 'free_translate': 20}
			with open('users.json', 'w') as file:
				json.dump(users, file, indent=4)

	bot.send_message(message.chat.id,
		f'''Ласкаво просимо! У вас залишилося {users[user_id]["free_voice_messages"]} безкоштовних голосових повідомлень. '''
		)


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
	user_id = str(message.from_user.id)
	if user_id in users and users[user_id]['free_voice_messages'] > 0:
		handler_voice(message)
		users[user_id]['free_voice_messages'] -= 1
		with open('users.json', 'w') as file:
			json.dump(users, file, indent=4)
		bot.send_message(message.chat.id,
						 f'Голосове повідомлення прийнято. '
						 f'Залишилося {users[user_id]["free_voice_messages"]} ')
	elif user_id in users and users[user_id]['free_voice_messages'] == 0:
		bot.send_message(message.chat.id, 'Ви вже використали всі безкоштовні '
										  'голосові повідомлення. '
										  f'Введіть /ad щоб продивитись рекламу'
										  f'та отримати ще 10 бещкоштовних голосових повідомлень')
		
@bot.message_handler(commands=["ad"])
def ad_handler(message):
	global users
	with open ('users.json','r') as file:
		user_json = json.load(file)
	if str(message.chat.id) in user_json.keys():
		with open('ad.json', 'r') as file:
			ad = json.load(file)
		random_key = random.choice(list(ad.keys()))
		bot.send_message(message.chat.id, f'<strong>{random_key}</strong>\n\n{ad[random_key]}',
				   parse_mode='html')
		user_json[str(message.chat.id)]["free_voice_messages"] += 10

		with open ('users.json', 'w') as file:
			json.dump(user_json, file, indent=4)
			users = user_json
if __name__ == '__main__':
	bot.polling(none_stop=True)
