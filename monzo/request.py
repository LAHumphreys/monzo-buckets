from urllib import request, parse
from monzo.session_context import MonzoContext
from http.client import HTTPResponse
import json

BASE_URL: str = "https://api.monzo.com/"


class InvalidAuthorization(Exception):
    pass


def parse_bearer_token(auth_response: HTTPResponse, context: MonzoContext):
    values = json.load(auth_response)
    if "token_type" not in values:
        raise InvalidAuthorization
    elif "access_token" not in values:
        raise InvalidAuthorization
    else:
        context.access_token = values["access_token"]
        context.refresh_token = values["refresh_token"]


def complete_login(context: MonzoContext):
    url = BASE_URL + "oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": context.client_id,
        "client_secret": context.client_secret,
        "redirect_uri": context.redirect_uri,
        "code": context.client_code
    }
    encoded_data = parse.urlencode(data).encode("UTF-8")

    token_request = request.Request(url, data=encoded_data, method="POST")
    token_request.add_header("Content-Type", "application/x-www-form-urlencoded")
    parse_bearer_token(request.urlopen(token_request), context)


def refresh_login(context: MonzoContext):
    url = BASE_URL + "oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": context.client_id,
        "client_secret": context.client_secret,
        "code": context.client_code,
        "refresh_token": context.refresh_token
    }
    encoded_data = parse.urlencode(data).encode("UTF-8")

    token_request = request.Request(url, data=encoded_data, method="POST")
    token_request.add_header("Content-Type", "application/x-www-form-urlencoded")
    parse_bearer_token(request.urlopen(token_request), context)


def auth_json_request(context: MonzoContext, endpoint):
    url = BASE_URL + endpoint
    token_request = request.Request(url, method="GET")
    token_request.add_header("Authorization", "Bearer " + context.access_token)

    with request.urlopen(token_request) as response:
        result = json.load(response)
    return result
