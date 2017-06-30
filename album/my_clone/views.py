from django.shortcuts import render
from django.views import *

# Create your views here.
from django.core.urlresolvers import reverse_lazy

class MainPage(View):

    def get(self, request):
        context = {
            "content": "Strona glowna albumu!",
            "title": "Main Page",
        }
        return render(request, "main_page.html", context)
