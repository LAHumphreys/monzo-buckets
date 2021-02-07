from monzo.session_context import load_context, to_json
from monzo.request import complete_login

context = load_context("../config/connection.json")

complete_login(context)
with open("../config/authenticated.json", mode="w") as gen_cfg:
    print(to_json(context), file=gen_cfg)
