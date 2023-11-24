def user_first_name(request):
    if request.user.is_authenticated:
        return {'user_first_name': request.user.first_name}
    return {}
