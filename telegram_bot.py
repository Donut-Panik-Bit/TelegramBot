#! /usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram import Bot, Dispatcher, executor, types
import db
import backend

TOKEN = "6098824044:AAEVhw4tU3uhOfPyS9fpUHcgLMim6MZb7jc"

def check_deep(text: str) -> tuple:
    sp = text.split()
    if len(sp) == 1:
        return False, None
    else:
        return True, sp[-1]
    
btn_profile = types.KeyboardButton("[X]]Мой профиль")
btn_write = types.KeyboardButton("✍️Дополнить заявку")
btn_media = types.KeyboardButton("[X]Медиа")
btn_money = types.KeyboardButton("[X]Софинансирование")
btn_files = types.KeyboardButton("[X]]Доп. Файлы")
btn_expenses = types.KeyboardButton("[X]Расходы")

btn_about = types.KeyboardButton("[X]Общее")
btn_about_project = types.KeyboardButton("☝️О проекте")
btn_team = types.KeyboardButton("[X]Команда")
btn_results = types.KeyboardButton("[X]Результаты")
btn_calendar = types.KeyboardButton("[X]Календарный план")

mkup_main = types.ReplyKeyboardMarkup().add(btn_profile)\
    .add(btn_write)\
        .add(btn_media)\
            .add(btn_money)\
                .add(btn_files)\
                    .add(btn_expenses)

mkup_write = types.ReplyKeyboardMarkup().add(btn_about)\
    .add(btn_about_project)\
        .add(btn_team)\
            .add(btn_results)\
                .add(btn_calendar)

# О проекте
inlbtn_kratk_info_o_proekt = types.InlineKeyboardButton("Краткая информация о проекте", callback_data="inlkratk_info_o_proekt")
inlbtn_opis_probl = types.InlineKeyboardButton("Описание проблемы", callback_data='opisprobl')
inlbtn_osnov_cel_group = types.InlineKeyboardButton("Основные целевые группы", callback_data='osnov_cel_group')
inlbtn_osnov_cel_proekt = types.InlineKeyboardButton("Основная цель проекта", callback_data='osnov_cel_proekt')
inlbtn_opit_uspesh_real = types.InlineKeyboardButton("Опыт успешной реализации проекта", callback_data='opit_uspesh_real')
inlbtn_perspective_razvit = types.InlineKeyboardButton("Перспектива развития и потенциал проекта", callback_data='perspective_razvit')

inlmkup_about_project = types.InlineKeyboardMarkup()\
    .add(inlbtn_kratk_info_o_proekt)\
        .add(inlbtn_opis_probl)\
            .add(inlbtn_osnov_cel_group)\
                .add(inlbtn_osnov_cel_proekt)\
                    .add(inlbtn_opit_uspesh_real)\
                        .add(inlbtn_perspective_razvit)



class GranatCatBot:

    bot = None
    redact_now = False
    redact_status_code = None
    
    def __init__(self, tg_token):
        self.bot = Bot(token = tg_token)
    
    async def send_welcome(self, message: types.Message):

        user_id = message.from_user.id # Получаем telegram_id

        its_deeplink, result_deeplink = check_deep(message.text)

        registered = db.get_granat_name_by_telegram_id(user_id)

        if registered:
            await message.answer("Вы уже зарегистрированы!", reply_markup = mkup_main)
        else:
            if its_deeplink:
                jwt_token = backend.login(result_deeplink)
                db.add(user_id, result_deeplink, jwt_token)
                await message.answer("Теперь вы зарегистрированы!", reply_markup = mkup_main)
            else:
                await message.answer("Что-то пошло не так")

    async def check(self, message: types.Message):
        await self.send_message_to_granat_user("hui", "HUIHUI!!")
        await message.answer("Checked!")
    
    async def commands(self, message: types.Message):
        if not self.redact_now:
            #if message.text == "Мой профиль":
            #    await message.answer("Ваш профиль:\n\n\nчёта короче")
            if message.text == "✍️Дополнить заявку":
                await message.answer("Общая информация\n\n\nРасполагается здесь!", reply_markup = mkup_write)
            #elif message.text == "💻Медиа":
            #    await message.answer("Медиа:\n\n\nчёта короче")
            if message.text == "☝️О проекте":
                await message.answer("Добавьте заметку в любом из следующих пунктов:", reply_markup = inlmkup_about_project)
            #else:
            #    await message.answer("Неизвестная команда!", reply_markup = mkup_main)
        else:
            await self.stop_redact(message)
    
    def detect_what_change(self, string: str):
        if string == "inlkratk_info_o_proekt":
            return 1, "Краткая информация о проекте"
        elif string == "opisprobl":
            return 2, "Описание проблемы"
        elif string == "osnov_cel_group":
            return 3, "Основные целевые группы"
        elif string == "osnov_cel_proekt":
            return 4, "Основная цель проекта"
        elif string == "opit_uspesh_real":
            return 5, "Опыт успешной реализации проекта"
        elif string == "perspective_razvit":
            return 6, "Перспектива развития и потенциал проекта"
        else:
            return 0, None


    async def process_callback_about_project(self, callback_query: types.CallbackQuery):

        code = callback_query.data

        status_code, text = self.detect_what_change(code)
        self.redact_now = True
        self.redact_status_code = status_code

        text = f"Вы дополняете поле **{text}**:"

        await self.bot.send_message(callback_query["from"]["id"], "Просто отправьте новую заметку")
    
    async def stop_redact(self, message: types.Message):
        
        note = f"\nЗаметка: {message.text}"

        granat_name = db.get_granat_name_by_telegram_id(message.from_id)
        json = backend.get_json_project(granat_name)
        
        if self.redact_status_code == 1:
            json["brief_information"] += note
        elif self.redact_status_code == 2:
            json["descrip_problem"] += note
        elif self.redact_status_code == 3:
            json["primary_goal"] += note
        elif self.redact_status_code == 4:
            json["major_groups"] += note
        elif self.redact_status_code == 5:
            json["implementation_experience"] += note
        elif self.redact_status_code == 6:
            json["project_potential"] += note
        
        backend.set_json_project(granat_name, json)
        
        self.redact_now = False
        self.redact_status_code = 0
        
        await message.answer("Заметка успешно сохранена")


    async def send_message_to_granat_user(self, granat_name: str, text: str):
        telegram_id = db.get_telegram_id_by_granat_name(granat_name)
        if telegram_id:
            await self.bot.send_message(telegram_id, text)
            return True
        return False
    
    
    def start(self):
        dp = Dispatcher(self.bot)
        dp.register_message_handler(self.send_welcome, commands = ['start'])
        dp.register_message_handler(self.check, commands = ['check'])
        dp.register_message_handler(self.commands, content_types = ['text'])
        dp.register_callback_query_handler(self.process_callback_about_project, lambda smth: True)

        executor.start_polling(dp, skip_updates = True)

if __name__ == "__main__":
    g = GranatCatBot(TOKEN)
    g.start()