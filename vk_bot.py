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
    return "🖤 Бот Ворон Кар работает!"

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
ADMIN_VK_ID = 355647886

vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

users_data = {}

# === ВАКАНСИИ С HH.RU ===
vacancies = [
    {"title": "SMM-менеджер", "company": "Digital Agency", "desc": "Ведение соцсетей, контент-план", "requirements": "• Опыт от 1 года\n• ВКонтакте, Telegram\n• Копирайтинг", "salary": "60-90 тыс. ₽", "link": "https://hh.ru/search/vacancy?text=SMM", "tips": "💡 Укажи примеры работ"},
    {"title": "Python-разработчик", "company": "TechStart", "desc": "Разработка ботов, API", "requirements": "• Python 3.x\n• aiogram/vk_api\n• Git, REST API", "salary": "80-120 тыс. ₽", "link": "https://hh.ru/search/vacancy?text=Python", "tips": "💡 Приложи GitHub"},
    {"title": "HR-ассистент", "company": "HR Pro", "desc": "Скрининг резюме, собеседования", "requirements": "• Коммуникабельность\n• Внимательность", "salary": "50-70 тыс. ₽", "link": "https://hh.ru/search/vacancy?text=HR", "tips": "💡 Подчеркни многозадачность"},
    {"title": "Контент-менеджер", "company": "Media House", "desc": "Наполнение сайта и соцсетей", "requirements": "• Грамотная речь\n• WordPress/Tilda", "salary": "45-65 тыс. ₽", "link": "https://hh.ru/search/vacancy?text=Контент-менеджер", "tips": "💡 Покажи примеры"},
    {"title": "Дизайнер", "company": "Creative Studio", "desc": "Дизайн для соцсетей", "requirements": "• Портфолио 5+ работ\n• Figma/Photoshop", "salary": "70-100 тыс. ₽", "link": "https://hh.ru/search/vacancy?text=Дизайнер", "tips": "💡 Приложи портфолио"},
]

# === ЗАДАНИЯ ===
daily_tasks = [
    {"text": "📝 Откликнись на 3 вакансии", "xp": 30, "instruction": "1. Открой «Вакансии»\n2. Выбери 3\n3. Нажми «✅ Подходит»"},
    {"text": "🎓 Изучи навык (30 мин)", "xp": 25, "instruction": "1. Открой «Ресурсы»\n2. Выбери курс\n3. Посмотри 30 мин"},
    {"text": "💼 Обнови резюме", "xp": 35, "instruction": "1. HH.ru\n2. Добавь достижения\n3. Проверь контакты"},
    {"text": "🤝 Напиши коллеге", "xp": 20, "instruction": "1. Вспомни 2-3 человека\n2. Напиши «Привет!»\n3. Предложи созвониться"},
    {"text": "📚 Прочитай статью", "xp": 15, "instruction": "1. Найди статью\n2. Прочитай\n3. Выдели 2-3 идеи"},
]

# === СОВЕТЫ ===
weekly_tips = [
    "💡 Откликайся до 10 утра!",
    "💡 Добавляй цифры в резюме!",
    "💡 Исследуй компанию!",
    "💡 Нетворкинг важнее резюме!",
    "💡 Делай паузы!",
]

# === ДОСТИЖЕНИЯ ===
achievements = {
    "first_start": "🐣 Первый шаг",
    "first_task": "✅ Дело сделано",
    "first_match": "🎯 Первый отклик",
    "interview_pass": "🎤 Собеседование пройдено",
}

# === ШАБЛОННЫЕ НАВЫКИ ===
available_skills = [
    "💬 Коммуникация", "🤝 Командная работа", "⏰ Тайм-менеджмент",
    "🐍 Python", "🇬🇧 Английский", "📊 Excel", "🎨 Дизайн",
    "📈 Аналитика", "🎯 Лидерство", "💡 Креативность",
    "📝 Копирайтинг", "🔍 Исследования", "💻 Программирование",
    "📱 SMM", "📊 Data Science",
]

skill_levels = {1: "🌱 Новичок", 2: "📚 Изучаю", 3: "💪 Практикую", 4: "🎯 Продвинутый", 5: "🏆 Эксперт"}

# === ТЕСТЫ ===
career_tests = {
    "prof_test": {
        "name": "🧪 Тест профориентации",
        "desc": "Узнай, какая профессия подходит!",
        "questions": [
            {"question": "Что нравится больше?", "options": [{"text": "Работать с людьми", "type": "social"}, {"text": "Работать с данными", "type": "analytical"}, {"text": "Создавать", "type": "creative"}, {"text": "Управлять", "type": "managerial"}]},
            {"question": "Как работаешь?", "options": [{"text": "В команде", "type": "social"}, {"text": "Сам", "type": "analytical"}, {"text": "Свободно", "type": "creative"}, {"text": "По плану", "type": "managerial"}]},
            {"question": "Что важнее?", "options": [{"text": "Помогать", "type": "social"}, {"text": "Анализ", "type": "analytical"}, {"text": "Творить", "type": "creative"}, {"text": "Достигать", "type": "managerial"}]},
        ],
        "results": {
            "social": {"title": "🤝 Социальный тип", "desc": "Тебе подходит работа с людьми!", "professions": ["HR", "Психолог", "Учитель", "Коуч"], "skills": ["💬 Коммуникация", "🎯 Эмпатия"], "resources": ["📖 «Как разговаривать с кем угодно»", "🎓 Курс «Коучинг»"]},
            "analytical": {"title": "📊 Аналитический тип", "desc": "Работа с данными!", "professions": ["Аналитик", "Программист", "Data Scientist"], "skills": ["🐍 Python", "📊 Визуализация"], "resources": ["📖 «Думай медленно»", "🎓 «Анализ данных»"]},
            "creative": {"title": "🎨 Креативный тип", "desc": "Творческая работа!", "professions": ["Дизайнер", "Копирайтер", "Маркетолог"], "skills": ["🎨 Figma", "✍️ Сторителлинг"], "resources": ["📖 «Кради как художник»", "🎓 «Основы дизайна»"]},
            "managerial": {"title": "🎯 Управленческий тип", "desc": "Руководящая работа!", "professions": ["Project Manager", "Team Lead", "Предприниматель"], "skills": ["📋 Agile", "🗣️ Коммуникация"], "resources": ["📖 «Цель» Голдратт", "🎓 «Управление проектами»"]},
        }
    },
    "stress_test": {
        "name": "😌 Тест на стресс",
        "desc": "Проверь стрессоустойчивость!",
        "questions": [
            {"question": "Реакция на дедлайны?", "options": [{"text": "Спокойно", "type": "high"}, {"text": "Нервничаю", "type": "medium"}, {"text": "Паникую", "type": "low"}]},
            {"question": "При конфликте?", "options": [{"text": "Ищу компромисс", "type": "high"}, {"text": "Избегаю", "type": "medium"}, {"text": "Конфликтую", "type": "low"}]},
        ],
        "results": {
            "high": {"title": "😌 Высокая устойчивость", "desc": "Отлично справляешься!", "recommendations": ["✅ Продолжай практиковать", "✅ Делись опытом"]},
            "medium": {"title": "😐 Средняя", "desc": "Есть куда расти", "recommendations": ["📚 Техники релаксации", "⏰ Планируй время"]},
            "low": {"title": "😰 Низкая", "desc": "Стоит поработать", "recommendations": ["🧘 Дыхательные практики", "📖 Книга «Антистресс»"]},
        }
    },
}

# === СОБЕСЕДОВАНИЕ ===
interview_questions = [
    {"question": "Расскажите о себе", "tips": "Образование → опыт → почему вакансия", "keywords": ["опыт", "образование", "работа", "интерес", "цель"], "red_flags": ["не знаю", "не уверен", "наверное"], "example": "Я окончил [вуз]. Работал в [сфера]. Заинтересовала вакансия, потому что [причина]."},
    {"question": "Почему хотите к нам?", "tips": "Покажи, что изучил компанию", "keywords": ["компания", "ценности", "продукт", "развитие"], "red_flags": ["не знаю", "просто хочу"], "example": "Мне нравится [факт]. Разделяю ценность [ценность]."},
    {"question": "Сильные стороны", "tips": "2-3 качества с примерами", "keywords": ["сильный", "навык", "опыт", "пример", "результат"], "red_flags": ["не знаю"], "example": "Организованный — вёл 3 проекта. Коммуникабельный — нахожу общий язык."},
    {"question": "Слабые стороны", "tips": "Слабость + как работаешь над ней", "keywords": ["работаю", "улучшаю", "учусь", "развиваюсь"], "red_flags": ["их нет", "перфекционизм"], "example": "Погружаюсь в детали. Научился ставить таймеры."},
    {"question": "Кем через 5 лет?", "tips": "Амбиции + реализм", "keywords": ["развитие", "рост", "цель", "карьера", "эксперт"], "red_flags": ["не знаю", "на вашем месте"], "example": "Вижу себя экспертом в [сфера], решающим сложные задачи."},
]

# === РЕСУРСЫ С ССЫЛКАМИ ===
career_resources = {
    "курсы": ["🎓 Яндекс.Практикум — https://practicum.yandex.ru/", "🎓 Stepik — https://stepik.org/", "🎓 Coursera — https://coursera.org/", "🎓 GeekBrains — https://geekbrains.ru/"],
    "книги": ["📖 «Дизайн карьеры» — как найти призвание", "📖 «Атомные привычки» — как меняться", "📖 «Гибкое сознание» — рост через ошибки"],
    "инструменты": ["🛠️ HH.ru — https://hh.ru/ (поиск вакансий)", "🛠️ Notion — https://notion.so/ (планирование)", "🛠️ Trello — https://trello.com/ (задачи)", "🛠️ Canva — https://canva.com/ (визуал)"],
    "сообщества": ["👥 «Карьера» ВКонтакте — советы и вакансии", "👥 «Профориентация» — тесты", "👥 «Молодые специалисты» — стажировки"],
}

# === РЕЗЮМЕ ЧЕК-ЛИСТ ===
resume_items = [
    {"id": "photo", "text": "📸 Фотография", "icon": "📸"},
    {"id": "contacts", "text": "📞 Контакты", "icon": "📞"},
    {"id": "experience", "text": "💼 Опыт работы", "icon": "💼"},
    {"id": "education", "text": "🎓 Образование", "icon": "🎓"},
    {"id": "skills", "text": "🛠️ Навыки", "icon": "🛠️"},
    {"id": "achievements", "text": "🏆 Достижения", "icon": "🏆"},
    {"id": "pdf", "text": "📄 Формат PDF", "icon": "📄"},
    {"id": "errors", "text": "✅ Нет ошибок", "icon": "✅"},
]

# === КЛАВИАТУРЫ ===
def get_main_keyboard():
    kb = VkKeyboard(one_time=False)
    kb.add_button('💼 Вакансии', color=VkKeyboardColor.PRIMARY)
    kb.add_button('📋 Задание дня', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('🧪 Тесты', color=VkKeyboardColor.PRIMARY)
    kb.add_button('🏆 Прогресс', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('📄 Резюме', color=VkKeyboardColor.PRIMARY)
    kb.add_button('🛠️ Навыки', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('🎤 Собеседование', color=VkKeyboardColor.PRIMARY)
    kb.add_button('✉️ Сопроводительное', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('📚 Ресурсы', color=VkKeyboardColor.POSITIVE)
    kb.add_button('📬 Полезное', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('💬 Обратная связь', color=VkKeyboardColor.NEGATIVE)
    return kb.get_keyboard()

def get_vacancy_kb():
    kb = VkKeyboard(one_time=False)
    kb.add_button('❌ Не подходит', color=VkKeyboardColor.NEGATIVE)
    kb.add_button('✅ Подходит', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('⏭️ Далее', color=VkKeyboardColor.PRIMARY)
    kb.add_button('🛑 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_task_kb():
    kb = VkKeyboard(one_time=False)
    kb.add_button('✅ Выполнил! (в меню)', color=VkKeyboardColor.POSITIVE)
    kb.add_button('🔄 Другое', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('🛑 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_tests_kb():
    kb = VkKeyboard(one_time=False)
    kb.add_button('🧪 Профориентация', color=VkKeyboardColor.PRIMARY)
    kb.add_button('😌 Тест на стресс', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_test_start_kb(name):
    kb = VkKeyboard(one_time=False)
    kb.add_button(f'▶️ {name}', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_test_options_kb(options):
    kb = VkKeyboard(one_time=False)
    for opt in options:
        kb.add_button(opt["text"], color=VkKeyboardColor.PRIMARY)
        kb.add_line()
    kb.add_line()
    kb.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_resume_kb():
    kb = VkKeyboard(one_time=False)
    for item in resume_items:
        kb.add_button(f"{item['icon']} {item['text']}", color=VkKeyboardColor.PRIMARY)
        kb.add_line()
    kb.add_line()
    kb.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_skills_kb():
    kb = VkKeyboard(one_time=False)
    kb.add_button('📊 Мои навыки', color=VkKeyboardColor.PRIMARY)
    kb.add_button('➕ Выбрать из списка', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_available_skills_kb():
    kb = VkKeyboard(one_time=False)
    for skill in available_skills[:10]:
        kb.add_button(skill, color=VkKeyboardColor.PRIMARY)
        kb.add_line()
    kb.add_line()
    kb.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_interview_kb():
    kb = VkKeyboard(one_time=False)
    kb.add_button('🎤 Начать практику', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

def get_resources_kb():
    kb = VkKeyboard(one_time=False)
    kb.add_button('🎓 Курсы', color=VkKeyboardColor.PRIMARY)
    kb.add_button('📖 Книги', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('🛠️ Инструменты', color=VkKeyboardColor.PRIMARY)
    kb.add_button('👥 Сообщества', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('🔙 В меню', color=VkKeyboardColor.SECONDARY)
    return kb.get_keyboard()

# === ФУНКЦИИ ===
def get_user(uid):
    if uid not in users_data:
        users_data[uid] = {
            "xp": 0, "level": 1, "tasks_done": 0,
            "achievements": [], "last_visit": None,
            "current_vacancy": 0, "matched": [],
            "completed_tasks": [], "waiting_feedback": False,
            "skills": {}, "interview_done": 0,
            "test_answers": None, "test_current": 0,
            "interview_mode": False, "interview_idx": 0,
            "resume_check": {}, "current_test": None,
            "cover_mode": False, "cover_data": {},
        }
    return users_data[uid]

def add_xp(uid, amount):
    u = get_user(uid)
    u["xp"] += amount
    lvl = (u["xp"] // 100) + 1
    if lvl > u["level"]:
        u["level"] = lvl
        return True
    return False

def send_msg(uid, text, kb=None):
    try:
        p = {'user_id': uid, 'message': text, 'random_id': random.randint(0, 2**31)}
        if kb: p['keyboard'] = kb
        vk.messages.send(**p)
        return True
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return False

def send_admin(text):
    try:
        vk.messages.send(user_id=ADMIN_VK_ID, message=text, random_id=random.randint(0, 2**31))
        return True
    except: return False

# === ОБРАБОТЧИКИ ===
def handle_start(uid):
    u = get_user(uid)
    if not u["last_visit"]:
        u["achievements"].append("first_start")
        add_xp(uid, 50)
        send_admin(f"🆕 Новый (ID: {uid})")
    u["last_visit"] = datetime.now()
    u["current_vacancy"] = 0
    u["interview_mode"] = False
    u["test_answers"] = None
    u["cover_mode"] = False
    u["current_test"] = None
    
    send_msg(uid, "🖤 Я Ворон Кар — карьерный наставник!")
    send_msg(uid, "Знаю, каково быть запутанным... Но я прошёл путь и теперь эксперт! 🎯")
    send_msg(uid, "В боте:\n\n💼 Вакансии с HH.RU\n📋 Задания с инструкциями\n🧪 Тесты профориентации\n🏆 Прогресс\n📄 Резюме чек-лист\n🛠️ Навыки\n🎤 Собеседование\n✉️ Сопроводительное\n📚 Ресурсы с ссылками\n📬 Советы", get_main_keyboard())

def handle_vacancies(uid):
    u = get_user(uid)
    if u["current_vacancy"] >= len(vacancies):
        send_msg(uid, "🎉 Все вакансии! Заходи позже! 🖤", get_main_keyboard())
        return
    v = vacancies[u["current_vacancy"]]
    txt = f"💼 {v['title']}\n🏢 {v['company']}\n💰 {v['salary']}\n\n📝 Задачи:\n{v['desc']}\n\n📋 Требования:\n{v['requirements']}\n\n🔗 Ссылка: {v['link']}\n\n{v['tips']}"
    send_msg(uid, txt, get_vacancy_kb())

def handle_tasks(uid):
    u = get_user(uid)
    avail = [i for i in range(len(daily_tasks)) if i not in u["completed_tasks"]]
    if not avail:
        send_msg(uid, "🎉 Все задания! Заходи завтра! 🖤", get_main_keyboard())
        return
    tid = random.choice(avail)
    t = daily_tasks[tid]
    txt = f"📋 Задание:\n\n{t['text']}\n\n📖 Инструкция:\n{t['instruction']}\n\n⚡ +{t['xp']} XP"
    send_msg(uid, txt, get_task_kb())

def handle_progress(uid):
    u = get_user(uid)
    ach = "\n".join([achievements[a] for a in u["achievements"]]) if u["achievements"] else "Пока нет"
    txt = f"🏆 Прогресс:\n\n📊 Уровень: {u['level']}\n⚡ XP: {u['xp']} / {u['level']*100}\n✅ Заданий: {u['tasks_done']}\n💕 Вакансий: {len(u['matched'])}\n\n🏅 Достижения:\n{ach}"
    send_msg(uid, txt)

def handle_tests(uid):
    send_msg(uid, "🧪 Выбери тест:\n\n1. Профориентация\nУзнай профессию!\n\n2. Тест на стресс\nПроверь устойчивость!", get_tests_kb())

def handle_skills(uid):
    u = get_user(uid)
    txt = "🛠️ Твои навыки\n\n"
    if u["skills"]:
        for name, lvl in u["skills"].items():
            txt += f"{skill_levels.get(lvl, '🌱')} — {name}\n"
    else:
        txt += "Пока нет.\n\nНажми «➕ Выбрать из списка»!"
    txt += f"\n\n⚡ +10 XP за навык"
    send_msg(uid, txt, get_skills_kb())

def handle_resources(uid, cat=None):
    if not cat:
        send_msg(uid, "📚 Ресурсы:\n\n🎓 Курсы — обучение\n📖 Книги — вдохновение\n🛠️ Инструменты — работа\n👥 Сообщества — поддержка", get_resources_kb())
    else:
        items = career_resources.get(cat, [])
        if items:
            send_msg(uid, f"📚 {cat.title()}:\n\n" + "\n\n".join(items))
        else:
            send_msg(uid, "⚠️ Не найдено.")

def handle_useful(uid):
    send_msg(uid, random.choice(weekly_tips))

def handle_feedback(uid):
    u = get_user(uid)
    send_msg(uid, "💬 Обратная связь\n\nНапиши:\n• Что понравилось\n• Что улучшить\n• Какие функции")
    u["waiting_feedback"] = True

def handle_interview(uid):
    u = get_user(uid)
    txt = f"🎤 Собеседование\n\nПройдено: {u.get('interview_done', 0)}\n\nЗадам 5 вопросов.\nПроанализирую:\n✅ Ключевые слова\n⚠️ Красные флаги\n💡 Пример ответа\n\n⚡ +20 XP за вопрос"
    send_msg(uid, txt, get_interview_kb())

def handle_resume(uid):
    u = get_user(uid)
    chk = u.get("resume_check", {})
    done = sum(1 for i in resume_items if chk.get(i["id"]))
    total = len(resume_items)
    pct = int(done/total*100)
    
    txt = f"📄 Чек-лист резюме\n\n📊 {done}/{total} ({pct}%)\n\nНажми на пункт:\n"
    for i in resume_items:
        st = "✅" if chk.get(i["id"]) else "⬜"
        txt += f"{st} {i['text']}\n"
    
    if pct == 100 and "resume_complete" not in u["achievements"]:
        u["achievements"].append("resume_complete")
        add_xp(uid, 200)
        txt += "\n🎉 Готово! +200 XP"
    
    send_msg(uid, txt, get_resume_kb())

# === ОСНОВНОЙ ЦИКЛ ===
def main():
    print("\n🖤 Ворон Кар запущен...")
    
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.obj.message
                uid = msg['from_id']
                txt = msg['text'].strip()
                txt_l = txt.lower()
                
                logging.info(f"📩 {uid}: {txt}")
                u = get_user(uid)
                
                # ПРИВЕТ
                if txt_l in ['привет', '/start', 'старт', 'меню']:
                    u["interview_mode"] = False
                    u["test_answers"] = None
                    u["waiting_feedback"] = False
                    u["cover_mode"] = False
                    u["current_test"] = None
                    handle_start(uid)
                    continue
                
                # В МЕНЮ / СТОП
                if txt_l == 'в меню' or '🔙' in txt or txt_l == 'стоп' or '🛑' in txt:
                    u["interview_mode"] = False
                    u["test_answers"] = None
                    u["waiting_feedback"] = False
                    u["cover_mode"] = False
                    u["current_test"] = None
                    send_msg(uid, "🔙 Меню", get_main_keyboard())
                    continue
                
                # ОБРАТНАЯ СВЯЗЬ
                if u.get("waiting_feedback"):
                    send_admin(f"💬 Отзыв от {uid}:\n{txt}")
                    send_msg(uid, "Спасибо! 🖤\n\n⚡ +20 XP", get_main_keyboard())
                    u["waiting_feedback"] = False
                    continue
                
                # КОМАНДЫ
                if 'вакансии' in txt_l or '💼' in txt:
                    handle_vacancies(uid)
                
                elif 'задание' in txt_l or '📋' in txt:
                    handle_tasks(uid)
                
                elif 'прогресс' in txt_l or '🏆' in txt:
                    handle_progress(uid)
                
                elif 'тесты' in txt_l or '🧪' in txt:
                    handle_tests(uid)
                
                elif 'навыки' in txt_l or '🛠️' in txt:
                    handle_skills(uid)
                
                elif 'резюме' in txt_l or '📄' in txt:
                    handle_resume(uid)
                
                elif 'ресурсы' in txt_l or '📚' in txt:
                    handle_resources(uid)
                
                elif 'курсы' in txt_l:
                    handle_resources(uid, 'курсы')
                elif 'книги' in txt_l:
                    handle_resources(uid, 'книги')
                elif 'инструменты' in txt_l:
                    handle_resources(uid, 'инструменты')
                elif 'сообщества' in txt_l:
                    handle_resources(uid, 'сообщества')
                
                elif 'полезное' in txt_l or '📬' in txt:
                    handle_useful(uid)
                
                elif 'обратная связь' in txt_l or '💬' in txt:
                    handle_feedback(uid)
                
                elif 'собеседование' in txt_l or '🎤' in txt:
                    handle_interview(uid)
                
                # СОПРОВОДИТЕЛЬНОЕ
                elif 'сопроводит' in txt_l or '✉️' in txt:
                    u["cover_mode"] = True
                    u["cover_data"] = {}
                    send_msg(uid, "✉️ Сопроводительное\n\nНапиши:\n1. Имя\n2. Позиция\n3. Компания\n4. Навыки (через /)\n5. Контакты\n6. Опыт (необяз.)\n\nПример:\nАнна, SMM, Digital, контент/аналитика, @anna, 2 года", get_main_keyboard())
                
                # ГЕНЕРАЦИЯ ПИСЬМА
                elif u.get("cover_mode"):
                    parts = [p.strip() for p in txt.split(',')]
                    if len(parts) >= 5:
                        name, pos, comp, skills_r, contact = parts[:5]
                        exp = parts[5] if len(parts) > 5 else ""
                        skills = [s.strip() for s in skills_r.split('/')]
                        
                        letter = f"Тема: {pos}\n\nУважаемая команда {comp}!\n\nМеня зовут {name}, хочу откликнуться на \"{pos}\".\n\n{exp if exp else 'Мои навыки соответствуют.'}\n\nНавыки:\n" + "\n".join([f"• {s}" for s in skills]) + f"\n\nПочему вы:\nМеня привлекает {comp}.\n\nЧто предложу:\n• Обучение\n• Ответственность\n• Команда\n• {skills[0] if skills else 'Профи'}\n\nКонтакты:\n{contact}\n\n{name}\n\n---\nВорон Кар 🖤"
                        
                        send_msg(uid, f"📬 Письмо:\n\n{letter}\n\n⚡ +30 XP", get_main_keyboard())
                        add_xp(uid, 30)
                        u["cover_mode"] = False
                    else:
                        send_msg(uid, "⚠️ 5+ пунктов через запятую!")
                    continue
                
                # ТЕСТЫ - ВЫБОР
                elif 'профориентация' in txt_l:
                    u["current_test"] = "prof_test"
                    t = career_tests["prof_test"]
                    send_msg(uid, f"{t['name']}\n\n{t['desc']}\n\n⏱️ 2 мин\n⚡ 100 XP", get_test_start_kb("Начать тест"))
                
                elif 'стресс' in txt_l:
                    u["current_test"] = "stress_test"
                    t = career_tests["stress_test"]
                    send_msg(uid, f"{t['name']}\n\n{t['desc']}\n\n⏱️ 1 мин\n⚡ 50 XP", get_test_start_kb("Начать тест"))
                
                # НАЧАТЬ ТЕСТ
                elif txt_l == 'начать тест' or '▶️' in txt:
                    if u.get("current_test"):
                        t = career_tests[u["current_test"]]
                        u["test_answers"] = []
                        u["test_current"] = 0
                        u["interview_mode"] = False
                        q = t["questions"][0]
                        send_msg(uid, f"🧪 Вопрос 1/{len(t['questions'])}\n\n{q['question']}", get_test_options_kb(q["options"]))
                    else:
                        send_msg(uid, "⚠️ Выбери тест из «🧪 Тесты»")
                
                # ОТВЕТЫ ТЕСТА
                elif u.get("test_answers") is not None and u.get("current_test"):
                    t = career_tests[u["current_test"]]
                    ans_type = None
                    
                    for opt in t["questions"][u["test_current"]]["options"]:
                        if opt["text"].lower() in txt_l:
                            ans_type = opt["type"]
                            break
                    
                    if ans_type:
                        u["test_answers"].append(ans_type)
                        u["test_current"] += 1
                        
                        if u["test_current"] >= len(t["questions"]):
                            counts = {}
                            for a in u["test_answers"]:
                                counts[a] = counts.get(a, 0) + 1
                            res_type = max(counts, key=counts.get)
                            res = t["results"][res_type]
                            
                            msg = f"🎉 Готово!\n\n{res['title']}\n\n{res['desc']}\n\n"
                            if 'professions' in res:
                                msg += f"🔍 Профессии:\n" + "\n".join([f"• {p}" for p in res['professions']]) + "\n\n"
                            if 'skills' in res:
                                msg += f"📈 Навыки:\n" + "\n".join([f"• {s}" for s in res['skills']]) + "\n\n"
                            if 'resources' in res:
                                msg += f"📚 Ресурсы:\n" + "\n".join([f"• {r}" for r in res['resources']]) + "\n\n"
                            if 'recommendations' in res:
                                msg += f"💡 Советы:\n" + "\n".join([f"• {r}" for r in res['recommendations']]) + "\n\n"
                            
                            xp = 100 if u["current_test"] == "prof_test" else 50
                            msg += f"\n⚡ +{xp} XP"
                            
                            add_xp(uid, xp)
                            send_msg(uid, msg, get_main_keyboard())
                            u["test_answers"] = None
                            u["current_test"] = None
                        else:
                            q = t["questions"][u["test_current"]]
                            send_msg(uid, f"🧪 Вопрос {u['test_current']+1}/{len(t['questions'])}\n\n{q['question']}", get_test_options_kb(q["options"]))
                    else:
                        send_msg(uid, "⚠️ Выбери вариант!")
                    continue
                
                # НАЧАТЬ ПРАКТИКУ
                elif 'начать практику' in txt_l or '▶️' in txt:
                    u["interview_mode"] = True
                    u["interview_idx"] = 0
                    u["test_answers"] = None
                    u["cover_mode"] = False
                    u["current_test"] = None
                    q = interview_questions[0]
                    send_msg(uid, f"🎤 Вопрос 1/{len(interview_questions)}\n\n{q['question']}\n\n💡 {q['tips']}\n\nНапиши ответ 👇")
                
                # СОБЕСЕДОВАНИЕ - ОТВЕТ
                elif u.get("interview_mode"):
                    idx = u.get("interview_idx", 0)
                    q = interview_questions[idx]
                    ans = txt_l
                    
                    # Красные флаги
                    reds = [f for f in q.get("red_flags", []) if f in ans]
                    # Ключевые слова
                    keys = [k for k in q["keywords"] if k in ans]
                    
                    fb = ""
                    if reds:
                        fb += f"⚠️ Не стоит:\n"
                        for r in reds: fb += f"❌ «{r}»\n"
                        fb += "\n"
                    
                    if len(keys) >= 2:
                        fb += f"✅ Отлично!\nУпомянул: {', '.join(keys)}"
                        xp = 25
                    elif len(keys) == 1:
                        fb += f"👍 Неплохо!\nУпомянул: {keys[0]}"
                        xp = 15
                    else:
                        fb += f"💡 Можно лучше!\n{q['tips']}"
                        xp = 10
                    
                    fb += f"\n\n💡 Пример:\n{q['example']}"
                    
                    u["interview_done"] = u.get("interview_done", 0) + 1
                    add_xp(uid, xp)
                    
                    if idx + 1 < len(interview_questions):
                        u["interview_idx"] += 1
                        nq = interview_questions[idx + 1]
                        send_msg(uid, f"{fb}\n\n⚡ +{xp} XP\n\n🎤 Вопрос {idx+2}/{len(interview_questions)}\n\n{nq['question']}\n\n💡 {nq['tips']}\n\nОтвет 👇")
                    else:
                        u["interview_mode"] = False
                        send_msg(uid, f"{fb}\n\n⚡ +{xp} XP\n\n🎉 Готово!\nВсего: {u['interview_done']}", get_main_keyboard())
                    continue
                
                # ВЫБОР НАВЫКА
                elif 'выбрать из списка' in txt_l or '➕' in txt:
                    send_msg(uid, "🛠️ Выбери:", get_available_skills_kb())
                
                elif any(s in txt for s in available_skills):
                    skill = txt.strip()
                    if skill in available_skills:
                        u = get_user(uid)
                        if skill not in u["skills"]:
                            u["skills"][skill] = 1
                            add_xp(uid, 10)
                            send_msg(uid, f"✅ Добавлен!\n\n🛠️ {skill} — 1/5\n\n⚡ +10 XP", get_main_keyboard())
                        else:
                            send_msg(uid, "⚠️ Уже есть!", get_main_keyboard())
                    else:
                        send_msg(uid, "Используй кнопки или 'привет'")
                
                # РЕЗЮМЕ - ЧЕК-ЛИСТ
                elif any(i['text'] in txt or i['icon'] in txt for i in resume_items):
                    u = get_user(uid)
                    chk = u.get("resume_check", {})
                    
                    for i in resume_items:
                        if i['text'] in txt or i['icon'] in txt:
                            chk[i["id"]] = not chk.get(i["id"], False)
                            st = "отмечен" if chk[i["id"]] else "снят"
                            send_msg(uid, f"✅ {i['text']} {st}!", get_resume_kb())
                            u["resume_check"] = chk
                            break
                    else:
                        handle_resume(uid)
                    continue
                
                # ВАКАНСИИ - КНОПКИ
                elif '✅' in txt and 'подходит' in txt_l:
                    vid = u["current_vacancy"]
                    if vid < len(vacancies):
                        if vid not in u["matched"]:
                            u["matched"].append(vid)
                        u["current_vacancy"] += 1
                        add_xp(uid, 20)
                        send_msg(uid, f"✅ Добавлена!\n\n🔗 {vacancies[vid]['link']}\n\n⚡ +20 XP")
                        handle_vacancies(uid)
                
                elif '❌' in txt or 'не подходит' in txt_l:
                    u["current_vacancy"] += 1
                    handle_vacancies(uid)
                
                elif '⏭️' in txt or 'далее' in txt_l:
                    u["current_vacancy"] += 1
                    handle_vacancies(uid)
                
                # ЗАДАНИЕ - ВЫПОЛНИЛ
                elif '✅' in txt and 'выполнил' in txt_l:
                    avail = [i for i in range(len(daily_tasks)) if i not in u["completed_tasks"]]
                    if avail:
                        tid = random.choice(avail)
                        u["completed_tasks"].append(tid)
                        u["tasks_done"] += 1
                        xp = daily_tasks[tid]["xp"]
                        add_xp(uid, xp)
                        send_msg(uid, f"✅ Готово!\n\n+{xp} XP", get_main_keyboard())
                
                elif '🔄' in txt or 'другое' in txt_l:
                    handle_tasks(uid)
                
                else:
                    send_msg(uid, "Используй кнопки или 'привет'", get_main_keyboard())
        
        except Exception as e:
            logging.error(f"❌ Ошибка: {e}")
            continue

if __name__ == '__main__':
    main()
