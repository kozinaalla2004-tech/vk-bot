import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import logging
from datetime import datetime
from flask import Flask
import threading
import os

# === ЛОГИРОВАНИЕ ===
logging.basicConfig(level=logging.INFO)

# === FLASK (для Render) ===
app = Flask(__name__)

@app.route('/')
def index():
    return "🖤 Бот Ворон Кар работает! VK API active."

@app.route('/health')
def health():
    return "OK"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# === НАСТРОЙКИ ===
VK_TOKEN = os.environ.get('VK_TOKEN', 'vk1.a.agr3ybcPZs9l_lQ1mjy_lCcPu6TFPYQqjNY-eElqLpM05PzxXBdHGsdRss4aF3Fxj_vxr9hHdKiPfBXRZO-YwB7HCDVfWKAl5e_Fq_QNWBTSiMz72uvcfdZ6a8XqqoEawr9sg0wf954Ey0xDglS0K1Z16PgOvxHBGHC9imv7iiiS1vQOL7rsf_iMP3Y11LwPrTX2MsOsxkmVDrGoJdkvhw')
GROUP_ID = 236725121
ADMIN_VK_ID = 355647886  # ← Вставь свой VK ID

# Инициализация
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

# === БАЗА ПОЛЬЗОВАТЕЛЕЙ ===
users_data = {}

# === ЗАДАНИЯ (20 штук) ===
daily_tasks = [
    {"text": "📝 Откликнись на 3 вакансии сегодня", "xp": 30, "instruction": "1. Открой раздел «Вакансии»\n2. Выбери 3 подходящие\n3. Нажми «✅ Подходит»"},
    {"text": "🎓 Изучи новый навык (30 минут)", "xp": 25, "instruction": "1. Открой «📚 Ресурсы» → «Курсы»\n2. Выбери бесплатный урок\n3. Посмотри 30 минут"},
    {"text": "💼 Обнови своё резюме", "xp": 35, "instruction": "1. Открой резюме на HH.ru\n2. Добавь достижения\n3. Проверь контакты"},
    {"text": "🤝 Напиши бывшему коллеге", "xp": 20, "instruction": "1. Вспомни 2-3 человека\n2. Напиши: «Привет! Как дела?»\n3. Предложи созвониться"},
    {"text": "📚 Прочитай статью по профессии", "xp": 15, "instruction": "1. Найди статью по специальности\n2. Прочитай внимательно\n3. Выдели 2-3 идеи"},
]

# === ВАКАНСИИ (10 штук) ===
vacancies = [
    {"title": "SMM-менеджер", "company": "Digital Agency", "desc": "Ведение соцсетей, создание контент-плана", "requirements": "• Опыт от 1 года\n• Знание ВКонтакте, Telegram\n• Навыки копирайтинга", "salary": "60-90 тыс. ₽", "link": "https://vk.com", "tips": "💡 Укажи примеры работ"},
    {"title": "Python-разработчик", "company": "TechStart", "desc": "Разработка ботов, парсеров, API", "requirements": "• Знание Python 3.x\n• Опыт с aiogram/vk_api\n• Git, REST API", "salary": "80-120 тыс. ₽", "link": "https://vk.com", "tips": "💡 Приложи GitHub"},
    {"title": "HR-ассистент", "company": "HR Pro", "desc": "Скрининг резюме, собеседования", "requirements": "• Коммуникабельность\n• Внимательность\n• Опыт с людьми", "salary": "50-70 тыс. ₽", "link": "https://vk.com", "tips": "💡 Подчеркни многозадачность"},
    {"title": "Контент-менеджер", "company": "Media House", "desc": "Наполнение сайта и соцсетей", "requirements": "• Грамотная речь\n• WordPress/Tilda\n• Базовый визуал", "salary": "45-65 тыс. ₽", "link": "https://vk.com", "tips": "💡 Покажи примеры"},
    {"title": "Графический дизайнер", "company": "Creative Studio", "desc": "Дизайн для соцсетей и веба", "requirements": "• Портфолио 5+ работ\n• Figma/Photoshop\n• Композиция", "salary": "70-100 тыс. ₽", "link": "https://vk.com", "tips": "💡 Приложи портфолио"},
]

# === ПОЛЕЗНЫЕ СОВЕТЫ ===
weekly_tips = [
    "💡 Откликайся на вакансии до 10 утра!",
    "💡 Добавляй цифры в резюме — «увеличил охват на 40%»!",
    "💡 Исследуй компанию перед собеседованием!",
    "💡 Нетворкинг важнее резюме — 70% вакансий по рекомендациям!",
    "💡 Делай паузы в поиске работы!",
]

# === ДОСТИЖЕНИЯ ===
achievements = {
    "first_start": "🐣 Первый шаг",
    "first_task": "✅ Дело сделано",
    "first_feedback": "💬 Голос услышан",
    "first_match": "🎯 Первый отклик",
    "week_streak": "🔥 Неделя в игре",
    "interview_pass": "🎤 Собеседование пройдено",
}

# === НАВЫКИ ===
template_skills = ["💬 Коммуникация", "🤝 Командная работа", "⏰ Тайм-менеджмент", "🐍 Python", "🇬🇧 Английский"]
skill_levels = {1: "🌱 Новичок", 2: "📚 Изучаю", 3: "💪 Практикую", 4: "🎯 Продвинутый", 5: "🏆 Эксперт"}

# === ТЕСТ ПРОФОРИЕНТАЦИИ ===
career_test_questions = [
    {"question": "Что тебе нравится больше?", "options": [{"text": "Работать с людьми", "type": "social"}, {"text": "Работать с данными", "type": "analytical"}, {"text": "Создавать новое", "type": "creative"}, {"text": "Управлять", "type": "managerial"}]},
    {"question": "Как ты работаешь?", "options": [{"text": "В команде", "type": "social"}, {"text": "Самостоятельно", "type": "analytical"}, {"text": "Свободно", "type": "creative"}, {"text": "По плану", "type": "managerial"}]},
    {"question": "Что важнее?", "options": [{"text": "Помогать", "type": "social"}, {"text": "Анализировать", "type": "analytical"}, {"text": "Творить", "type": "creative"}, {"text": "Достигать", "type": "managerial"}]},
]

career_test_results = {
    "social": {"title": "🤝 Социальный тип", "desc": "Тебе подходит работа с людьми!", "professions": ["HR-менеджер", "Психолог", "Учитель", "Коуч"]},
    "analytical": {"title": "📊 Аналитический тип", "desc": "Тебе подходит работа с данными!", "professions": ["Аналитик", "Программист", "Финансист", "Data Scientist"]},
    "creative": {"title": "🎨 Креативный тип", "desc": "Тебе подходит творческая работа!", "professions": ["Дизайнер", "Копирайтер", "Маркетолог", "Режиссёр"]},
    "managerial": {"title": "🎯 Управленческий тип", "desc": "Тебе подходит руководящая работа!", "professions": ["Project Manager", "Team Lead", "Предприниматель", "COO"]},
}

# === ВОПРОСЫ ДЛЯ СОБЕСЕДОВАНИЯ ===
interview_questions = [
    {"question": "Расскажите немного о себе", "tips": "Говори 2-3 минуты: образование → опыт → почему вакансия", "keywords": ["опыт", "образование", "работа", "интерес", "цель", "навык"], "example_answer": "Я окончил [вуз]. Последние [число] лет работал в [сфера]. Меня заинтересовала вакансия, потому что [причина]."},
    {"question": "Почему вы хотите работать у нас?", "tips": "Покажи, что изучил компанию", "keywords": ["компания", "ценности", "продукт", "культура", "развитие", "интерес"], "example_answer": "Мне нравится, что ваша компания [факт]. Я разделяю ценность [ценность]."},
    {"question": "Назовите сильные стороны", "tips": "Выбери 2-3 качества с примерами", "keywords": ["сильный", "навык", "умение", "опыт", "пример", "результат"], "example_answer": "Я организованный — вёл 3 проекта одновременно. Коммуникабельный — легко нахожу общий язык."},
    {"question": "Назовите слабые стороны", "tips": "Назови слабость + как работаешь над ней", "keywords": ["работаю", "улучшаю", "учусь", "развиваюсь", "практика"], "example_answer": "Иногда погружаюсь в детали. Но научился ставить таймеры и проверять приоритеты."},
    {"question": "Кем видите себя через 5 лет?", "tips": "Покажи амбиции, но будь реалистом", "keywords": ["развитие", "рост", "цель", "карьера", "профессионал", "эксперт"], "example_answer": "Через 5 лет вижу себя экспертом в [сфера], решающим сложные задачи."},
]

# === КАТАЛОГ РЕСУРСОВ ===
career_resources = {
    "курсы": ["🎓 Яндекс.Практикум — IT и маркетинг", "🎓 Stepik — бесплатные курсы", "🎓 Coursera — международные курсы"],
    "книги": ["📖 «Дизайн карьеры» Б. Бернетт", "📖 «Атомные привычки» Дж. Клир", "📖 «Гибкое сознание» К. Дуэк"],
    "инструменты": ["🛠️ HH.ru — поиск вакансий", "🛠️ Notion — планирование", "🛠️ Trello — задачи"],
    "сообщества": ["👥 «Карьера» ВКонтакте", "👥 «Профориентация»", "👥 «Молодые специалисты»"],
}

# === КЛАВИАТУРЫ ===
def get_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('💼 Вакансии', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📋 Задание дня', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🧪 Тесты', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🏆 Прогресс', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📄 Резюме', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🛠️ Навыки', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🎤 Собеседование', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('✉️ Сопроводительное', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📚 Ресурсы', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('📬 Полезное', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('💬 Обратная связь', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def get_vacancy_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('❌ Не подходит', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('✅ Подходит', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('⏭️ Далее', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🛑 Стоп', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_task_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('✅ Выполнил!', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('🔄 Другое', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_resources_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🎓 Курсы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Книги', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🛠️ Инструменты', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('👥 Сообщества', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_test_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_progress_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_skills_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_interview_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🎤 Начать практику', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_feedback_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_resume_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

# === ФУНКЦИИ ===
def get_user_data(user_id):
    if user_id not in users_data:
        users_data[user_id] = {
            "xp": 0, "level": 1, "tasks_completed": 0,
            "achievements": [], "streak": 0, "last_visit": None,
            "current_vacancy": 0, "matched_vacancies": [],
            "completed_tasks": [], "waiting_feedback": False,
            "test_result": None, "skills": {}, "interview_completed": 0,
            "first_message_time": datetime.now(),
            "test_answers": None, "test_current": 0,
            "interview_mode": False, "interview_question_idx": 0,
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
        params = {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 2**31)}
        if keyboard:
            params['keyboard'] = keyboard
        vk.messages.send(**params)
        return True
    except Exception as e:
        logging.error(f"Ошибка отправки: {e}")
        return False

def send_to_admin(text):
    try:
        vk.messages.send(user_id=ADMIN_VK_ID, message=text, random_id=random.randint(0, 2**31))
        logging.info("✅ Сообщение админу отправлено")
        return True
    except Exception as e:
        logging.error(f"❌ Ошибка отправки админу: {e}")
        return False

# === ОБРАБОТЧИКИ ===
def handle_start(user_id):
    user = get_user_data(user_id)
    if user["last_visit"] is None:
        user["achievements"].append("first_start")
        add_xp(user_id, 50)
        send_to_admin(f"🆕 Новый пользователь (ID: {user_id})")
    user["last_visit"] = datetime.now()
    user["current_vacancy"] = 0
    user["interview_mode"] = False
    user["test_answers"] = None
    
    send_message(user_id, "🖤 Я Ворон Кар — твой карьерный наставник!")
    send_message(user_id, "Я знаю, каково это: быть запутанным... Но я прошёл этот путь и теперь эксперт! 🎯")
    send_message(user_id, "В этом боте ты можешь:\n\n💼 Найти вакансии с требованиями\n📋 Получать задания с инструкциями\n🧪 Пройти тест профориентации\n🏆 Отслеживать прогресс\n📄 Создать резюме\n🛠️ Трекер навыков\n🎤 Симулятор собеседования\n✉️ Сопроводительное письмо\n📚 Каталог ресурсов\n📬 Еженедельные советы", get_main_keyboard())

def handle_vacancies(user_id):
    user = get_user_data(user_id)
    if user["current_vacancy"] >= len(vacancies):
        send_message(user_id, "🎉 Все вакансии просмотрены!\n\nЗаходи позже — будут новые! 🖤", get_main_keyboard())
        return
    vac = vacancies[user["current_vacancy"]]
    text = f"💼 {vac['title']}\n🏢 {vac['company']}\n💰 {vac['salary']}\n\n📝 Задачи:\n{vac['desc']}\n\n📋 Требования:\n{vac['requirements']}\n\n{vac['tips']}"
    send_message(user_id, text, get_vacancy_keyboard())

def handle_tasks(user_id):
    user = get_user_data(user_id)
    available = [i for i in range(len(daily_tasks)) if i not in user["completed_tasks"]]
    if not available:
        send_message(user_id, "🎉 Все задания выполнены!\n\nЗаходи завтра за новыми! 🖤", get_main_keyboard())
        return
    task_id = random.choice(available)
    task = daily_tasks[task_id]
    text = f"📋 Задание:\n\n{task['text']}\n\n📖 Инструкция:\n{task['instruction']}\n\n⚡ +{task['xp']} XP"
    send_message(user_id, text, get_task_keyboard())

def handle_progress(user_id):
    user = get_user_data(user_id)
    achievements_list = "\n".join([achievements[a] for a in user["achievements"]]) if user["achievements"] else "Пока нет"
    text = f"🏆 Твой прогресс:\n\n📊 Уровень: {user['level']}\n⚡ XP: {user['xp']} / {user['level'] * 100}\n🔥 Стрик: {user['streak']} дней\n✅ Заданий: {user['tasks_completed']}\n💕 Вакансий: {len(user['matched_vacancies'])}\n\n🏅 Достижения:\n{achievements_list}"
    send_message(user_id, text, get_progress_keyboard())

def handle_tests(user_id):
    user = get_user_data(user_id)
    if user.get("test_result"):
        result = career_test_results.get(user["test_result"], {})
        text = f"🎉 Твой результат: {result['title']}\n\n{result['desc']}\n\n🔍 Подходящие профессии:\n" + "\n".join([f"• {p}" for p in result.get('professions', [])])
        send_message(user_id, text, get_test_keyboard())
    else:
        send_message(user_id, "🧪 Тест профориентации\n\nОтветь на 3 вопроса и узнай, какая профессия тебе подходит!\n\n⏱️ Время: 2 минуты\n⚡ Награда: 100 XP\n\nНапиши 'начать тест'", get_test_keyboard())

def handle_skills(user_id):
    user = get_user_data(user_id)
    text = "🛠️ Твои навыки\n\n"
    if user["skills"]:
        for skill_name, level in user["skills"].items():
            level_name = skill_levels.get(level, "🌱 Новичок")
            text += f"{level_name} — {skill_name} (уровень {level}/5)\n"
    else:
        text += "Пока нет навыков.\n\nНапиши 'добавить навык [название]'\n\nПример: добавить навык коммуникация"
    text += f"\n\n⚡ +10 XP за новый навык"
    send_message(user_id, text, get_skills_keyboard())

def handle_resources(user_id, category=None):
    if category is None:
        text = "📚 Полезные ресурсы\n\nВыбери категорию:\n• 🎓 Курсы — обучение\n• 📖 Книги — для роста\n• 🛠️ Инструменты — для работы\n• 👥 Сообщества — поддержка\n\nНапиши название категории 👇"
        send_message(user_id, text, get_resources_keyboard())
    else:
        items = career_resources.get(category.lower(), [])
        if items:
            text = f"📚 {category.title()}:\n\n" + "\n".join(items)
            send_message(user_id, text)
        else:
            send_message(user_id, "⚠️ Категория не найдена. Попробуй: курсы, книги, инструменты, сообщества")

def handle_useful(user_id):
    tip = random.choice(weekly_tips)
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('📬 Ещё совет', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    send_message(user_id, tip, keyboard.get_keyboard())

def handle_feedback(user_id):
    user = get_user_data(user_id)
    send_message(user_id, "💬 Обратная связь\n\nЯ хочу сделать бота ещё лучше!\n\nНапиши:\n• Что тебе понравилось\n• Что можно улучшить\n• Какие функции добавить", get_feedback_keyboard())
    user["waiting_feedback"] = True

def handle_interview(user_id):
    user = get_user_data(user_id)
    text = f"🎤 Симулятор собеседования\n\nПройдено вопросов: {user.get('interview_completed', 0)}\n\nЯ задам вопрос, ты ответишь текстом.\nЯ проанализирую ответ и дам обратную связь!\n\n⚡ +20 XP за каждый вопрос"
    send_message(user_id, text, get_interview_keyboard())

def handle_resume(user_id):
    checklist_items = ["📸 Фотография добавлена", "📞 Контакты указаны", "💼 Опыт работы описан", "🎓 Образование указано", "🛠️ Навыки перечислены", "🏆 Достижения с цифрами", "📄 Формат PDF", "✅ Нет ошибок"]
    user = get_user_data(user_id)
    done = sum(1 for item in user.get("resume_checklist", [False]*8) if item)
    total = len(checklist_items)
    percent = int(done / total * 100)
    
    text = f"📄 Чек-лист резюме\n\n📊 Прогресс: {done}/{total} ({percent}%)\n\n"
    for i, item in enumerate(checklist_items):
        status = "✅" if user.get("resume_checklist", [False]*8)[i] else "⬜"
        text += f"{status} {item}\n"
    
    send_message(user_id, text, get_resume_keyboard())

# === ОСНОВНОЙ ЦИКЛ ===
def main():
    print("\n🖤 Ворон Кар (VK) запущен...")
    print(f"👥 Сообщество ID: {GROUP_ID}")
    print(f"👑 Админ ID: {ADMIN_VK_ID}")
    print("="*50)
    
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.obj.message
                user_id = message['from_id']
                text = message['text'].lower().strip()
                
                logging.info(f"Сообщение от {user_id}: {text}")
                user = get_user_data(user_id)
                
                # === КНОПКА "В МЕНЮ" ===
                if text == 'в меню' or text == '🔙':
                    user["interview_mode"] = False
                    user["test_answers"] = None
                    user["waiting_feedback"] = False
                    send_message(user_id, "🔙 Главное меню", get_main_keyboard())
                    continue
                
                # === СТОП → МЕНЮ ===
                if text == 'стоп' or text == '🛑':
                    user["interview_mode"] = False
                    user["test_answers"] = None
                    user["waiting_feedback"] = False
                    send_message(user_id, "🔙 Возврат в главное меню", get_main_keyboard())
                    continue
                
                # === ОБРАТНАЯ СВЯЗЬ ===
                if user.get("waiting_feedback", False):
                    feedback_text = f"💬 Новый отзыв!\n\n👤 От: {user_id}\n📝 Текст:\n{text}"
                    send_to_admin(feedback_text)
                    send_message(user_id, "Спасибо! Твой отзыв сохранён 🖤\n\n⚡ +20 XP", get_main_keyboard())
                    user["waiting_feedback"] = False
                    continue
                
                # === ОСНОВНЫЕ КОМАНДЫ ===
                if text in ['привет', '/start', 'старт', 'меню']:
                    handle_start(user_id)
                
                elif 'вакансии' in text or '💼' in text:
                    handle_vacancies(user_id)
                
                elif 'задание' in text or '📋' in text:
                    handle_tasks(user_id)
                
                elif 'прогресс' in text or '🏆' in text:
                    handle_progress(user_id)
                
                elif text == 'начать тест' or text == 'начатьтест':
                    user["test_answers"] = []
                    user["test_current"] = 0
                    user["interview_mode"] = False
                    question = career_test_questions[0]
                    keyboard = VkKeyboard(one_time=False)
                    for opt in question["options"]:
                        keyboard.add_button(opt["text"], color=VkKeyboardColor.PRIMARY)
                        keyboard.add_line()
                    keyboard.add_line()
                    keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
                    send_message(user_id, f"🧪 Вопрос 1/3\n\n{question['question']}", keyboard.get_keyboard())
                
                elif 'тест' in text or '🧪' in text:
                    handle_tests(user_id)
                
                elif 'навыки' in text or '🛠️' in text:
                    handle_skills(user_id)
                
                elif 'резюме' in text or '📄' in text:
                    handle_resume(user_id)
                
                elif 'ресурсы' in text or '📚' in text:
                    handle_resources(user_id)
                
                elif 'курсы' in text:
                    handle_resources(user_id, 'курсы')
                elif 'книги' in text:
                    handle_resources(user_id, 'книги')
                elif 'инструменты' in text:
                    handle_resources(user_id, 'инструменты')
                elif 'сообщества' in text:
                    handle_resources(user_id, 'сообщества')
                
                elif 'полезное' in text or '📬' in text:
                    handle_useful(user_id)
                
                elif 'обратная связь' in text or '💬' in text:
                    handle_feedback(user_id)
                
                elif 'собеседование' in text or '🎤' in text:
                    handle_interview(user_id)
                
                # === НАЧАТЬ ПРАКТИКУ ===
                elif 'начать практику' in text or 'начатьпрактику' in text:
                    user["interview_mode"] = True
                    user["interview_question_idx"] = 0
                    user["test_answers"] = None
                    q_data = interview_questions[0]
                    send_message(user_id, f"🎤 Вопрос 1/{len(interview_questions)}\n\n{q_data['question']}\n\n💡 Подсказка: {q_data['tips']}\n\nНапиши ответ 👇")
                
                # === ОБРАБОТКА СОБЕСЕДОВАНИЯ ===
                elif user.get("interview_mode", False):
                    q_idx = user.get("interview_question_idx", 0)
                    q_data = interview_questions[q_idx]
                    user_answer = text.lower()
                    
                    found_keywords = [kw for kw in q_data["keywords"] if kw in user_answer]
                    keyword_count = len(found_keywords)
                    
                    if keyword_count >= 2:
                        feedback = f"✅ Отличный ответ!\n\nТы упомянул: {', '.join(found_keywords)}\n\n💡 Пример:\n{q_data['example_answer']}"
                        xp_gain = 25
                    elif keyword_count == 1:
                        feedback = f"👍 Неплохо!\n\nТы упомянул: {found_keywords[0]}\n\n💡 Пример:\n{q_data['example_answer']}"
                        xp_gain = 15
                    else:
                        feedback = f"💡 Можно лучше!\n\nПопробуй: {q_data['tips']}\n\n💡 Пример:\n{q_data['example_answer']}"
                        xp_gain = 10
                    
                    user["interview_completed"] = user.get("interview_completed", 0) + 1
                    add_xp(user_id, xp_gain)
                    
                    if q_idx + 1 < len(interview_questions):
                        user["interview_question_idx"] += 1
                        next_q = interview_questions[q_idx + 1]
                        send_message(user_id, f"{feedback}\n\n⚡ +{xp_gain} XP\n\n🎤 Вопрос {q_idx + 2}/{len(interview_questions)}\n\n{next_q['question']}\n\n💡 Подсказка: {next_q['tips']}\n\nНапиши ответ 👇")
                    else:
                        user["interview_mode"] = False
                        send_message(user_id, f"{feedback}\n\n⚡ +{xp_gain} XP\n\n🎉 Собеседование завершено!\n\nВсего пройдено: {user['interview_completed']} вопросов", get_main_keyboard())
                    continue
                
                # === ОБРАБОТКА ТЕСТА ===
                elif user.get("test_answers") is not None and user.get("test_current", 0) < 3:
                    answer_type = None
                    for q in career_test_questions:
                        for opt in q["options"]:
                            if opt["text"].lower() in text:
                                answer_type = opt["type"]
                                break
                        if answer_type:
                            break
                    
                    if answer_type:
                        user["test_answers"].append(answer_type)
                        user["test_current"] += 1
                        
                        if user["test_current"] >= len(career_test_questions):
                            counts = {}
                            for ans in user["test_answers"]:
                                counts[ans] = counts.get(ans, 0) + 1
                            result_type = max(counts, key=counts.get)
                            user["test_result"] = result_type
                            add_xp(user_id, 100)
                            
                            result = career_test_results[result_type]
                            text = f"🎉 Тест завершён!\n\n{result['title']}\n{result['desc']}\n\n🔍 Подходящие профессии:\n" + "\n".join([f"• {p}" for p in result['professions']]) + f"\n\n⚡ +100 XP"
                            send_message(user_id, text, get_main_keyboard())
                            user["test_answers"] = None
                        else:
                            question = career_test_questions[user["test_current"]]
                            keyboard = VkKeyboard(one_time=False)
                            for opt in question["options"]:
                                keyboard.add_button(opt["text"], color=VkKeyboardColor.PRIMARY)
                                keyboard.add_line()
                            keyboard.add_line()
                            keyboard.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
                            send_message(user_id, f"🧪 Вопрос {user['test_current']+1}/3\n\n{question['question']}", keyboard.get_keyboard())
                    continue
                
                # === ДОБАВИТЬ НАВЫК ===
                elif 'добавить навык' in text:
                    parts = text.split('добавить навык')
                    if len(parts) > 1 and parts[1].strip():
                        skill_name = parts[1].strip()
                        if len(skill_name) >= 3 and skill_name not in user["skills"]:
                            user["skills"][skill_name] = 1
                            add_xp(user_id, 10)
                            send_message(user_id, f"✅ Навык добавлен!\n\n🛠️ {skill_name} — уровень 1/5\n\n⚡ +10 XP", get_main_keyboard())
                        else:
                            send_message(user_id, "⚠️ Введи название (мин. 3 символа) или навык уже добавлен!")
                    else:
                        send_message(user_id, "⚠️ Напиши: 'добавить навык [название]'\n\nПример: добавить навык коммуникация")
                
                # === ОБРАБОТКА КНОПОК ВАКАНСИЙ ===
                elif '✅' in text and 'подходит' in text:
                    vac_id = user["current_vacancy"]
                    if vac_id < len(vacancies):
                        if vac_id not in user["matched_vacancies"]:
                            user["matched_vacancies"].append(vac_id)
                        user["current_vacancy"] += 1
                        add_xp(user_id, 20)
                        send_message(user_id, f"✅ Отлично! Вакансия добавлена.\n\n⚡ +20 XP")
                        handle_vacancies(user_id)
                
                elif '❌' in text or 'не подходит' in text:
                    user["current_vacancy"] += 1
                    handle_vacancies(user_id)
                
                elif '⏭️' in text or 'далее' in text:
                    user["current_vacancy"] += 1
                    handle_vacancies(user_id)
                
                # === ВЫПОЛНИЛ ЗАДАНИЕ ===
                elif '✅' in text and 'выполнил' in text:
                    available = [i for i in range(len(daily_tasks)) if i not in user["completed_tasks"]]
                    if available:
                        task_id = random.choice(available)
                        user["completed_tasks"].append(task_id)
                        user["tasks_completed"] += 1
                        xp = daily_tasks[task_id]["xp"]
                        add_xp(user_id, xp)
                        send_message(user_id, f"✅ Выполнено!\n\n+{xp} XP", get_main_keyboard())
                
                elif '🔄' in text or 'другое' in text:
                    handle_tasks(user_id)
                
                # === ЕЩЁ СОВЕТ ===
                elif 'ещё совет' in text or 'ещёсовет' in text:
                    handle_useful(user_id)
                
                else:
                    send_message(user_id, "Используй кнопки внизу или напиши 'привет' для меню", get_main_keyboard())
        
        except Exception as e:
            logging.error(f"Ошибка обработки: {e}")
            continue

if __name__ == '__main__':
    main()
