from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить скидку', 'url_name': 'add_sale'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]


# mixin class for pagination and dry on main views
class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:  # dont displaying add_sale in user dont login
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
