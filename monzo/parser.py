from monzo.request import auth_json_request
from monzo.json_response import make_array, make_scalar
from monzo.session_context import MonzoContext


def _parse_array(response: str, scalar):
    result = make_array(scalar)
    result.parse_json_string_into_array(response)
    return result


def _parse_object(response: str, scalar):
    result = make_scalar(scalar)
    result.parse_json_string_into_object(response)
    return result


def _get_array(context: MonzoContext, endpoint: str, name: str, scalar, params: dict = None):
    response = auth_json_request(context, endpoint, params=params)[name]
    return _parse_array(response, scalar)


def _get_object(context: MonzoContext, endpoint: str, scalar, params: dict = None):
    response = auth_json_request(context, endpoint, params=params)
    return _parse_object(response, scalar)
