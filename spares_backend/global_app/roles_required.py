import json
from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def roles_required(*allowed_roles):
    """
    Problem:
        You want to restrict access to a view or function based on the user's role.

    Solution:
        Create a decorator function that takes a list of allowed roles as input and checks if the user's role is in the list. If the user's role is in the list, the view or function is allowed to be accessed. If the user's role is not in the list, the view or function is not allowed to be accessed.

    Usage:
        @roles_required('admin', 'project admin')
        def my_view(request):
            # Access granted to admin and project admin users only
            ...
    
    Test Cases:
        - Test case 1: User with role 'admin' only should be able to access the services.
        - Test case 2: User with role 'admin' and 'project admin',
          should be able to access user management.

    Solution:
        Decorator that checks if user role is in the allowed roles list.

    Args:
        *allowed_roles: A list of strings representing allowed user roles.

    Returns:
        A decorator function.

    Logic:
        1. Get the user's role from the request.
        2. Check if the user's role is in the allowed roles list.
        3. If the user's role is in the allowed roles list, return the original function.
        4. Otherwise, return an error message and HTTP status code.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.role.role in allowed_roles:
                return func(request, *args, **kwargs)
            else:
                response_data = json.dumps({
                    'status': 'error',
                    'message': 'You are not authorized to access this service.'
                })
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        return wrapper

    return decorator
