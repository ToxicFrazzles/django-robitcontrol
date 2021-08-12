from django.shortcuts import render
from django.urls import reverse_lazy
from django import views
from ..models import Robit


class Index(views.View):
    def get(self, request):
        context = {
            "sock_url": "/robitcontrol" + reverse_lazy('browsersocket', urlconf='robitcontrol.routing')
        }
        if request.user.is_superuser or request.user.is_staff:
            context["robots"] = Robit.objects.exclude(channel_name=None)
        else:
            context["robots"] = Robit.objects.filter(available=True).exclude(channel_name=None)
        return render(request, 'robitcontrol/index.html', context=context)
