from django.shortcuts import render
from django.urls import reverse_lazy
from django import views


class Index(views.View):
    def get(self, request):
        context = {
            "sock_url": reverse_lazy('browsersocket', urlconf='robitcontrol.routing')
        }
        return render(request, 'robitcontrol/index.html', context=context)
