from monzo.ping.whoami import WhoAmI
from monzo.parser import _get_object
from monzo.session_context import MonzoContext

def who_am_i(context: MonzoContext) -> WhoAmI:
    return _get_object(context, "ping/whoami", WhoAmI)