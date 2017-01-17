from django.core.exceptions import PermissionDenied

def reviewer(function):
    """
    Enable all writes only for authenticated users.
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous():
            raise PermissionDenied
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap