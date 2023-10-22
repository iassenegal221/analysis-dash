# myapp/views.py
from django.shortcuts import render
from dashapp.dashboard import app
from dash import Dash

def dash_view(request):
    return render(request, "dashapp/dashboard.html")

def dash_ajax(request):
    dash_instance = Dash(__name__, server=False)
    app.init_app(dash_instance)

    return HttpResponse(content=dash_instance.serve_layout(), content_type='text/html')
