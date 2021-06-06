from django.shortcuts import render
from django.urls import reverse
from django import views


class Index(views.View):
    def get(self, request):
        context = {
            "sock_url": reverse('browsersocket', urlconf='robitcontrol.routing')
        }
        return render(request, 'robitcontrol/index.html', context=context)
