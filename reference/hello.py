from monzo.session_context import load_context
from monzo.ping import who_am_i

context = load_context("../config/authenticated.json")

print(who_am_i(context))
