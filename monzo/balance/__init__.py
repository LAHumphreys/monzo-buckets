from monzo.parser import _get_object
from monzo.session_context import MonzoContext
from monzo.accounts import Account
from monzo.balance.balance import Balance


def get_balance(context: MonzoContext, acc: Account) -> Balance:
    params = {
        "account_id": acc.id
    }
    return _get_object(context, "balance", Balance, params=params)
