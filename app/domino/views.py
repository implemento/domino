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

    cli = Client(base_url='unix://var/run/docker.sock')
    container = cli.create_container(image='xtermjs',
                                     port_bindings={ 3000: [ 3001, 3002]}, detach=True)
    print(container)
    return render(request, 'sshlogon.html', {"server": server})
