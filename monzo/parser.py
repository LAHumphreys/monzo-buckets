from monzo.request import auth_json_request
from monzo.json_response import make_array, make_scalar
from monzo.session_context import MonzoContext


def _parse_array(response: str, Scalar):
    result = make_array(Scalar)()
    result._load(response)
    return result


def _parse_object(response: str, Scalar):
    result = make_scalar(Scalar)()
    result._load(response)
    return result


def _get_array(context: MonzoContext, endpoint: str, Scalar):
    response = auth_json_request(context, endpoint)
    return _parse_array(response, Scalar)


def _get_object(context: MonzoContext, endpoint: str, Scalar):
    response = auth_json_request(context, endpoint)
    return _parse_object(response, Scalar)
