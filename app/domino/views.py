from django.shortcuts import render
from django.http import HttpResponse
from .models import Server
from docker import Client


def index(request):
    servers = Server.objects.order_by('name')
    print("index chiamato!!")
    return render(request, 'index.html', {"servers": servers})

def sshlogon(request, server_id):
    # does it require vpn?
    server = Server.objects.get(pk=server_id)
    print("logon chiamato!!")

    # spin up vpn (vpnc, openvpn) container with assigned private
    # network

    # spin up xtermjs container and attach it to private network

    # redirect user to xtermjs browser page
    #servers = Server.objects.order_by('name')
    return render(request, 'webssh.html', {"server": server})
