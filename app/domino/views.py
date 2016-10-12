from django.shortcuts import render
from django.http import HttpResponse
from .models import Server
from docker import Client


def index(request):
    servers = Server.objects.order_by('name')
    return render(request, 'index.html', {"servers": servers})

def sshlogon(request, server_id):
    server = Server.objects.get(pk=server_id)
    if server.vpn is not None:
        # spin up vpn (vpnc, openvpn) container with assigned private
        # network
        pass

    # spin up xtermjs container and attach it to private network

    return render(request, 'sshlogon.html', {"server": server})
