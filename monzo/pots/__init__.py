from typing import List

from monzo.session_context import MonzoContext
from monzo.parser import _get_array
from monzo.pots.pot import Pot
from monzo.accounts import Account


def get_pots(context: MonzoContext, acc: Account) -> List[Pot]:
    params = {
        "current_account_id": acc.id
    }
    response = _get_array(context, "pots", "pots", Pot, params=params)
    return response.get_items()


def get_active_pots(context: MonzoContext, acc: Account) -> List[Pot]:
    return [pot for pot in get_pots(context, acc) if not pot.deleted]
