import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import logging
from datetime import datetime
from flask import Flask
import threading

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
VK_TOKEN = 'vk1.a.LKl0bvHMF1VamJQb-L8_k9HpPwRquBjAus3KxMxMH140LsAJJfYsS'  # ← Вставь свой токен
GROUP_ID = 236725121  # ← Вставь свой ID

# Инициализация
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

# === БАЗА ПОЛЬЗОВАТЕЛЕЙ ===
users_data = {}

# === ЗАДАНИЯ (20 штук) ===
daily_tasks = [
    {"text": "📝 Откликнись на 3 вакансии сегодня", "xp": 30},
    {"text": "🎓 Изучи новый навык (30 минут)", "xp": 25},
    {"text": "💼 Обнови своё резюме", "xp": 35},
    {"text": "🤝 Напиши бывшему коллеге", "xp": 20},
    {"text": "📚 Прочитай статью по профессии", "xp": 15},
    {"text": "🎯 Определи 3 карьерные цели", "xp": 25},
    {"text": "💡 Пройди профориентационный тест", "xp": 30},
    {"text": "📧 Напиши сопроводительное письмо", "xp": 40},
    {"text": "🔍 Изучи 5 компаний", "xp": 20},
    {"text": "🗣️ Потренируйся на собеседовании", "xp": 25},
    {"text": "✍️ Напиши пост о пути", "xp": 30},
    {"text": "🎬 Посмотри вебинар", "xp": 35},
    {"text": "📊 Проанализируй сильные стороны", "xp": 20},
    {"text": "🌐 Найди сообщества", "xp": 15},
    {"text": "📞 Позвони ментору", "xp": 25},
    {"text": "📋 Составь план развития", "xp": 40},
    {"text": "🎨 Обнови портфолио", "xp": 45},
    {"text": "💬 Напиши отзыв", "xp": 20},
    {"text": "🔗 Добавь контакты", "xp": 30},
    {"text": "🧘 Самопрезентация", "xp": 15},
]

# === ВАКАНСИИ ===
vacancies = [
    {"title": "SMM-менеджер", "company": "Digital Agency", "desc": "Ведение соцсетей", "link": "https://vk.com", "salary": "60-90 тыс. ₽"},
    {"title": "Python-разработчик", "company": "TechStart", "desc": "Разработка ботов", "link": "https://vk.com", "salary": "80-120 тыс. ₽"},
    {"title": "HR-ассистент", "company": "HR Pro", "desc": "Подбор персонала", "link": "https://vk.com", "salary": "50-70 тыс. ₽"},
    {"title": "Контент-менеджер", "company": "Media House", "desc": "Наполнение сайта", "link": "https://vk.com", "salary": "45-65 тыс. ₽"},
    {"title": "Дизайнер", "company": "Creative Studio", "desc": "Дизайн для соцсетей", "link": "https://vk.com", "salary": "70-100 тыс. ₽"},
]

# === ДОСТИЖЕНИЯ ===
achievements = {
    "first_start": "🐣 Первый шаг",
    "first_task": "✅ Дело сделано",
    "first_feedback": "💬 Голос услышан",
    "first_match": "🎯 Первый отклик",
}

# === НАВЫКИ ===
template_skills = ["💬 Коммуникация", "🤝 Командная работа", "⏰ Тайм-менеджмент", "🐍 Python", "🇬🇧 Английский"]
skill_levels = {1: "🌱 Новичок", 2: "📚 Изучаю", 3: "💪 Практикую", 4: "🎯 Продвинутый", 5: "🏆 Эксперт"}

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
            "completed_tasks": [], "waiting_feedback": False,
            "test_result": None, "resume_checklist": [False]*8,
            "skills": {}, "interview_completed": 0
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
        vk.messages.send(user_id=user_id, message=text, keyboard=keyboard, random_id=random.randint(0, 2**31))
        return True
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return False

# === ОБРАБОТЧИКИ ===
def handle_start(user_id, user_name):
    user = get_user_data(user_id)
    if user["last_visit"] is None:
        user["achievements"].append("first_start")
        add_xp(user_id, 50)
    user["last_visit"] = datetime.now()
    user["current_vacancy"] = 0
    
    send_message(user_id, f"Привет, {user_name}! 🖤\n\nЯ Ворон Кар — твой карьерный наставник!")
    send_message(user_id, "Я знаю, каково это: быть запутанным... Но я прошёл этот путь и теперь эксперт! 🎯")
    send_message(user_id, "В этом боте ты можешь:\n\n💼 Найти вакансии\n📋 Получать задания\n🧪 Пройти тесты\n🏆 Отслеживать прогресс\n📄 Создать резюме\n🛠️ Трекер навыков\n🎤 Собеседование\n✉️ Сопроводительное\n📬 Полезное\n💬 Обратная связь", get_main_keyboard())

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
        send_message(user_id, "🎉 Все задания выполнены!")
        return
    task_id = random.choice(available)
    task = daily_tasks[task_id]
    send_message(user_id, f"📋 Задание:\n\n{task['text']}\n\n⚡ +{task['xp']} XP", get_task_keyboard())

def handle_progress(user_id):
    user = get_user_data(user_id)
    text = f"🏆 Прогресс:\n\n📊 Уровень: {user['level']}\n⚡ XP: {user['xp']}\n🔥 Стрик: {user['streak']}\n✅ Заданий: {user['tasks_completed']}\n💕 Вакансий: {len(user['matched_vacancies'])}"
    send_message(user_id, text)

def handle_tests(user_id):
    user = get_user_data(user_id)
    if user.get("test_result"):
        send_message(user_id, f"🧪 Твой результат: {user['test_result']}\n\nНапиши 'тест' чтобы пройти заново")
    else:
        send_message(user_id, "🧪 Тест профориентации\n\nНапиши 'начать тест'")

def handle_skills(user_id):
    user = get_user_data(user_id)
    text = "🛠️ Навыки\n\n"
    if user["skills"]:
        for name, level in user["skills"].items():
            text += f"{skill_levels.get(level, '🌱')} — {name}\n"
    else:
        text += "Пока нет. Напиши 'добавить навык [название]'"
    send_message(user_id, text)

def handle_useful(user_id):
    tips = ["💡 Откликайся до 10 утра!", "💡 Добавляй цифры в резюме", "💡 Исследуй компанию перед собеседованием"]
    send_message(user_id, random.choice(tips))

# === ОСНОВНОЙ ЦИКЛ ===
def main():
    print("\n🖤 Ворон Кар (VK) запущен...")
    print(f"👥 Сообщество ID: {GROUP_ID}")
    print("="*50)
    
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.obj.message
                user_id = message['from_id']
                text = message['text'].lower().strip()
                
                logging.info(f"Сообщение от {user_id}: {text}")
                
                if text in ['привет', '/start', 'старт']:
                    handle_start(user_id, f"пользователь {user_id}")
                elif 'вакансии' in text:
                    handle_vacancies(user_id)
                elif 'задание' in text:
                    handle_tasks(user_id)
                elif 'прогресс' in text:
                    handle_progress(user_id)
                elif 'тест' in text:
                    handle_tests(user_id)
                elif 'навыки' in text:
                    handle_skills(user_id)
                elif 'полезное' in text:
                    handle_useful(user_id)
                elif 'обратная связь' in text:
                    send_message(user_id, "💬 Напиши отзыв!")
                    get_user_data(user_id)["waiting_feedback"] = True
                elif 'выполнил' in text:
                    user = get_user_data(user_id)
                    available = [i for i in range(len(daily_tasks)) if i not in user["completed_tasks"]]
                    if available:
                        task_id = random.choice(available)
                        user["completed_tasks"].append(task_id)
                        user["tasks_completed"] += 1
                        xp = daily_tasks[task_id]["xp"]
                        add_xp(user_id, xp)
                        send_message(user_id, f"✅ Выполнено!\n\n+{xp} XP")
                elif user.get("waiting_feedback", False):
                    send_message(user_id, "Спасибо! Отзыв сохранён 🖤\n\n⚡ +20 XP")
                    get_user_data(user_id)["waiting_feedback"] = False
                else:
                    send_message(user_id, "Используй кнопки или напиши 'привет'", get_main_keyboard())
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            continue

if __name__ == '__main__':
    main()
