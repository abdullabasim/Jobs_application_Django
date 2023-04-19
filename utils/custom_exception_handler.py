from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__
    print(exception_class)

    if exception_class == 'AuthenticationFailed' :
        response.data = {
            "error" : "Invalid username and password"
        }
    if exception_class == 'NotAuthenticated':
        response.data = {
            "error": "Login first to access this resource"
        }

    if exception_class == 'InvalidToken':
        response.data = {
            "error": "Your authentication token is expired , please login again!"
        }

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response