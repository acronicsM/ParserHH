# API: Что хотят от джуна
## _API - проекта "juniors skills"_ 

API позволяет парсить HH.ru по списку запросов, выявлять ключевые навыки вакансий и производить анализ вакансий и навыков

## Возможности

- Добавлять и удалять поисковые запросы
- Запускать парсер по поисковым запросам, удалять снятые с публикации вакансии
- Получать список и детальные данные вакансии
- Получать список навыков вакансии
- Получать список вакансий навыка
- Удалять навыки
- Получать результаты анализа (в разработке)

## Стек
- [Flask]
- [SQLAlchemy]
- [pandas]
- [seaborn]
- [BeautifulSoup]

## Установка
    Установка docker на debian: https://docs.docker.com/engine/install/debian/
    Авторизация на docker hub: sudo docker login
    Загрузка образа: sudo docker pull meacronics/my_api_hh:v21092023
    Запуск образа: sudo docker run -p 5000:5000 --rm -d meacronics/my_api_hh:v21092023
