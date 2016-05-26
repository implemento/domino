from django.shortcuts import render


def index(request, server_id):
    return render(request, 'index.html', {"server_id": server_id}, content_type="text/html")
