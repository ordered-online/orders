import json
from json import JSONDecodeError

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse

from . import settings
from .models import Session


class SuccessResponse(JsonResponse):
    def __init__(self, response=None, *args, **kwargs):
        if response is None:
            super().__init__({
                "success": True,
            }, *args, **kwargs)
        else:
            super().__init__({
                "success": True,
                "response": response
            }, *args, **kwargs)


class AbstractFailureResponse(JsonResponse):
    reason = None

    def __init__(self, *args, **kwargs):
        super().__init__({
            "success": False,
            "reason": self.reason
        }, *args, **kwargs)


class IncorrectAccessMethod(AbstractFailureResponse):
    reason = "incorrect_access_method"


class MalformedJson(AbstractFailureResponse):
    reason = "malformed_json"


class IncorrectCredentials(AbstractFailureResponse):
    reason = "incorrect_credentials"


class VerificationServiceUnavailable(AbstractFailureResponse):
    reason = "verification_service_unavailable"


class LocationServiceUnavailable(AbstractFailureResponse):
    reason = "location_service_unavailable"


class CodeServiceUnavailable(AbstractFailureResponse):
    reason = "code_service_unavailable"


def debug_session(request, session_code) -> TemplateResponse:
    """Render a session to debug web sockets."""
    return render(request, "orders/debug_session.html", {
        "session_code": session_code
    })


def verify_user(data: dict) -> tuple:
    """Verify the user with the verification service."""
    session_key = data.get("session_key")
    if not session_key:
        raise ValueError()
    user_id = data.get("user_id")
    if not user_id:
        raise ValueError()

    # send a post request to the verification service endpoint
    response = requests.post(
        "{}/verification/verify/".format(settings.VERIFICATION_SERVICE_URL),
        data=json.dumps({"session_key": session_key, "user_id": user_id})
    )
    verification_data = response.json()
    if verification_data.get("success") is not True:
        raise ValueError()

    return user_id, session_key


def verify_location_owner(user_id, location_id):
    """Verify, that the user is the location owner."""

    # send a get request to the locations service endpoint
    response = requests.get("{}/locations/get/{}/".format(
        settings.LOCATIONS_SERVICE_URL, location_id
    ))
    location_data = response.json()
    if location_data.get("success") is not True:
        raise ValueError()

    # unwrap the user_id from the location data
    location_object = location_data.get("response")
    if not location_object:
        raise ValueError()
    location_user_id = location_object.get("user_id")
    if not location_user_id:
        raise ValueError()

    if user_id != location_user_id:
        raise ValueError()


def fetch_code() -> str:
    """Fetch a new code from the codes service."""
    response = requests.get("{}/codes/new/".format(
        settings.CODES_SERVICE_URL
    ))
    code_data = response.json()
    if code_data.get("success") is not True:
        raise ValueError()
    try:
        return code_data["response"]["value"]
    except KeyError:
        raise ValueError()


def create_session(request) -> JsonResponse:
    """Create a session via POST."""

    if request.method != "POST":
        return IncorrectAccessMethod()

    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return MalformedJson()

    try:
        user_id, _ = verify_user(data)
    except ValueError:
        return IncorrectCredentials()
    except requests.ConnectionError:
        return VerificationServiceUnavailable()

    location_id, name = data.get("location_id"), data.get("name")
    if not location_id or not name:
        return MalformedJson()

    try:
        verify_location_owner(user_id, location_id)
    except ValueError:
        return IncorrectCredentials()
    except requests.ConnectionError:
        return LocationServiceUnavailable()

    try:
        code = fetch_code()
    except (requests.ConnectionError, ValueError):
        return CodeServiceUnavailable()

    session = Session.objects.create(
        name=name,
        code=code,
        location_id=location_id,
    )

    return SuccessResponse(session.dict_representation)
