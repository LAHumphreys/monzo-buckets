from typing import List

from monzo.session_context import MonzoContext
from monzo.parser import _get_array
from monzo.accounts.account import Account


def get_accounts(context: MonzoContext) -> List[Account]:
    response = _get_array(context, "accounts", "accounts", Account)
    return response.get_items()

def get_retail_accounts(context: MonzoContext) -> List[Account]:
    return [acc for acc in get_accounts(context) if acc.type == "uk_retail"]
