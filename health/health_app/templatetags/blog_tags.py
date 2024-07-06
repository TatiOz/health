from django import template
# import health.health_app.views as views
from ..models import Blog_category, MenuItem

register = template.Library()

@register.simple_tag()
def get_categories():
    return Blog_category.objects.all()


# Blog_category.objects.all().blog_set.all()
# Blog.object.filter(category_id=1)

@register.inclusion_tag('health_app/list_blog_categories.html')
def show_blog_categories(cat_blog_selected=0):
    blog = Blog_category.objects.all()
    return {'blog': blog, 'selected_cat': cat_blog_selected}


# @register.inclusion_tag('health_app/list_blog_categories.html')
# def show_blog_categories(cat_blog_selected=0):
#     cats = Blog_category.objects.all()
#     return {'cats': cats, 'selected_cat': cat_blog_selected}


# @register.inclusion_tag('health_app/menu.html')
# def show_menu(cat_blog_selected=0):
#     menu = MenuItem.objects.all()
#     return {'menu': menu, 'selected_cat': cat_blog_selected}
