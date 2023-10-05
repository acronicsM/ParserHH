#
# @app.route('/home')
# def index():
#     return jsonify(index_data())
#
#
# @app.route('/update_vacancy')
# def get_update_vacancy():
#     if search_query := request.args.get('query'):
#         return jsonify(update_vacancies(query=search_query))
#     else:
#         if all_query := Query.query.all():
#             return jsonify([update_vacancies(query=search_query) for search_query in all_query])
#         else:
#             return 'no key "query"', 400
#
#
# @app.route('/vacancies')
# def vacancies():
#     per_page, page, = 10, 0
#     tag_id = search_query = None
#
#     if _per_page := request.args.get('per_page'):
#         per_page = min(int(_per_page), per_page)
#
#     if _page := request.args.get('page'):
#         page = int(_page)
#
#     if _tag_id := request.args.get('tag_id'):
#         tag_id = int(_tag_id)
#
#     if _query := request.args.get('query'):
#         search_query = int(_query)
#
#     count, result = get_all_vacancies(page=page, per_page=per_page, tag_id=tag_id, query_id=search_query)
#
#     return jsonify({'found': count,
#                     'result': [vacancy.to_dict() for vacancy in result]
#                     })
#
#
# @app.route('/get_vacancy/<int:vacancy_id>')
# def get_vacancy(vacancy_id):
#     return jsonify(get_vacancy_by_id(vacancy_id).to_dict_detail())
#
#
# @app.route('/get_vacancy_tags/<int:vacancy_id>')
# def get_vacancy_tags(vacancy_id):
#     return jsonify(get_vacancy_skills(vacancy_id))
#
#
# @app.route('/tags')
# def tags():
#     per_page, page = 100, 0
#
#     if _per_page := request.args.get('per_page'):
#         per_page = min(int(_per_page), per_page)
#
#     if _page := request.args.get('page'):
#         page = int(_page)
#
#     return jsonify(get_all_skills(per_page=per_page, page=page))
#
#
# @app.route('/tags/<int:tags_id>')
# def get_tag_vacancies(tags_id):
#     return get_skill_vacancies(skill_id=tags_id)
#
#
# @app.route('/query/<int:query_id>')
# def query_vacancy(query_id):
#     return jsonify(get_vacancy_query(query_id))
#
#
# @app.route('/query', methods=['GET', 'POST', 'DELETE'])
# def query():
#     if request.method == 'GET':
#         return jsonify(get_query())
#     elif request.method == 'POST':
#         if query_name := request.args.get('query_name'):
#             return post_query(query_name)
#
#         return status_400()
#     elif request.method == 'DELETE':
#         if query_id := request.args.get('query_id'):
#             return delete_query(query_id)
#
#         return status_400()
#
#     return status_405()
#
#
# @app.route('/agg', methods=['GET', 'POST', 'DELETE'])
# def aggregators():
#     if request.method == 'GET':
#         return jsonify(get_aggregators())
#     elif request.method == 'POST':
#         if query_name := request.args.get('name'):
#             return post_aggregator(name=query_name)
#
#         return status_400()
#     elif request.method == 'DELETE':
#         if query_id := request.args.get('name'):
#             return delete_aggregator(query_id)
#
#         return status_400()
#
#     return status_405()
#
#
# @app.route('/get_images')
# def update_static():
#     return 'work get_images'
