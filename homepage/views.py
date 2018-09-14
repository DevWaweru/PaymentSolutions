from django.shortcuts import render

# Create your views here.
def home(request):
    title = 'Home'
    
    return render(request, 'index.html', {
        'title':title,
    })