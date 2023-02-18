import os
import sqlite3

connection = sqlite3.connect(os.path.join("db", "configs.db"))
cursor = connection.cursor()

def add(tg_id: int, granat_name: str, jwt: str):
	cursor.execute("INSERT INTO data VALUES('{}', {token}, '{jwt}')".format(granat_name, token = tg_id, jwt = jwt))
	connection.commit()

def get_granat_name_by_telegram_id(tg_id: int):
	granat_name = cursor.execute(f"SELECT granat_name FROM data WHERE telegram_chat_id = {tg_id}").fetchall()
	if granat_name:
		return granat_name[0][0]
	return False

def get_telegram_id_by_granat_name(granat_name: str):
	telegram_id = cursor.execute(f"SELECT telegram_chat_id FROM data WHERE granat_name = '{granat_name}'").fetchall()
	if telegram_id:
		return telegram_id[0][0]
	return False

def jwt_token_by_granat_name(granat_name: str):
	jwt_token = cursor.execute(f"SELECT jwt FROM data WHERE granat_name = '{granat_name}'").fetchall()
	if jwt_token:
		return jwt_token[0][0]
	return False

def get_counter():
	return cursor.execute("SELECT COUNT(*) FROM data").fetchall()[0][0]