from django.shortcuts import render
from django.views import View


class BaseView(View):

    def get(self, request):
        context = {
            'turn_on_block': False,
            'page_role': 'home'
        }
        return render(request, 'base.html', context=context)
