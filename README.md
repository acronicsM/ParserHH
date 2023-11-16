# skills-guide_parser

Сервис проекта skills_guide по парсингу вакансий их хранению 

## 🛠️ Подготовка в запуску

1. [Download and install Python](https://www.python.org/downloads/) (Version 3.10+ is recommended).

2. Клонируйте репозиторий GitHub:
```bash
git clone https://github.com/acronicsM/ParserHH.git
```
3. Перейдите в директорию проекта:
```bash
cd ParserHH
```
4. Установите переменные окружения:
```bash
nano .env
```
5. (Рекомендуется) Создайте виртуальную среду Python::
[Python official documentation](https://docs.python.org/3/tutorial/venv.html).


```
python3 -m venv venv
```

6. Активируйте виртуальную среду:
   - On Windows:
   ```
   .\venv\Scripts\activate
   ```
   - On macOS and Linux:
   ```
   source venv/bin/activate
   ```
7. Установите необходимые пакеты Python из `requirements.txt`:

```
pip install -r requirements.txt
```

8. Запустите `app.py`


## 💡 Использование
После запуска документация API доступа по адресу http://localhost:5000/swagger/

## 🙌 Необходимы переменные окружения

1. DB_DRIVER - Драйвер подключения к БД. В текущей конфигурации выбор ограничивается только драйверов postgresql, в случаи указания любого другого драйвера или не указания драйвера вовсе используется бд sqlite:///base1.db
2. POSTGRES_USER - Пользователь для подключения к postgre
3. POSTGRES_PASSWORD - Пароль пользователя для подключения к postgre
4. POSTGRES_HOST - адрес хоста бд postgre
5. POSTGRES_PORT - порт хоста бд postgre
6. POSTGRES_DATABASE_PARSER - имя БД postgre
7. ENV - выбор между production (запускает приложение на localhost) и development
8. DEBUG - вкл/выкл режима отладки
9. SECRET_KEY
10. JWT_SECRET_KEY - для доступа к методам 

     - /**/aggregators**[POST, DELETE]; 
     - **/job_search_queries**[POST, DELETE]; 
     - **/update_vacancies**[GET] 
     - **/auth/token/refresh**[POST]
     - **/auth/users**[GET]

## 🚀 Общие принципы работы

1. **/aggregators[POST]** - Добавление агрегатор вакансий (Cейчас доступен только HH)
2. **/job_search_queries[POST]** - Добавление нового поискового запроса (например python junior)
3. **/update_vacancies[GET]** - Запуск парсера вакансий по всем поисковым запросам и агрегаторам
4. **/vacancies[GET]** - Список актуальных вакансий
