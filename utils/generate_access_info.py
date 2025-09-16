import random
from datetime import datetime, timedelta

# Случайные данные для сотрудников
surnames = ["Иванова", "Петрова", "Сидорова", "Кузнецова", "Смирнова", "Васильева", "Попова", "Новикова", "Федорова", "Морозова"]
names = ["Анна", "Мария", "Елена", "Ольга", "Наталья", "Ирина", "Светлана", "Татьяна", "Юлия", "Екатерина"]
male_surnames = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Васильев", "Попов", "Новиков", "Федоров", "Морозов"]
male_names = ["Алексей", "Дмитрий", "Сергей", "Андрей", "Михаил", "Владимир", "Александр", "Иван", "Максим", "Артем"]

# Системы и сервисы
systems = [
    'CRM "Амелия"',
    'ERP "Галактика"',
    '1C:Предприятие',
    'Jira',
    'Confluence',
    'Bitbucket',
    'Сервер мониторинга (Zabbix)',
    'Система документооборота',
    'База данных Oracle',
    'Виртуальный рабочий стол'
]

# Комментарии для доступов
access_comments = [
    "Доступ предоставлен для анализа данных",
    "Доступ для решения инцидентов",
    "Технический доступ для разработки",
    "Доступ для мониторинга системы",
    "Административные права",
    "Доступ для тестирования новых функций",
    "Резервный доступ на время отпуска коллеги",
    "Доступ для аудита безопасности",
    "Временный доступ для проекта",
    "Полный доступ к системе"
]

# Почтовые ящики
mailboxes = [
    "support@company.com",
    "info@company.com",
    "sales@company.com",
    "devops@company.com",
    "hr@company.com",
    "finance@company.com",
    "it-support@company.com",
    "projects@company.com",
    "security@company.com",
    "monitoring@company.com"
]

# Назначения почтовых ящиков
mailbox_purposes = [
    "Общий ящик для обработки обращений клиентов",
    "Ящик для коммерческих предложений",
    "Ящик отдела продаж",
    "Экстренные уведомления от систем мониторинга",
    "Вопросы по кадровому делопроизводству",
    "Финансовые вопросы и отчетность",
    "Техническая поддержка пользователей",
    "Управление проектами и задачами",
    "Вопросы информационной безопасности",
    "Мониторинг и оповещения систем"
]

def generate_random_date(start_year=2023):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")

def generate_employee_name():
    if random.choice([True, False]):
        return f"{random.choice(surnames)} {random.choice(names)}"
    else:
        return f"{random.choice(male_surnames)} {random.choice(male_names)}"

def generate_access_entry():
    employee = generate_employee_name()
    date = generate_random_date(2023)
    system = random.choice(systems)
    comment = random.choice(access_comments)
    
    if random.random() < 0.3:
        comment += f". Запрос от руководителя отдела {generate_employee_name()}."
    elif random.random() < 0.6:
        comment += f". Запрос через тикет в Jira (PROJ-{random.randint(100, 999)})."
    
    return f"""[Сотрудник]: {employee}
[Дата получения доступа]: {date}
[Система]: {system}
[Комментарий]: {comment}

---"""

def generate_mailbox_entry():
    mailbox = random.choice(mailboxes)
    date = generate_random_date(2022)
    responsible_count = random.randint(1, 3)
    responsible = ", ".join([generate_employee_name() for _ in range(responsible_count)])
    purpose = random.choice(mailbox_purposes)
    
    return f"""[Почтовый ящик]: {mailbox}
[Дата создания]: {date}
[Ответственные]: {responsible}
[Назначение]: {purpose}.

---"""

# Генерируем содержимое файла
content = """# Информация о доступах сотрудников

"""

# Добавляем 5-8 записей о доступах
for _ in range(random.randint(5, 8)):
    content += generate_access_entry() + "\n\n"

content += """
# Информация о почтовых ящиках

"""

# Добавляем 3-5 записей о почтовых ящиках
for _ in range(random.randint(3, 5)):
    content += generate_mailbox_entry() + "\n\n"

# Сохраняем в файл
filename = "информация_о_доступах.txt"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Файл '{filename}' успешно создан!")
print(f"Создано записей: {content.count('---')}")
