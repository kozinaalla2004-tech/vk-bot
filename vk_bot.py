import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload
import random
import logging
from datetime import datetime, timedelta

# === ЛОГИРОВАНИЕ ===
logging.basicConfig(level=logging.INFO)

# === НАСТРОЙКИ ===
VK_TOKEN = 'vk1.a.LKI0bvHWFlVamJQb-L8_k9HpPwRquBjAus3KxWxMHl40LsAJJfYsSl_3Qcq_WZHpwOKFqVB5uvmUp7zSy4m5sauhsGBKprGd9aKcubqXcy6sh8VoxO2glAHVpMPgx3obTIyoi71T3yXcNZLCotUheNdwbYih2DJcy8Y7DW8q3SHmyzMWteV8jIZun8tSHfAkLNzv7ku2H2fkokWG8Lw6ZQ'  # ← ВСТАВЬ СВОЙ ТОКЕН
GROUP_ID = 236725121  # ← ВСТАВЬ СВОЙ ID (без минуса!)

# Инициализация
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
upload = VkUpload(vk_session)

# === БАЗА ПОЛЬЗОВАТЕЛЕЙ ===
users_data = {}

# === ЗАДАНИЯ (20 штук) ===
daily_tasks = [
    {"text": "📝 Откликнись на 3 вакансии сегодня", "xp": 30},
    {"text": "🎓 Изучи новый навык (30 минут)", "xp": 25},
    {"text": "💼 Обнови своё резюме", "xp": 35},
    {"text": "🤝 Напиши бывшему коллеге или одногруппнику", "xp": 20},
    {"text": "📚 Прочитай статью по своей профессии", "xp": 15},
    {"text": "🎯 Определи 3 карьерные цели на месяц", "xp": 25},
    {"text": "💡 Пройди один профориентационный тест", "xp": 30},
    {"text": "📧 Напиши сопроводительное письмо для мечты", "xp": 40},
    {"text": "🔍 Изучи 5 компаний, где хочешь работать", "xp": 20},
    {"text": "🗣️ Потренируйся отвечать на вопросы на собеседовании", "xp": 25},
    {"text": "✍️ Напиши пост о своём профессиональном пути", "xp": 30},
    {"text": "🎬 Посмотри вебинар по твоей специальности", "xp": 35},
    {"text": "📊 Проанализируй свои сильные и слабые стороны", "xp": 20},
    {"text": "🌐 Найди 3 профессиональных сообщества", "xp": 15},
    {"text": "📞 Позвони ментору или наставнику", "xp": 25},
    {"text": "📋 Составь план развития на квартал", "xp": 40},
    {"text": "🎨 Создай или обнови портфолио", "xp": 45},
    {"text": "💬 Напиши отзыв о курсе/книге", "xp": 20},
    {"text": "🔗 Добавь 5 новых контактов", "xp": 30},
    {"text": "🧘 Практикуй самопрезентацию (2 мин)", "xp": 15},
]

# === ВАКАНСИИ (10 штук) ===
vacancies = [
    {"title": "SMM-менеджер", "company": "Digital Agency", "desc": "Ведение соцсетей, создание контента", "link": "https://vk.com", "salary": "60-90 тыс. ₽"},
    {"title": "Python-разработчик", "company": "TechStart", "desc": "Разработка ботов, парсеров, API", "link": "https://vk.com", "salary": "80-120 тыс. ₽"},
    {"title": "HR-ассистент", "company": "HR Pro", "desc": "Помощь в подборе персонала", "link": "https://vk.com", "salary": "50-70 тыс. ₽"},
    {"title": "Контент-менеджер", "company": "Media House", "desc": "Наполнение сайта и соцсетей", "link": "https://vk.com", "salary": "45-65 тыс. ₽"},
    {"title": "Графический дизайнер", "company": "Creative Studio", "desc": "Дизайн для соцсетей и веба", "link": "https://vk.com", "salary": "70-100 тыс. ₽"},
    {"title": "Маркетолог-аналитик", "company": "Growth Lab", "desc": "Анализ рекламных кампаний", "link": "https://vk.com", "salary": "75-110 тыс. ₽"},
    {"title": "Технический писатель", "company": "DocuTech", "desc": "Написание документации", "link": "https://vk.com", "salary": "55-80 тыс. ₽"},
    {"title": "Project Manager", "company": "Agile Team", "desc": "Управление проектами", "link": "https://vk.com", "salary": "90-140 тыс. ₽"},
    {"title": "UX/UI дизайнер", "company": "Design Hub", "desc": "Проектирование интерфейсов", "link": "https://vk.com", "salary": "85-130 тыс. ₽"},
    {"title": "Data Analyst", "company": "DataFlow", "desc": "Анализ данных, визуализация", "link": "https://vk.com", "salary": "95-150 тыс. ₽"},
]

# === ПОЛЕЗНЫЕ СОВЕТЫ ===
weekly_tips = [
    "💡 Лайфхак: Откликайся на вакансии до 10 утра — рекрутеры чаще смотрят резюме в начале дня!",
    "💡 Лайфхак: Добавляй цифры в резюме — «увеличил охват на 40%» работает лучше, чем просто «работал с охватом».",
    "💡 Лайфхак: Исследуй компанию перед собеседованием — задавай умные вопросы о продукте.",
    "💡 Лайфхак: Нетворкинг важнее резюме — 70% вакансий закрываются по рекомендациям.",
    "💡 Лайфхак: Делай паузы в поиске работы — выгорание снижает качество откликов.",
    "💡 Лайфхак: Сохраняй все отказы — анализируй, что можно улучшить.",
]

# === ДОСТИЖЕНИЯ ===
achievements = {
    "first_start": "🐣 Первый шаг",
    "first_task": "✅ Дело сделано",
    "first_feedback": "💬 Голос услышан",
    "first_match": "🎯 Первый отклик",
    "week_streak": "🔥 Неделя в игре",
}

# === НАВЫКИ ===
template_skills = [
    "💬 Коммуникация",
    "🤝 Работа в команде",
    "⏰ Тайм-менеджмент",
    "🐍 Python",
    "🇬🇧 Английский",
    "📊 Excel",
    "🎨 Дизайн",
    "📈 Аналитика",
]

skill_levels = {1: "🌱 Новичок", 2: "📚 Изучаю", 3: "💪 Практикую", 4: "🎯 Продвинутый", 5: "🏆 Эксперт"}

# === КЛАВИАТУРЫ ===
def get_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('💼 Вакансии', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📋 Задание дня', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🧪 Тесты', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🏆 Мой прогресс', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📄 Резюме', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🛠️ Навыки', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🎤 Собеседование', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('✉️ Сопроводительное', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📬 Полезное', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('💬 Обратная связь', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def get_vacancy_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('❌ Не подходит', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('✅ Подходит', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('⏭️ Далее', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🛑 Стоп', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_task_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('✅ Выполнил!', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('🔄 Другое', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()

# === ФУНКЦИИ ===
def get_user_data(user_id):
    if user_id not in users_data:
        users_data[user_id] = {
            "xp": 0, "level": 1, "tasks_completed": 0,
            "achievements": [], "streak": 0, "last_visit": None,
            "current_vacancy": 0, "matched_vacancies": [],
            "completed_tasks": [], "waiting_feedback": False, "username": None,
            "test_result": None, "resume_checklist": [False]*8,
            "skills": {}, "custom_skills": [],
            "interview_completed": 0, "last_streak_check": None,
            "cover_letter_data": {}, "last_weekly_tip": None
        }
    return users_data[user_id]

def add_xp(user_id, amount):
    user = get_user_data(user_id)
    user["xp"] += amount
    new_level = (user["xp"] // 100) + 1
    if new_level > user["level"]:
        user["level"] = new_level
        return True
    return False

def send_message(user_id, text, keyboard=None):
    try:
        vk.messages.send(
            user_id=user_id,
            message=text,
            keyboard=keyboard,
            random_id=random.randint(0, 2**31)
        )
        return True
    except Exception as e:
        logging.error(f"Ошибка отправки: {e}")
        return False

# === ОБРАБОТЧИКИ ===
def handle_start(user_id, user_name):
    user = get_user_data(user_id)
    
    if user["last_visit"] is None:
        user["achievements"].append("first_start")
        add_xp(user_id, 50)
        user["username"] = user_name
    
    user["last_visit"] = datetime.now()
    user["current_vacancy"] = 0
    
    # Сообщение 1
    send_message(user_id, f"Привет, {user_name}! 🖤\n\nЯ Ворон Кар — твой карьерный наставник!")
    
    # Сообщение 2
    send_message(user_id, "Я — ворон, и я знаю, каково это: быть запутанным...\n\nНо я прошёл этот путь и теперь стал экспертом! 🎯\n\nТеперь я помогаю таким же, как ты.")
    
    # Сообщение 3
    send_message(user_id, 
        "В этом боте ты можешь:\n\n"
        "💼 Найти вакансии\n"
        "📋 Получать задания\n"
        "🧪 Пройти тесты\n"
        "🏆 Отслеживать прогресс\n"
        "📄 Создать резюме\n"
        "🛠️ Трекер навыков\n"
        "🎤 Симулятор собеседования\n"
        "✉️ Сопроводительное письмо\n"
        "📬 Полезное\n"
        "💬 Обратная связь\n\n"
        "Выбирай раздел в меню 👇",
        get_main_keyboard()
    )

def handle_vacancies(user_id):
    user = get_user_data(user_id)
    
    if user["current_vacancy"] >= len(vacancies):
        send_message(user_id, "🎉 Все вакансии просмотрены!")
        return
    
    vac = vacancies[user["current_vacancy"]]
    text = f"💼 {vac['title']}\n🏢 {vac['company']}\n💰 {vac['salary']}\n\n📝 {vac['desc']}"
    
    send_message(user_id, text, get_vacancy_keyboard())

def handle_tasks(user_id):
    user = get_user_data(user_id)
    available = [i for i in range(len(daily_tasks)) if i not in user["completed_tasks"]]
    
    if not available:
        send_message(user_id, "🎉 Все задания выполнены!\n\nЗаходи завтра за новыми!")
        return
    
    task_id = random.choice(available)
    task = daily_tasks[task_id]
    text = f"📋 Задание:\n\n{task['text']}\n\n⚡ +{task['xp']} XP"
    
    send_message(user_id, text, get_task_keyboard())

def handle_progress(user_id):
    user = get_user_data(user_id)
    achievements_list = "\n".join([achievements[a] for a in user["achievements"]]) if user["achievements"] else "Пока нет"
    
    text = (f"🏆 Твой прогресс:\n\n"
            f"📊 Уровень: {user['level']}\n"
            f"⚡ XP: {user['xp']} / {user['level'] * 100}\n"
            f"🔥 Стрик: {user['streak']} дней\n"
            f"✅ Заданий: {user['tasks_completed']}\n"
            f"💕 Вакансий: {len(user['matched_vacancies'])}\n\n"
            f"🏅 Достижения:\n{achievements_list}")
    
    send_message(user_id, text)

def handle_tests(user_id):
    user = get_user_data(user_id)
    
    if user.get("test_result"):
        send_message(user_id, f"🧪 Твой результат: {user['test_result']}\n\n🔁 Пройти заново? Напиши 'тест'")
    else:
        send_message(user_id, "🧪 Тест профориентации\n\nОтветь на 3 вопроса и узнай, какая профессия тебе подходит!\n\n⏱️ Время: 2 минуты\n⚡ Награда: 100 XP\n\nНапиши 'начать тест'")

def handle_skills(user_id):
    user = get_user_data(user_id)
    text = "🛠️ Твои навыки\n\n"
    
    if user["skills"]:
        for skill_name, level in user["skills"].items():
            level_name = skill_levels.get(level, "🌱 Новичок")
            text += f"{level_name} — {skill_name} (уровень {level}/5)\n"
    else:
        text += "Пока нет навыков. Добавь первый!\n\nНапиши 'добавить навык [название]'"
    
    send_message(user_id, text)

def handle_useful(user_id):
    tip = random.choice(weekly_tips)
    send_message(user_id, tip)

# === ОСНОВНОЙ ЦИКЛ ===
def main():
    print("\n" + "="*50)
    print("🖤 Ворон Кар (VK) запущен...")
    print(f"👥 Сообщество ID: {GROUP_ID}")
    print("="*50 + "\n")
    
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.obj.message
                user_id = message['from_id']
                user_name = message.get('peer_id')  # Получаем имя из сообщения
                text = message['text'].lower().strip()
                
                logging.info(f"Сообщение от {user_id}: {text}")
                
                # Обработка команд
                if text in ['привет', '/start', 'старт']:
                    handle_start(user_id, f"пользователь {user_id}")
                
                elif text == '💼 вакансии' or text == 'вакансии':
                    handle_vacancies(user_id)
                
                elif text == '📋 задание дня' or text == 'задание':
                    handle_tasks(user_id)
                
                elif text == '🏆 мой прогресс' or text == 'прогресс':
                    handle_progress(user_id)
                
                elif text == '🧪 тесты' or text == 'тест':
                    handle_tests(user_id)
                
                elif text == '🛠️ навыки' or text == 'навыки':
                    handle_skills(user_id)
                
                elif text == '📬 полезное' or text == 'полезное':
                    handle_useful(user_id)
                
                elif text == '💬 обратная связь' or text == 'обратная связь':
                    send_message(user_id, "💬 Твоё мнение важно!\n\nНапиши свой отзыв, и я всё прочитаю! 🖤")
                    user = get_user_data(user_id)
                    user["waiting_feedback"] = True
                
                elif text == '✅ выполнил!':
                    user = get_user_data(user_id)
                    available = [i for i in range(len(daily_tasks)) if i not in user["completed_tasks"]]
                    if available:
                        task_id = random.choice(available)
                        user["completed_tasks"].append(task_id)
                        user["tasks_completed"] += 1
                        xp = daily_tasks[task_id]["xp"]
                        add_xp(user_id, xp)
                        send_message(user_id, f"✅ Выполнено!\n\n+{xp} XP")
                
                elif text.startswith('❌') or text.startswith('не подходит'):
                    user = get_user_data(user_id)
                    user["current_vacancy"] += 1
                    handle_vacancies(user_id)
                
                elif text.startswith('✅') or text.startswith('подходит'):
                    user = get_user_data(user_id)
                    vac_id = user["current_vacancy"]
                    if vac_id < len(vacancies):
                        if vac_id not in user["matched_vacancies"]:
                            user["matched_vacancies"].append(vac_id)
                        user["current_vacancy"] += 1
                        add_xp(user_id, 20)
                        send_message(user_id, f"✅ Отлично!\n\n{vacancies[vac_id]['title']}\n\n🔗 {vacancies[vac_id]['link']}\n\n⚡ +20 XP")
                        handle_vacancies(user_id)
                
                elif text == '⏭️ далее' or text == 'далее':
                    user = get_user_data(user_id)
                    user["current_vacancy"] += 1
                    handle_vacancies(user_id)
                
                elif text == '🛑 стоп' or text == 'стоп':
                    user = get_user_data(user_id)
                    send_message(user_id, f"🛑 Остановлено!\n\n💕 В избранном: {len(user['matched_vacancies'])}\n👀 Посмотрено: {user['current_vacancy'] + 1}")
                
                elif user.get("waiting_feedback", False):
                    send_message(user_id, "Спасибо! Твой отзыв сохранён 🖤\n\n⚡ +20 XP")
                    user["waiting_feedback"] = False
                
                else:
                    send_message(user_id, "Используй кнопки внизу или напиши 'привет'", get_main_keyboard())
        
        except Exception as e:
            logging.error(f"Ошибка обработки: {e}")
            continue

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")