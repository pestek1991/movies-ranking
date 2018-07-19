# -*- coding: utf-8 -*-



from django.http import HttpResponse
from django.shortcuts import render



def test(request):
    return HttpResponse("Witojcie u mnnie :)")


def main_site(request):
    return render(request, 'index.html')


def err404(request):
    return HttpResponse("404 kolego! <hr> <a href='/'>go to main page</a>")



