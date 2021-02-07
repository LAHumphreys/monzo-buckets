from typing import List

from monzo.session_context import MonzoContext
from monzo.parser import _get_array
from monzo.accounts.account import Account


def get_accounts(context: MonzoContext) -> List[Account]:
    response = _get_array(context, "accounts", "accounts", Account)
    return response.get_items()
