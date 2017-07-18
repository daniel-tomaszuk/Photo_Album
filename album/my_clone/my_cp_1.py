def is_logged(request):
    if request.user.is_authenticated:
        context = {
            "logged": True,
            "user": request.user.username
        }
    else:
        context = {
            "logged": False,
        }
    return context