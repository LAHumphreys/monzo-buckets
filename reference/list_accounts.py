from monzo.session_context import load_context
from monzo.accounts import get_accounts

context = load_context("../config/authenticated.json")

print(get_accounts(context))
