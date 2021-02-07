from monzo.session_context import load_context, to_json
from monzo.request import refresh_login

context = load_context("../config/authenticated.json")

refresh_login(context)
with open("../config/authenticated.json", mode="w") as gen_cfg:
    print(to_json(context), file=gen_cfg)
