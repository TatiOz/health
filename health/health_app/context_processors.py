from health_app.models import MenuItem

#FOR ALL PAGES, redisred in settings
def menu_items(request):
    if request.user.is_authenticated:
        menu = MenuItem.objects.all()
    else:
        menu = MenuItem.objects.filter(authenticated_only=False)
    return {'menu': menu}