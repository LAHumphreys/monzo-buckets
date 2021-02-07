from monzo.session_context import load_context
from monzo.accounts import get_retail_accounts
from monzo.balance import get_balance
from monzo.pots import get_active_pots

context = load_context("../config/authenticated.json")

for acc in get_retail_accounts(context):
    balance = get_balance(context, acc)
    print("Balance   £{0:.2f}".format(balance.total_balance / 100.0))
    print("    {0:20s}: £{1:.2f}".format("Unassigned", balance.balance / 100.0))
    for pot in get_active_pots(context, acc):
        print("    {0:20s}: £{1:.2f}".format(pot.name, pot.balance/100.0))
