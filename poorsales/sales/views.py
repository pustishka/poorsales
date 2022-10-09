from django.http import HttpResponse
from django.shortcuts import render

# main page for site
def index(request):
    return HttpResponse('Main page of sales app')


# function responsible for places
def places(request):
    return HttpResponse('<h1>Discounts by places</h1>')