from django.contrib.auth.models import Group

def user_group_context(request):
    if request.user.is_authenticated:
        is_manager = request.user.groups.filter(name="Менеджер").exists()
    else:
        is_manager = False
    return {'is_manager': is_manager}
