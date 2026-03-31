import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload
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
upload = VkUpload(vk_session)

# === ССЫЛКИ НА ФОТО (замени на свои из альбома ВК!) ===
PHOTOS = {
    "start": "https://sun9-54.userapi.com/s/v1/ig2/cFf1OunCo8BMzn4-BfkBj0Q_M7xTGmGYm-jpKDISGHAKqSeRzy5vjqFtvn1vb6FrrfSyodyaQ5NMmR6XCunXA70v.jpg?quality=95&as=32x18,48x27,72x40,108x60,160x89,240x134,360x201,480x268,540x301,640x357,720x402,1080x602,1280x714,1377x768&from=bu&u=qywfPR3VR6x5oRU7rNurBhG4LRdACIgWGklJDCmncZY&cs=1377x0",
    "vacancy": "https://sun9-18.userapi.com/s/v1/ig2/T4KCgP4Uvcne5KB3-vGxUdk7FWR0U1_Jt0jhAuDwNY2KvSF8t5A30qjpp8FeiwvVE0k7J4ihFFvpCTZpYFNTZCYN.jpg?quality=95&as=32x18,48x27,72x40,108x60,160x89,240x134,360x201,480x268,540x301,640x357,720x402,1080x602,1280x714,1377x768&from=bu&cs=1377x0",
    "task": "https://sun9-10.userapi.com/s/v1/ig2/OkShBpprQtHk-d9XSPC3qAbW1nnVH-ELBcR7UkXRi-hKRDoqFWCdT1AULWkkslDwmoYp3i1AjhdVk83nOXVXmZNY.jpg?quality=95&as=32x18,48x27,72x40,108x60,160x89,240x134,360x201,480x268,540x301,640x357,720x402,1080x602,1280x714,1377x768&from=bu&cs=1377x0",
    "progress": "https://sun9-7.userapi.com/s/v1/ig2/5XYe4EZdiK7LPX4CEU0IvJm785k3k5L8quBWklixe4fEBsPzSle4eEIk1WxQB20RNBAxwd2ugVxehijBWND5kbNX.jpg?quality=95&as=32x18,48x27,72x40,108x60,160x89,240x134,360x201,480x268,540x301,640x357,720x402,1080x602,1280x714,1377x768&from=bu&cs=1377x0",
    "test": "https://sun9-81.userapi.com/s/v1/ig2/9FHJh7h_X2BGLeCWaUwSbNWKdLGrugdCH1QLY9j6qDVr1_I16SrD4n0gmjJtvYAlZ7ndswagEoEeSVRyGBnizGRk.jpg?quality=95&as=32x18,48x27,72x40,108x60,160x89,240x134,360x201,480x268,540x301,640x357,720x402,1080x602,1280x714,1377x768&from=bu&cs=1377x0",
    "useful": "https://sun9-6.userapi.com/s/v1/ig2/xOa4DDkWGI0W0m11dkBZXbusjbJH2173ROc2gSEhZ3HHpha6DyqJLF7oQIQLNEIMdFkwOi_1BlCmn1qRHCjXKvK-.jpg?quality=95&as=32x18,48x27,72x40,108x60,160x89,240x134,360x201,480x268,540x301,640x357,720x402,1080x602,1280x714,1377x768&from=bu&cs=1377x0",
    "feedback": "https://sun9-68.userapi.com/s/v1/ig2/NW2txpQdF5jmMfVum-a306OZG5qMzXq37JPyaKwg9j1hMp99sj-CfOw15uzWhc3mgk8_t-C_1KoppXdqYBfvqPul.jpg?quality=95&as=32x18,48x27,72x40,108x60,160x89,240x134,360x201,480x268,540x301,640x357,720x402,1080x602,1280x714,1377x768&from=bu&cs=1377x0",
}

# === БАЗА ПОЛЬЗОВАТЕЛЕЙ ===
users_data = {}

# === ЗАДАНИЯ (20 штук) ===
daily_tasks = [
    {"text": "📝 Откликнись на 3 вакансии сегодня", "xp": 30, "instruction": "1. Открой раздел «Вакансии»\n2. Выбери 3 подходящие\n3. Нажми «✅ Подходит»\n4. Перейди по ссылке и отправь резюме"},
    {"text": "🎓 Изучи новый навык (30 минут)", "xp": 25, "instruction": "1. Открой «📚 Ресурсы» → «Курсы»\n2. Выбери бесплатный урок\n3. Посмотри/прочитай 30 минут\n4. Запиши 3 главных вывода"},
    {"text": "💼 Обнови своё резюме", "xp": 35, "instruction": "1. Открой резюме на HH.ru\n2. Добавь последние достижения с цифрами\n3. Проверь контакты и фото\n4. Сохрани изменения"},
    {"text": "🤝 Напиши бывшему коллеге", "xp": 20, "instruction": "1. Вспомни 2-3 человека\n2. Напиши: «Привет! Как дела?»\n3. Предложи созвониться на 15 минут"},
    {"text": "📚 Прочитай статью по профессии", "xp": 15, "instruction": "1. Найди статью по специальности\n2. Прочитай внимательно\n3. Выдели 2-3 идеи для применения"},
    {"text": "🎯 Определи 3 карьерные цели", "xp": 25, "instruction": "1. Возьми листок\n2. Напиши: «Через месяц я хочу...»\n3. Сформулируй 3 конкретные цели\n4. Сохрани и проверяй прогресс"},
    {"text": "💡 Пройди профориентационный тест", "xp": 30, "instruction": "1. Напиши боту «тест»\n2. Ответь на 3 вопроса честно\n3. Изучи результат\n4. Сохрани подходящие профессии"},
    {"text": "📧 Напиши сопроводительное письмо", "xp": 40, "instruction": "1. Напиши боту «сопроводительное»\n2. Ответь на 6 вопросов\n3. Скопируй готовое письмо\n4. Отправь в компанию мечты"},
    {"text": "🔍 Изучи 5 компаний мечты", "xp": 20, "instruction": "1. Составь список из 5 компаний\n2. Для каждой найди: сайт, соцсети, вакансии\n3. Запиши, что нравится в каждой"},
    {"text": "🗣️ Потренируйся на собеседовании", "xp": 25, "instruction": "1. Напиши боту «собеседование»\n2. Нажми «🎤 Начать практику»\n3. Отвечай на вопросы\n4. Изучи обратную связь"},
    {"text": "✍️ Напиши пост о своём пути", "xp": 30, "instruction": "1. Вспомни ключевые точки\n2. Напиши пост для соцсетей\n3. Добавь, чему научился\n4. Опубликуй"},
    {"text": "🎬 Посмотри вебинар", "xp": 35, "instruction": "1. Открой «📚 Ресурсы»\n2. Найди бесплатный вебинар\n3. Посмотри с блокнотом\n4. Запиши 3 инсайта"},
    {"text": "📊 Проанализируй сильные стороны", "xp": 20, "instruction": "1. Раздели лист на 2 колонки\n2. Запиши 5 сильных сторон\n3. Запиши 5 зон роста\n4. Для каждой слабости — шаг по улучшению"},
    {"text": "🌐 Найди 3 профессиональных сообщества", "xp": 15, "instruction": "1. В поиске ВК введи профессию\n2. Найди 3 активных группы\n3. Подпишись\n4. Включи уведомления"},
    {"text": "📞 Позвони ментору", "xp": 25, "instruction": "1. Вспомни человека, чьим опытом восхищаешься\n2. Напиши: «Можно задать 2-3 вопроса?»\n3. Подготовь вопросы заранее"},
    {"text": "📋 Составь план развития на квартал", "xp": 40, "instruction": "1. Определи главную цель на 3 месяца\n2. Разбей на месячные шаги\n3. Добавь метрики успеха\n4. Проверяй прогресс каждую неделю"},
    {"text": "🎨 Создай или обнови портфолио", "xp": 45, "instruction": "1. Собери 3-5 лучших работ\n2. Опиши: задача → действие → результат\n3. Размести на Behance/GitHub/Notion"},
    {"text": "💬 Напиши отзыв о курсе/книге", "xp": 20, "instruction": "1. Вспомни последний курс/книгу\n2. Напиши: что понравилось, что применил\n3. Опубликуй в соцсетях"},
    {"text": "🔗 Добавь 5 новых контактов", "xp": 30, "instruction": "1. Открой ВК/LinkedIn\n2. Найди специалистов в твоей сфере\n3. Напиши персонализированное приглашение"},
    {"text": "🧘 Практикуй самопрезентацию", "xp": 15, "instruction": "1. Встань перед зеркалом\n2. Расскажи о себе за 2 минуты\n3. Запиши, что улучшить в подаче"},
]

# === ВАКАНСИИ (10 штук) ===
vacancies = [
    {"title": "SMM-менеджер", "company": "Digital Agency", "desc": "Ведение соцсетей, создание контент-плана, работа с блогерами, аналитика охватов", "requirements": "• Опыт от 1 года в SMM\n• Знание ВКонтакте, Telegram\n• Навыки копирайтинга\n• Умение работать с метриками", "salary": "60-90 тыс. ₽", "link": "https://vk.com", "tips": "💡 В отклике укажи примеры работ и метрики роста охватов"},
    {"title": "Python-разработчик", "company": "TechStart", "desc": "Разработка Telegram/VK ботов, парсеров, интеграция с API, поддержка кода", "requirements": "• Знание Python 3.x и ООП\n• Опыт с aiogram/vk_api\n• Git, REST API, SQL\n• Понимание асинхронности", "salary": "80-120 тыс. ₽", "link": "https://vk.com", "tips": "💡 Приложи ссылку на GitHub с примерами кода"},
    {"title": "HR-ассистент", "company": "HR Pro", "desc": "Первичный скрининг резюме, организация собеседований, ведение базы кандидатов", "requirements": "• Коммуникабельность и эмпатия\n• Внимательность к деталям\n• Опыт работы с людьми\n• Знание офисных программ", "salary": "50-70 тыс. ₽", "link": "https://vk.com", "tips": "💡 Подчеркни опыт работы с документами и многозадачность"},
    {"title": "Контент-менеджер", "company": "Media House", "desc": "Наполнение сайта и соцсетей, работа с CMS, координация с дизайнерами", "requirements": "• Грамотная письменная речь\n• Опыт работы с WordPress/Tilda\n• Базовые навыки визуала (Canva/Figma)\n• Умение работать в дедлайнах", "salary": "45-65 тыс. ₽", "link": "https://vk.com", "tips": "💡 Покажи примеры контента, который создавал"},
    {"title": "Графический дизайнер", "company": "Creative Studio", "desc": "Дизайн для соцсетей и веба, создание баннеров, иллюстраций", "requirements": "• Портфолио с 5+ работами\n• Уверенное владение Figma/Photoshop\n• Понимание композиции и типографики\n• Готовность к правкам", "salary": "70-100 тыс. ₽", "link": "https://vk.com", "tips": "💡 В отклике сразу приложи портфолио"},
    {"title": "Маркетолог-аналитик", "company": "Growth Lab", "desc": "Анализ рекламных кампаний, работа с метриками, подготовка отчётов", "requirements": "• Опыт с Яндекс.Метрикой, Google Analytics\n• Знание основ статистики\n• Умение работать с Excel/Google Sheets\n• Аналитический склад ума", "salary": "75-110 тыс. ₽", "link": "https://vk.com", "tips": "💡 Приведи пример, как твой анализ повлиял на результат"},
    {"title": "Технический писатель", "company": "DocuTech", "desc": "Написание документации, инструкций, гайдов для пользователей", "requirements": "• Отличная письменная речь\n• Понимание технических тем\n• Опыт работы с Markdown/Confluence\n• Внимательность к деталям", "salary": "55-80 тыс. ₽", "link": "https://vk.com", "tips": "💡 Приложи пример документации, которую писал"},
    {"title": "Project Manager", "company": "Agile Team", "desc": "Управление проектами, координация команды, планирование спринтов", "requirements": "• Опыт управления проектами от 1 года\n• Знание Agile/Scrum\n• Навыки коммуникации\n• Умение работать с Jira/Trello", "salary": "90-140 тыс. ₽", "link": "https://vk.com", "tips": "💡 Опиши проект, который вёл: команда, сроки, результат"},
    {"title": "UX/UI дизайнер", "company": "Design Hub", "desc": "Проектирование интерфейсов, пользовательские сценарии, прототипирование", "requirements": "• Портфолио с кейсами\n• Уверенное владение Figma\n• Понимание принципов юзабилити\n• Готовность к исследованиям", "salary": "85-130 тыс. ₽", "link": "https://vk.com", "tips": "💡 В кейсе покажи процесс: исследование → решение → результат"},
    {"title": "Data Analyst", "company": "DataFlow", "desc": "Анализ данных, визуализация, подготовка отчётов, поиск инсайтов", "requirements": "• Знание Python/R и SQL\n• Опыт с Pandas, NumPy, Matplotlib\n• Понимание статистики и A/B-тестов\n• Умение презентовать результаты", "salary": "95-150 тыс. ₽", "link": "https://vk.com", "tips": "💡 Приведи пример анализа, который привёл к бизнес-решению"},
]

# === ПОЛЕЗНЫЕ СОВЕТЫ ===
weekly_tips = [
    "💡 Откликайся на вакансии до 10 утра — рекрутеры чаще смотрят резюме в начале дня!",
    "💡 Добавляй цифры в резюме — «увеличил охват на 40%» работает лучше!",
    "💡 Исследуй компанию перед собеседованием — задавай умные вопросы!",
    "💡 Нетворкинг важнее резюме — 70% вакансий закрываются по рекомендациям!",
    "💡 Делай паузы в поиске работы — выгорание снижает качество откликов!",
    "💡 Сохраняй все отказы — анализируй, что можно улучшить!",
    "💡 Создай шаблон сопроводительного — адаптируй за 5 минут!",
    "💡 Обновляй резюме каждые 3 месяца — даже если не ищешь работу!",
]

# === ДОСТИЖЕНИЯ ===
achievements = {
    "first_start": "🐣 Первый шаг",
    "first_task": "✅ Дело сделано",
    "first_feedback": "💬 Голос услышан",
    "first_match": "🎯 Первый отклик",
    "week_streak": "🔥 Неделя в игре",
    "interview_pass": "🎤 Собеседование пройдено",
    "weekly_reader": "📚 Любитель советов",
    "portfolio_ready": "🎨 Портфолио готово",
}

# === НАВЫКИ ===
template_skills = ["💬 Коммуникация", "🤝 Работа в команде", "⏰ Тайм-менеджмент", "🐍 Python", "🇬🇧 Английский", "📊 Excel", "🎨 Дизайн", "📈 Аналитика", "🎯 Лидерство", "💡 Креативность"]
skill_levels = {1: "🌱 Новичок", 2: "📚 Изучаю", 3: "💪 Практикую", 4: "🎯 Продвинутый", 5: "🏆 Эксперт"}

# === ТЕСТ ПРОФОРИЕНТАЦИИ ===
career_test_questions = [
    {"question": "Что тебе нравится больше?", "options": [{"text": "Работать с людьми", "type": "social"}, {"text": "Работать с данными", "type": "analytical"}, {"text": "Создавать что-то новое", "type": "creative"}, {"text": "Управлять процессами", "type": "managerial"}]},
    {"question": "Как ты предпочитаешь работать?", "options": [{"text": "В команде", "type": "social"}, {"text": "Самостоятельно", "type": "analytical"}, {"text": "В свободном режиме", "type": "creative"}, {"text": "С чётким планом", "type": "managerial"}]},
    {"question": "Что для тебя важнее?", "options": [{"text": "Помогать другим", "type": "social"}, {"text": "Находить закономерности", "type": "analytical"}, {"text": "Выражать себя", "type": "creative"}, {"text": "Достигать целей", "type": "managerial"}]},
]

career_test_results = {
    "social": {"title": "🤝 Социальный тип", "desc": "Тебе подходит работа с людьми! Ты умеешь слушать, помогать и вдохновлять.", "professions": ["HR-менеджер", "Психолог", "Учитель", "Коуч", "Event-менеджер"], "skills_to_develop": ["💬 Активное слушание", "🎯 Эмоциональный интеллект", "📚 Методики обучения", "⏰ Тайм-менеджмент"], "resources": ["📖 Книга: «Как разговаривать с кем угодно» М. Роудз", "🎓 Курс: «Основы коучинга» на Stepik", "🌐 Сообщество: «Карьера» ВКонтакте"]},
    "analytical": {"title": "📊 Аналитический тип", "desc": "Тебе подходит работа с данными! Ты любишь находить закономерности.", "professions": ["Аналитик данных", "Программист", "Финансист", "Исследователь", "SEO-специалист"], "skills_to_develop": ["🐍 Python для анализа", "📊 Визуализация данных", "🔍 Критическое мышление", "📈 Статистика и A/B-тесты"], "resources": ["📖 Книга: «Думай медленно... решай быстро» Д. Канеман", "🎓 Курс: «Анализ данных на Python» на Stepik", "🌐 Сообщество: «Data Science» ВКонтакте"]},
    "creative": {"title": "🎨 Креативный тип", "desc": "Тебе подходит творческая работа! Ты умеешь генерировать идеи.", "professions": ["Дизайнер", "Копирайтер", "Маркетолог", "Режиссёр", "Иллюстратор"], "skills_to_develop": ["🎨 Figma/Photoshop", "✍️ Сторителлинг и копирайтинг", "💡 Методы генерации идей", "🎯 Понимание аудитории"], "resources": ["📖 Книга: «Кради как художник» О. Клеон", "🎓 Курс: «Основы дизайна» на Skillshare", "🌐 Сообщество: «Дизайнеры ВКонтакте»"]},
    "managerial": {"title": "🎯 Управленческий тип", "desc": "Тебе подходит руководящая работа! Ты умеешь ставить цели и вести команду.", "professions": ["Project Manager", "Team Lead", "Предприниматель", "COO", "Product Manager"], "skills_to_develop": ["📋 Agile/Scrum методологии", "🗣️ Эффективная коммуникация", "🎯 Постановка целей (OKR, SMART)", "💼 Финансовая грамотность"], "resources": ["📖 Книга: «Цель» Э. Голдратт", "🎓 Курс: «Управление проектами» на Coursera", "🌐 Сообщество: «Проджект-менеджеры» ВКонтакте"]},
}

# === ВОПРОСЫ ДЛЯ СОБЕСЕДОВАНИЯ ===
interview_questions = [
    {"question": "Расскажите немного о себе", "tips": "Говори 2-3 минуты. Структура: образование → опыт → почему эта вакансия.", "keywords": ["опыт", "образование", "работа", "интерес", "цель", "навык"], "example_answer": "Я окончил [вуз] по специальности [специальность]. Последние [число] лет работал в [сфера], где занимался [задачи]. Меня заинтересовала ваша вакансия, потому что [причина]. Я хочу развиваться в [направление] и верю, что мой опыт в [навык] будет полезен."},
    {"question": "Почему вы хотите работать именно у нас?", "tips": "Покажи, что изучил компанию: продукт, ценности, новости.", "keywords": ["компания", "ценности", "продукт", "культура", "развитие", "интерес"], "example_answer": "Мне нравится, что ваша компания [конкретный факт]. Я разделяю ценность [ценность] и хочу развиваться в направлении [направление]. Вижу, что мой опыт в [навык] может помочь в [задача компании]."},
    {"question": "Назовите ваши сильные стороны", "tips": "Выбери 2-3 качества, релевантные вакансии. Подкрепи примерами.", "keywords": ["сильный", "навык", "умение", "опыт", "пример", "результат"], "example_answer": "Я организованный — вёл 3 проекта одновременно и все дедлайны были соблюдены. Коммуникабельный — легко нахожу общий язык с командой. Быстро учусь — освоил [навык] за [срок] и применил в работе."},
    {"question": "Назовите ваши слабые стороны", "tips": "Назови реальную, но не критичную слабость + как работаешь над ней.", "keywords": ["работаю", "улучшаю", "учусь", "развиваюсь", "практика"], "example_answer": "Иногда слишком погружаюсь в детали. Но я научился ставить таймеры, проверять приоритеты и спрашивать обратную связь на ранних этапах, чтобы соблюдать дедлайны без потери качества."},
    {"question": "Кем вы видите себя через 5 лет?", "tips": "Покажи амбиции, но будь реалистом. Свяжи с развитием в компании.", "keywords": ["развитие", "рост", "цель", "карьера", "профессионал", "эксперт"], "example_answer": "Через 5 лет вижу себя экспертом в [сфера], который решает сложные задачи и помогает расти другим специалистам. Хочу развиваться в [направление] и приносить больше ценности компании."},
]

# === ⚠️ КРАСНЫЕ ФЛАГИ (слова, которые НЕЛЬЗЯ говорить на собеседовании) ===
interview_red_flags = {
    "не знаю": "⚠️ Лучше сказать: «Я ещё не сталкивался с этим, но готов быстро изучить»",
    "не уверен": "⚠️ Лучше сказать: «Я изучу этот вопрос и вернусь с ответом»",
    "наверное": "⚠️ Избегай неуверенности. Говори чётко и уверенно!",
    "может быть": "⚠️ Лучше сказать: «Я рассмотрю этот вариант»",
    "посмотрим": "⚠️ Лучше сказать: «Я изучу и предложу решение»",
    "как получится": "⚠️ Лучше сказать: «Я сделаю всё возможное для результата»",
    "не люблю": "⚠️ Не говори о нелюбви. Скажи: «Мне больше нравится...»",
    "ненавижу": "⚠️ ⛔ НИКОГДА не используй это слово на собеседовании!",
    "устал": "⚠️ Лучше сказать: «Я ищу новые вызовы для развития»",
    "выгорел": "⚠️ Лучше сказать: «Я ищу проект с новыми задачами»",
    "скучно": "⚠️ Лучше сказать: «Я ищу более интересные задачи»",
    "мало платили": "⚠️ Лучше сказать: «Я ищу рынокую зарплату за свой опыт»",
    "плохой начальник": "⚠️ ⛔ НИКОГДА не критикуй прошлых руководителей!",
    "плохая компания": "⚠️ ⛔ НИКОГДА не критикуй прошлых работодателей!",
    "ругались": "⚠️ Лучше сказать: «У нас были разные взгляды на процессы»",
    "конфликт": "⚠️ Лучше сказать: «Мы искали оптимальное решение»",
    "увольняли": "⚠️ Лучше сказать: «Мы расстались по соглашению сторон»",
    "выгнали": "⚠️ ⛔ НИКОГДА не используй это слово!",
    "не моё": "⚠️ Лучше сказать: «Я ищу направление, где смогу принести больше пользы»",
    "надоело": "⚠️ Лучше сказать: «Я ищу новые вызовы для профессионального роста»",
    "денег мало": "⚠️ Лучше сказать: «Я ищу справедливую оплату за свой вклад»",
    "переработки": "⚠️ Лучше сказать: «Я ценю баланс работы и жизни»",
    "не ценили": "⚠️ Лучше сказать: «Я ищу компанию, где вклад каждого важен»",
    "бесило": "⚠️ ⛔ НИКОГДА не используй эмоциональные негативные слова!",
    "злость": "⚠️ ⛔ Сохраняй профессиональный тон!",
    "обида": "⚠️ ⛔ Не говори о личных эмоциях!",
}

# === КАТАЛОГ РЕСУРСОВ ===
career_resources = {
    "курсы": ["🎓 Яндекс.Практикум — профессии IT и маркетинга (есть рассрочка)", "🎓 Skillbox — практические курсы с дипломом", "🎓 Stepik — бесплатные курсы по программированию", "🎓 Открытое образование — курсы от ведущих вузов РФ", "🎓 Coursera — международные курсы (есть финансовая помощь)", "🎓 GeekBrains — IT-профессии с гарантией трудоустройства"],
    "книги": ["📖 «Дизайн карьеры» Б. Бернетт — как найти своё призвание", "📖 «Атомные привычки» Дж. Клир — как меняться постепенно", "📖 «Гибкое сознание» К. Дуэк — как расти через ошибки", "📖 «Работа мечты» М. Олпорт — как найти дело по душе", "📖 «Не работайте с идиотами» М. Гоулд — здоровые отношения на работе", "📖 «Спроси маму» Р. Фицпатрик — как тестировать идеи"],
    "инструменты": ["🛠️ HH.ru — поиск вакансий, резюме, статистика", "🛠️ LinkedIn — профессиональная сеть для нетворкинга", "🛠️ Notion — планирование, заметки, портфолио", "🛠️ Trello/Asana — управление задачами и проектами", "🛠️ Canva/Figma — создание визуалов для портфолио", "🛠️ Google Forms — сбор обратной связи и опросы"],
    "сообщества": ["👥 «Карьера» ВКонтакте — советы, вакансии, истории успеха", "👥 «Профориентация» — тесты, консультации, вебинары", "👥 «Молодые специалисты» — поддержка старта, стажировки", "👥 «Карьерный рост» — интервью с экспертами, разбор кейсов", "👥 «Удалёнка» — вакансии и советы для работы из дома", "👥 «Фриланс» — поиск заказов, юридические вопросы, налоги"],
}

# === СТАТИСТИКА ПО ПРОФЕССИЯМ ===
profession_stats = {
    "smm": {"name": "SMM-менеджер", "avg_salary": "50-90 тыс. ₽", "growth": "+15% в год", "skills": ["Контент", "Аналитика", "Таргет", "Копирайтинг", "Визуал"], "pros": ["Творчество", "Гибкий график", "Удалёнка", "Быстрый вход"], "cons": ["Ненормированный день", "Высокая конкуренция", "Нужно быть на связи"], "first_steps": "1. Освой базовый копирайтинг и визуал (Canva)\n2. Создай портфолио на 3-5 кейсах\n3. Начни с фриланса или стажировки"},
    "python": {"name": "Python-разработчик", "avg_salary": "80-150 тыс. ₽", "growth": "+25% в год", "skills": ["Python", "SQL", "Git", "API", "Асинхронность"], "pros": ["Высокая зарплата", "Спрос на рынке", "Удалёнка", "Логика и структура"], "cons": ["Нужно постоянно учиться", "Сидячая работа", "Высокий порог входа"], "first_steps": "1. Пройди бесплатный курс на Stepik\n2. Реши 50+ задач на LeetCode/HackerRank\n3. Создай 2-3 проекта для портфолио на GitHub"},
    "hr": {"name": "HR-специалист", "avg_salary": "45-80 тыс. ₽", "growth": "+10% в год", "skills": ["Коммуникация", "Эмпатия", "Документооборот", "Ассессмент"], "pros": ["Работа с людьми", "Разнообразие задач", "Развитие софт-скиллов"], "cons": ["Эмоциональное выгорание", "Много рутины", "Ответственность за людей"], "first_steps": "1. Изучи основы трудового права и рекрутинга\n2. Пройди стажировку в HR-отделе\n3. Развивай навыки интервью и обратной связи"},
    "designer": {"name": "Графический/UX-дизайнер", "avg_salary": "60-120 тыс. ₽", "growth": "+20% в год", "skills": ["Figma", "Композиция", "Типографика", "Исследования", "Прототипирование"], "pros": ["Творчество", "Визуальный результат", "Удалёнка", "Междисциплинарность"], "cons": ["Субъективная оценка", "Много правок", "Нужно прокачивать насмотренность"], "first_steps": "1. Освой Figma на бесплатных туториалах\n2. Перерисуй 10+ интерфейсов для тренировки\n3. Создай кейс с процессом: задача → исследование → решение"},
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
    return keyboard.get_keyboard()

def get_task_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('✅ Выполнил!', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('🔄 Другое', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()

def get_resources_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🎓 Курсы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Книги', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🛠️ Инструменты', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('👥 Сообщества', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_profession_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('SMM', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Python', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('HR', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Дизайнер', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_resume_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('📋 Чек-лист', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('✅ Отметить пункт', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_skills_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('📊 Мои навыки', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('➕ Добавить', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('⬆️ Прокачать', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_interview_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🎤 Начать практику', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('💡 Советы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
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
            "skills": {}, "interview_completed": 0,
            "cover_letter_data": {}, "last_weekly_tip": None,
            "first_message_time": datetime.now(),
            "test_answers": None, "test_current": 0,
            "interview_mode": False, "interview_question_idx": 0,
            "waiting_custom_skill": False
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

def send_message(user_id, text, keyboard=None, attachment=None):
    try:
        params = {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 2**31)}
        if keyboard:
            params['keyboard'] = keyboard
        if attachment:
            params['attachment'] = attachment
        vk.messages.send(**params)
        return True
    except Exception as e:
        logging.error(f"Ошибка отправки: {e}")
        return False

def send_photo(user_id, photo_url, caption, keyboard=None):
    try:
        photo = upload.photo_messages(photos=photo_url)[0]
        attachment = f"photo{photo['owner_id']}_{photo['id']}"
        return send_message(user_id, caption, keyboard, attachment)
    except Exception as e:
        logging.warning(f"⚠️ Фото не отправлено: {e}")
        return send_message(user_id, caption, keyboard)

def send_to_admin(text):
    try:
        vk.messages.send(user_id=ADMIN_VK_ID, message=text, random_id=random.randint(0, 2**31))
        logging.info("✅ Сообщение админу отправлено")
        return True
    except Exception as e:
        logging.error(f"❌ Ошибка отправки админу: {e}")
        return False

def check_interview_red_flags(user_answer):
    """Проверяет ответ на красные флаги"""
    found_flags = []
    user_answer_lower = user_answer.lower()
    
    for flag, advice in interview_red_flags.items():
        if flag in user_answer_lower:
            found_flags.append((flag, advice))
    
    return found_flags

# === ОБРАБОТЧИКИ ===
def handle_start(user_id, user_name):
    user = get_user_data(user_id)
    if user["last_visit"] is None:
        user["achievements"].append("first_start")
        add_xp(user_id, 50)
        send_to_admin(f"🆕 Новый пользователь: {user_name} (ID: {user_id})")
    user["last_visit"] = datetime.now()
    user["current_vacancy"] = 0
    
    photo_url = PHOTOS.get("start", "")
    caption = f"Привет, {user_name}! 🖤\n\nЯ Ворон Кар — твой карьерный наставник!"
    send_photo(user_id, photo_url, caption)
    
    send_message(user_id, "Я знаю, каково это: быть запутанным... Но я прошёл этот путь и теперь эксперт! 🎯")
    send_message(user_id, "В этом боте ты можешь:\n\n💼 Найти вакансии с требованиями и советами\n📋 Получать задания с инструкциями\n🧪 Пройти тест профориентации с рекомендациями\n🏆 Отслеживать прогресс и достижения\n📄 Создать резюме по чек-листу\n🛠️ Трекер навыков с уровнями прокачки\n🎤 Симулятор собеседования с примерами ответов\n✉️ Генератор сопроводительных писем\n📚 Каталог ресурсов (курсы, книги, инструменты)\n📬 Еженедельные карьерные лайфхаки", get_main_keyboard())

def handle_vacancies(user_id):
    user = get_user_data(user_id)
    if user["current_vacancy"] >= len(vacancies):
        send_message(user_id, "🎉 Все вакансии просмотрены!\n\nЗаходи позже — будут новые! 🖤")
        return
    vac = vacancies[user["current_vacancy"]]
    text = f"💼 <b>{vac['title']}</b>\n🏢 {vac['company']}\n💰 {vac['salary']}\n\n📝 <b>Задачи:</b>\n{vac['desc']}\n\n📋 <b>Требования:</b>\n{vac['requirements']}\n\n{vac['tips']}"
    photo_url = PHOTOS.get("vacancy", "")
    send_photo(user_id, photo_url, text, get_vacancy_keyboard())

def handle_tasks(user_id):
    user = get_user_data(user_id)
    available = [i for i in range(len(daily_tasks)) if i not in user["completed_tasks"]]
    if not available:
        send_message(user_id, "🎉 Все задания выполнены!\n\nЗаходи завтра за новыми! 🖤")
        return
    task_id = random.choice(available)
    task = daily_tasks[task_id]
    text = f"📋 <b>Задание:</b>\n\n{task['text']}\n\n📖 <b>Инструкция:</b>\n{task['instruction']}\n\n⚡ +{task['xp']} XP"
    photo_url = PHOTOS.get("task", "")
    send_photo(user_id, photo_url, text, get_task_keyboard())

def handle_progress(user_id):
    user = get_user_data(user_id)
    achievements_list = "\n".join([achievements[a] for a in user["achievements"]]) if user["achievements"] else "Пока нет"
    text = f"🏆 <b>Твой прогресс:</b>\n\n📊 Уровень: {user['level']}\n⚡ XP: {user['xp']} / {user['level'] * 100}\n🔥 Стрик: {user['streak']} дней подряд\n✅ Заданий выполнено: {user['tasks_completed']}\n💕 Вакансий в избранном: {len(user['matched_vacancies'])}\n\n🏅 <b>Достижения:</b>\n{achievements_list}"
    photo_url = PHOTOS.get("progress", "")
    send_photo(user_id, photo_url, text)

def handle_tests(user_id):
    user = get_user_data(user_id)
    if user.get("test_result"):
        result = career_test_results.get(user["test_result"], {})
        text = f"🎉 <b>Твой результат: {result['title']}</b>\n\n{result['desc']}\n\n🔍 <b>Подходящие профессии:</b>\n" + "\n".join([f"• {p}" for p in result.get('professions', [])]) + f"\n\n📈 <b>Навыки для развития:</b>\n" + "\n".join([f"• {s}" for s in result.get('skills_to_develop', [])]) + f"\n\n📚 <b>Полезные ресурсы:</b>\n" + "\n".join([f"• {r}" for r in result.get('resources', [])])
        send_message(user_id, text)
    else:
        photo_url = PHOTOS.get("test", "")
        send_photo(user_id, photo_url, "🧪 <b>Тест профориентации</b>\n\nОтветь на 3 вопроса и узнай, какая профессия тебе подходит!\n\n⏱️ Время: 2 минуты\n⚡ Награда: 100 XP\n\nНапиши 'начать тест'")

def handle_skills(user_id):
    user = get_user_data(user_id)
    text = "🛠️ <b>Твои навыки</b>\n\n"
    if user["skills"]:
        for skill_name, level in user["skills"].items():
            level_name = skill_levels.get(level, "🌱 Новичок")
            text += f"{level_name} — {skill_name} (уровень {level}/5)\n"
    else:
        text += "Пока нет навыков. Добавь первый!\n\nНапиши 'добавить навык [название]'\n\nПримеры: 'добавить навык коммуникация', 'добавить навык Figma'"
    text += f"\n\n⚡ +10 XP за новый навык, +15 XP за прокачку"
    photo_url = PHOTOS.get("skills", "")
    send_photo(user_id, photo_url, text, get_skills_keyboard())

def handle_resume(user_id):
    user = get_user_data(user_id)
    checklist_items = ["📸 Фотография добавлена", "📞 Контакты указаны", "💼 Опыт работы описан", "🎓 Образование указано", "🛠️ Навыки перечислены", "🏆 Достижения с цифрами", "📄 Формат PDF", "✅ Нет ошибок"]
    done = sum(1 for item in user["resume_checklist"] if item)
    total = len(checklist_items)
    percent = int(done / total * 100)
    
    text = f"📄 <b>Чек-лист резюме</b>\n\n📊 <b>Прогресс:</b> {done}/{total} ({percent}%)\n\n"
    for i, item in enumerate(checklist_items):
        status = "✅" if user["resume_checklist"][i] else "⬜"
        text += f"{status} {item}\n"
    
    if percent == 100 and "resume_complete" not in user["achievements"]:
        user["achievements"].append("resume_complete")
        add_xp(user_id, 200)
        text += "\n\n🎉 <b>Поздравляю! Резюме готово! +200 XP</b>"
    
    photo_url = PHOTOS.get("resume", "")
    send_photo(user_id, photo_url, text, get_resume_keyboard())

def handle_interview(user_id):
    user = get_user_data(user_id)
    text = f"🎤 <b>Симулятор собеседования</b>\n\nПройдено вопросов: {user.get('interview_completed', 0)}\n\nЯ задам вопрос, ты ответишь текстом.\nЯ проанализирую ответ и дам обратную связь + пример идеального ответа!\n\n⚠️ <b>Внимание:</b> Я также проверяю ответы на «красные флаги» — слова, которые лучше не говорить на собеседовании!\n\n⚡ +20 XP за каждый вопрос, +50 XP за прохождение всех"
    photo_url = PHOTOS.get("interview", "")
    send_photo(user_id, photo_url, text, get_interview_keyboard())

def handle_resources(user_id, category=None):
    if category is None:
        text = "📚 <b>Полезные ресурсы</b>\n\nВыбери категорию:\n• 🎓 Курсы — обучение новым навыкам\n• 📖 Книги — для вдохновения и роста\n• 🛠️ Инструменты — для работы и организации\n• 👥 Сообщества — поддержка и нетворкинг\n\nНапиши название категории 👇"
        send_message(user_id, text, get_resources_keyboard())
    else:
        items = career_resources.get(category.lower(), [])
        if items:
            text = f"📚 <b>{category.title()}:</b>\n\n" + "\n".join(items)
            send_message(user_id, text)
        else:
            send_message(user_id, "⚠️ Категория не найдена. Попробуй: курсы, книги, инструменты, сообщества")

def handle_profession_info(user_id, profession):
    stat = profession_stats.get(profession.lower())
    if stat:
        text = f"🔍 <b>{stat['name']}</b>\n\n💰 <b>Средняя зарплата:</b> {stat['avg_salary']}\n📈 <b>Рост спроса:</b> {stat['growth']}\n\n🛠️ <b>Ключевые навыки:</b>\n" + "\n".join([f"• {s}" for s in stat['skills']]) + f"\n\n✅ <b>Плюсы:</b> {', '.join(stat['pros'])}\n❌ <b>Минусы:</b> {', '.join(stat['cons'])}\n\n🚀 <b>Первые шаги:</b>\n{stat['first_steps']}"
        send_message(user_id, text)
    else:
        send_message(user_id, "⚠️ Профессия не найдена. Попробуй: smm, python, hr, дизайнер", get_profession_keyboard())

def handle_useful(user_id):
    tip = random.choice(weekly_tips)
    photo_url = PHOTOS.get("useful", "")
    send_photo(user_id, photo_url, tip)

def handle_feedback(user_id):
    user = get_user_data(user_id)
    photo_url = PHOTOS.get("feedback", "")
    send_photo(user_id, photo_url, "💬 <b>Обратная связь</b>\n\nЯ хочу сделать бота ещё лучше!\n\nНапиши:\n• Что тебе понравилось\n• Что можно улучшить\n• Какие функции добавить")
    user["waiting_feedback"] = True

# === АДМИН-ПАНЕЛЬ ===
def handle_admin(user_id):
    if user_id != ADMIN_VK_ID:
        send_message(user_id, "⚠️ Доступ только для администратора!")
        return
    
    total_users = len(users_data)
    active_users = sum(1 for u in users_data.values() if u["last_visit"])
    total_xp = sum(u["xp"] for u in users_data.values())
    
    top_users = sorted(users_data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:5]
    top_text = "\n".join([f"{i+1}. ID {uid} — {u['xp']} XP" for i, (uid, u) in enumerate(top_users)])
    
    text = f"👑 <b>Админ-панель Ворон Кар</b>\n\n📊 <b>Статистика:</b>\n👥 Всего пользователей: {total_users}\n🔥 Активных: {active_users}\n⚡ XP выдано: {total_xp}\n\n🏆 <b>Топ-5 по активности:</b>\n{top_text}\n\n<i>Для детальной статистики напиши 'статистика'</i>"
    send_message(user_id, text)

def handle_stats(user_id):
    if user_id != ADMIN_VK_ID:
        return
    
    text = "📊 <b>Детальная статистика пользователей:</b>\n\n"
    for uid, data in users_data.items():
        text += f"👤 ID: {uid}\n   • XP: {data['xp']}, Уровень: {data['level']}\n   • Заданий: {data['tasks_completed']}, Стрик: {data['streak']}\n   • Последнее посещение: {data['last_visit']}\n\n"
    send_message(user_id, text)

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
                
                # === АДМИН-КОМАНДЫ ===
                if text in ['/admin', 'админ', 'панель']:
                    handle_admin(user_id)
                    continue
                elif text in ['/stats', 'статистика']:
                    handle_stats(user_id)
                    continue
                
                # === ОБРАТНАЯ СВЯЗЬ → АДМИНУ В ЛС ===
                if user.get("waiting_feedback", False):
                    feedback_text = f"💬 <b>Новый отзыв!</b>\n\n👤 От: {user_id}\n📝 Текст:\n{text}\n\n📊 Статистика:\n   • XP: {user['xp']}, Уровень: {user['level']}\n   • Заданий: {user['tasks_completed']}"
                    send_to_admin(feedback_text)
                    send_message(user_id, "Спасибо! Твой отзыв сохранён 🖤\n\n⚡ +20 XP")
                    user["waiting_feedback"] = False
                    continue
                
                # === ОСНОВНЫЕ КОМАНДЫ ===
                if text in ['привет', '/start', 'старт']:
                    handle_start(user_id, f"пользователь {user_id}")
                elif any(word in text for word in ['вакансии', '💼']):
                    handle_vacancies(user_id)
                elif any(word in text for word in ['задание', '📋', 'день']):
                    handle_tasks(user_id)
                elif any(word in text for word in ['прогресс', '🏆', 'уровень']):
                    handle_progress(user_id)
                elif any(word in text for word in ['тест', '🧪', 'профориентация']):
                    if 'начать' in text:
                        user["test_answers"] = []
                        user["test_current"] = 0
                        question = career_test_questions[0]
                        keyboard = VkKeyboard(one_time=False)
                        for opt in question["options"]:
                            keyboard.add_button(opt["text"], color=VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                        send_message(user_id, f"🧪 <b>Вопрос 1/3</b>\n\n{question['question']}", keyboard.get_keyboard())
                    else:
                        handle_tests(user_id)
                elif any(word in text for word in ['навыки', '🛠️']):
                    handle_skills(user_id)
                elif any(word in text for word in ['резюме', '📄']):
                    handle_resume(user_id)
                elif any(word in text for word in ['собеседование', '🎤', 'интервью']):
                    handle_interview(user_id)
                elif any(word in text for word in ['сопроводительное', '✉️', 'письмо']):
                    send_message(user_id, "✉️ <b>Генератор сопроводительного письма</b>\n\nНапиши 'создать письмо' чтобы начать мастер создания")
                elif any(word in text for word in ['полезное', '📬', 'совет']):
                    handle_useful(user_id)
                elif any(word in text for word in ['обратная связь', '💬', 'отзыв']):
                    handle_feedback(user_id)
                elif any(word in text for word in ['ресурсы', '📚', 'каталог']):
                    handle_resources(user_id)
                elif any(cat in text for cat in ['курсы', 'книги', 'инструменты', 'сообщества']):
                    handle_resources(user_id, text)
                elif any(word in text for word in ['профессия', 'статистика', 'smm', 'python', 'hr', 'дизайнер']):
                    if any(p in text for p in ['smm', 'python', 'hr', 'дизайнер']):
                        handle_profession_info(user_id, text)
                    else:
                        send_message(user_id, "🔍 <b>Статистика по профессиям</b>\n\nВыбери профессию:", get_profession_keyboard())
                
                # === ОБРАБОТКА ОТВЕТОВ НА ТЕСТ ===
                elif user.get("test_answers") is not None and user.get("test_current", 0) < 3:
                    if text.startswith('начать тест') or user.get("test_current", 0) == 0:
                        user["test_answers"] = []
                        user["test_current"] = 0
                        question = career_test_questions[0]
                        keyboard = VkKeyboard(one_time=False)
                        for opt in question["options"]:
                            keyboard.add_button(opt["text"], color=VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                        send_message(user_id, f"🧪 <b>Вопрос 1/3</b>\n\n{question['question']}", keyboard.get_keyboard())
                    elif any(opt["text"].lower() in text for q in career_test_questions for opt in q["options"]):
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
                                text = f"🎉 <b>Тест завершён!</b>\n\n<b>{result['title']}</b>\n{result['desc']}\n\n🔍 <b>Подходящие профессии:</b>\n" + "\n".join([f"• {p}" for p in result['professions']]) + f"\n\n📈 <b>Навыки для развития:</b>\n" + "\n".join([f"• {s}" for s in result['skills_to_develop']]) + f"\n\n📚 <b>Полезные ресурсы:</b>\n" + "\n".join([f"• {r}" for r in result['resources']]) + f"\n\n⚡ +100 XP"
                                send_message(user_id, text)
                                user["test_answers"] = None
                            else:
                                question = career_test_questions[user["test_current"]]
                                keyboard = VkKeyboard(one_time=False)
                                for opt in question["options"]:
                                    keyboard.add_button(opt["text"], color=VkKeyboardColor.PRIMARY)
                                    keyboard.add_line()
                                send_message(user_id, f"🧪 <b>Вопрос {user['test_current']+1}/3</b>\n\n{question['question']}", keyboard.get_keyboard())
                    continue
                
                # === ОБРАБОТКА СОБЕСЕДОВАНИЯ (с проверкой на красные флаги!) ===
                elif user.get("interview_mode", False):
                    q_idx = user.get("interview_question_idx", 0)
                    q_data = interview_questions[q_idx]
                    user_answer = text.lower()
                    
                    # Проверяем на красные флаги
                    red_flags = check_interview_red_flags(user_answer)
                    
                    # Проверяем на позитивные ключевые слова
                    found_keywords = [kw for kw in q_data["keywords"] if kw in user_answer]
                    keyword_count = len(found_keywords)
                    
                    # Формируем обратную связь
                    if red_flags:
                        # ⚠️ Нашли красные флаги!
                        feedback = "⚠️ <b>Внимание! Я заметил проблемные фразы:</b>\n\n"
                        for flag, advice in red_flags:
                            feedback += f"❌ «{flag}» → {advice}\n\n"
                        feedback += "\n💡 <b>Как лучше сказать:</b>\n"
                        feedback += f"{q_data['example_answer']}"
                        xp_gain = 10  # Меньше XP за ответ с красными флагами
                    elif keyword_count >= 2:
                        feedback = f"✅ <b>Отличный ответ!</b>\n\nТы упомянул: {', '.join(found_keywords)}\nЭто хорошие признаки!\n\n💡 <b>Пример идеального ответа:</b>\n{q_data['example_answer']}"
                        xp_gain = 25
                    elif keyword_count == 1:
                        feedback = f"👍 <b>Неплохо!</b>\n\nТы упомянул: {found_keywords[0]}\nПопробуй добавить больше конкретики.\n\n💡 <b>Пример идеального ответа:</b>\n{q_data['example_answer']}"
                        xp_gain = 15
                    else:
                        feedback = f"💡 <b>Можно лучше!</b>\n\nПопробуй добавить:\n• {q_data['tips']}\n\n💡 <b>Пример идеального ответа:</b>\n{q_data['example_answer']}"
                        xp_gain = 10
                    
                    user["interview_completed"] = user.get("interview_completed", 0) + 1
                    add_xp(user_id, xp_gain)
                    
                    if q_idx + 1 < len(interview_questions):
                        user["interview_question_idx"] += 1
                        next_q = interview_questions[q_idx + 1]
                        send_message(user_id, f"{feedback}\n\n⚡ +{xp_gain} XP\n\n🎤 <b>Вопрос {q_idx + 2}/{len(interview_questions)}</b>\n\n<b>{next_q['question']}</b>\n\n💡 Подсказка: {next_q['tips']}\n\nНапиши ответ 👇")
                    else:
                        user["interview_mode"] = False
                        if user["interview_completed"] >= 3 and "interview_pass" not in user["achievements"]:
                            user["achievements"].append("interview_pass")
                            add_xp(user_id, 50)
                            bonus = "\n\n🎉 <b>+50 XP за прохождение всех вопросов!</b>"
                        else:
                            bonus = ""
                        send_message(user_id, f"{feedback}\n\n⚡ +{xp_gain} XP\n\n🎉 <b>Собеседование завершено!</b>\n\nВсего пройдено: {user['interview_completed']} вопросов{bonus}")
                    continue
                
                # === ОБРАБОТКА КНОПОК ВАКАНСИЙ ===
                elif '✅' in text and 'подходит' in text:
                    vac_id = user["current_vacancy"]
                    if vac_id < len(vacancies):
                        if vac_id not in user["matched_vacancies"]:
                            user["matched_vacancies"].append(vac_id)
                            if "first_match" not in user["achievements"]:
                                user["achievements"].append("first_match")
                                add_xp(user_id, 50)
                        user["current_vacancy"] += 1
                        add_xp(user_id, 20)
                        vac = vacancies[vac_id]
                        send_message(user_id, f"✅ <b>Отлично!</b>\n\n{vac['title']} в {vac['company']}\n\n🔗 {vac['link']}\n\n⚡ +20 XP")
                        handle_vacancies(user_id)
                
                elif '❌' in text or 'не подходит' in text:
                    user["current_vacancy"] += 1
                    handle_vacancies(user_id)
                
                elif '⏭️' in text or 'далее' in text:
                    user["current_vacancy"] += 1
                    handle_vacancies(user_id)
                
                elif '🛑' in text or 'стоп' in text:
                    send_message(user_id, f"🛑 <b>Остановлено!</b>\n\n💕 В избранном: {len(user['matched_vacancies'])}\n👀 Посмотрено: {user['current_vacancy'] + 1}")
                
                # === ОБРАБОТКА ЗАДАНИЙ ===
                elif '✅' in text and 'выполнил' in text:
                    available = [i for i in range(len(daily_tasks)) if i not in user["completed_tasks"]]
                    if available:
                        task_id = random.choice(available)
                        user["completed_tasks"].append(task_id)
                        user["tasks_completed"] += 1
                        xp = daily_tasks[task_id]["xp"]
                        add_xp(user_id, xp)
                        if "first_task" not in user["achievements"]:
                            user["achievements"].append("first_task")
                            add_xp(user_id, 50)
                        send_message(user_id, f"✅ <b>Выполнено!</b>\n\n+{xp} XP")
                
                elif '🔄' in text or 'другое' in text:
                    handle_tasks(user_id)
                
                # === ОБРАБОТКА НАВЫКОВ ===
                elif 'добавить навык' in text:
                    skill_name = text.replace('добавить навык', '').strip()
                    if len(skill_name) >= 3 and skill_name not in user["skills"]:
                        user["skills"][skill_name] = 1
                        add_xp(user_id, 10)
                        send_message(user_id, f"✅ <b>Навык добавлен!</b>\n\n🛠️ {skill_name} — уровень 1/5\n\n⚡ +10 XP")
                    else:
                        send_message(user_id, "⚠️ Введи название навыка (мин. 3 символа) или навык уже добавлен!")
                
                elif 'прокачать' in text or '⬆️' in text:
                    if not user["skills"]:
                        send_message(user_id, "⚠️ Сначала добавь навыки!")
                    else:
                        kb = []
                        for skill_name, level in user["skills"].items():
                            if level < 5:
                                kb.append([VkKeyboardButton(f"⬆️ {skill_name} ({level}/5)", color=VkKeyboardColor.PRIMARY)])
                        if not kb:
                            send_message(user_id, "🏆 Все навыки на максимуме!")
                        else:
                            keyboard = VkKeyboard(one_time=False)
                            for btn in kb:
                                keyboard.add_button(btn[0].text, color=btn[0].color)
                                keyboard.add_line()
                            send_message(user_id, "⬆️ <b>Выбери навык для прокачки:</b>", keyboard.get_keyboard())
                
                # === ОБРАБОТКА РЕЗЮМЕ ===
                elif 'чек-лист' in text or '📋' in text:
                    handle_resume(user_id)
                
                elif 'отметить' in text or '✅' in text:
                    checklist_items = ["📸 Фотография", "📞 Контакты", "💼 Опыт работы", "🎓 Образование", "🛠️ Навыки", "🏆 Достижения", "📄 Формат PDF", "✅ Нет ошибок"]
                    kb = []
                    for i, item in enumerate(checklist_items):
                        if not user["resume_checklist"][i]:
                            kb.append([VkKeyboardButton(item, color=VkKeyboardColor.PRIMARY)])
                    if not kb:
                        send_message(user_id, "🎉 Все пункты отмечены!")
                    else:
                        keyboard = VkKeyboard(one_time=False)
                        for btn in kb:
                            keyboard.add_button(btn[0].text, color=btn[0].color)
                            keyboard.add_line()
                        send_message(user_id, "✅ <b>Отметь выполненный пункт:</b>", keyboard.get_keyboard())
                
                # === ОБРАБОТКА СОПРОВОДИТЕЛЬНОГО ===
                elif 'создать письмо' in text:
                    send_message(user_id, "✏️ <b>Создание сопроводительного письма</b>\n\nНапиши в следующем сообщении:\n1. Твоё имя\n2. Позиция (вакансия)\n3. Компания\n4. 3-5 навыков (через запятую)\n5. Контакты (телефон/почта/телеграм)\n6. Опыт (необязательно)\n\nПример:\nАнна, SMM-менеджер, Digital Agency, контент/аналитика/креатив, @anna, 2 года в маркетинге")
                    user["cover_letter_data"] = {"step": 1}
                
                elif user.get("cover_letter_data", {}).get("step", 0) > 0:
                    data = text.split(',')
                    if len(data) >= 5:
                        name, position, company, skills_raw, contact = [s.strip() for s in data[:5]]
                        skills = [s.strip() for s in skills_raw.split('/')]
                        experience = data[5].strip() if len(data) > 5 else ""
                        
                        letter = f"<b>Тема:</b> Отклик на вакансию \"{position}\"\n\n<b>Уважаемая команда {company}!</b>\n\nМеня зовут {name}, и я хочу откликнуться на вакансию <b>\"{position}\"</b>.\n\n{experience if experience else 'Я считаю, что мой опыт и навыки соответствуют требованиям этой позиции.'}\n\n<b>Мои ключевые навыки:</b>\n" + "\n".join([f"• {skill}" for skill in skills]) + f"\n\n<b>Почему я хочу работать у вас:</b>\nМеня привлекает возможность развиваться в {company} и применять свои навыки для решения интересных задач.\n\n<b>Что я могу предложить:</b>\n• Готовность к обучению и развитию\n• Ответственный подход к работе\n• Умение работать в команде\n• {skills[0] if skills else 'Профессионализм'}\n\n<b>Контакты для связи:</b>\n{contact}\n\nС уважением и готовностью к сотрудничеству,\n{name}\n\n<i>Письмо сгенерировано ботом Ворон Кар 🖤</i>"
                        user["cover_letter_data"] = {}
                        add_xp(user_id, 30)
                        send_message(user_id, f"📬 <b>Твоё сопроводительное письмо:</b>\n\n{letter}\n\n<i>📋 Скопируй и отправь работодателю!</i>\n\n⚡ +30 XP")
                    else:
                        send_message(user_id, "⚠️ Заполни все поля через запятую! Пример: Анна, SMM-менеджер, Digital Agency, контент/аналитика, @anna")
                    continue
                
                # === ПО УМОЛЧАНИЮ ===
                else:
                    send_message(user_id, "Используй кнопки внизу или напиши 'привет' для меню", get_main_keyboard())
        
        except Exception as e:
            logging.error(f"Ошибка обработки: {e}")
            continue

if __name__ == '__main__':
    main()
