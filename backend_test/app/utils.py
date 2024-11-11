from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def get_status_message(message, error_message=None, response_success=False):
    if message:
        return message
    elif error_message:
        return str(error_message)
    elif response_success:
        return "Success"
    else:
        return "Failed"


class ResponseWrapper(Response):
    def __init__(
        self,
        data=None,
        error_code=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        error_message=None,
        message=None,
        reason=None,
        response_success=None,
        status=None,
        **kwargs,
    ):
        res_success = True
        if error_code is None and status is not None:
            if status > 299 or status < 200:
                error_code = status
                res_success = False
        if error_code is not None:
            res_success = False

            if not reason and message:
                reason = message

            data = {
                "code": str(error_code),
                "reason": reason,
                "message": get_status_message(message, error_message, res_success),
                "status": str(status),
            }
        custom_headers = {}
        if res_success:
            if "results" in data:
                custom_headers["count"] = data.pop("count")
                custom_headers["next"] = data.pop("next")
                custom_headers["previous"] = data.pop("previous")
                data = data.pop("results")

        super().__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=custom_headers if res_success else headers,
            exception=exception,
            content_type=content_type,
        )


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]

        message = None

        if response.status_code in [400, 401, 403, 404, 405, 409, 500]:
            error_code = response.status_code
            reason = data.get("reason", None)

            if data:
                message = data.get("message", None)

            output_data = {
                "code": str(error_code),
                "reason": reason,
                "message": message,
                "status": str(response.status_code),
            }
            return super().render(output_data, accepted_media_type, renderer_context)

        return super().render(data, accepted_media_type, renderer_context)


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        response = ResponseWrapper(
            code=400,
            message=str(exc),
            status=400,
            referenceError="Bad Request",
            baseType="Bad Request",
            schemaLocation="Bad Request",
            type="Bad Request",
        )

    if response.status_code == 404:
        response.data["code"] = response.status_code
        response.data["status_code"] = response.status_code
        response.data["referenceError"] = "Detail Not Found"
        try:
            response.data["reason"] = "Unable to find with ID:{}".format(
                context.get("kwargs", {}).get("pk")
            )
            response.data["message"] = "Unable to find with ID:{}".format(
                context.get("kwargs", {}).get("pk")
            )
            if str(exc) == "":
                response.data["reason"] = "Please provide valid ID"
                response.data["message"] = "Please provide valid ID"
        except Exception:
            response.data["reason"] = str(exc)
            response.data["message"] = str(exc)
        response.data["@baseType"] = "Detail Not Found"
        response.data["@schemaLocation"] = "Detail Not Found"
        response.data["@type"] = "Detail Not Found"

        return response

    try:
        if (
            response.data["reason"]
            == "Please provide valid ID, It should not contain '_'"
            or response.data["referenceerror"]
            == "Please provide valid ID, It should not contain '_"
        ):
            return response
    except Exception:
        return response

    # Now add the HTTP status code to the response.
    if (
        response.data["message"]
        == "Required headers are missing, please verify and try again"
        or response.data["reason"]
        == "Please provide all the necessary and required http headers"
        or response.data["referenceerror"]
        == "Please provide all the necessary and required http headers"
    ):
        return response
