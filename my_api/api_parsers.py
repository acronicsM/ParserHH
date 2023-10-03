from my_api import api

agg_post = api.parser()
agg_post.add_argument("id", type=str, location="form")