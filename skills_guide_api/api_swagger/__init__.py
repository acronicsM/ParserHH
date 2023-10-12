from .aggregators.routes import ns as aggregators_ns
from .job_search_queries.routes import ns as queries_ns
from .update_vacancies.routes import ns as update_ns
from .vacancies.routes import ns as vacancies_ns
from .tags.routes import ns as tags_ns
from .index.routes import ns as index_ns
from .images.routes import ns as images_ns
from .auth.routes import ns as auth_ns

namespaces = [
    aggregators_ns,
    queries_ns,
    update_ns,
    vacancies_ns,
    tags_ns,
    index_ns,
    images_ns,
    auth_ns,
]
