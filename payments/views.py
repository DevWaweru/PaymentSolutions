from django.shortcuts import render

# Create your views here.
def index(request):
    title = 'home'

    return render(request, 'index.html',{
        'title':title,
    })