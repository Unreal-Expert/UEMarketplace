from django.shortcuts import render

# Create your views here.
def frontpage(request):
    return render(request, 'core/frontpage.html')

def htmx_rocks(request):
    return render(request, 'core/partials/htmx_rocks.html')  