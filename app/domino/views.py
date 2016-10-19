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
        #
        # spin up vpn (vpnc, openvpn) container with assigned private
        # network
        pass

    create_vpn_container(server)

    return render(request, 'sshlogon.html', {"server": server})

def create_vpn_container(server):
    vpn = server.vpn

    cli = Client(base_url='unix://var/run/docker.sock')
    container = cli.create_container(
        image='implemento/vpn', detach=True,
        host_config=cli.create_host_config(
            port_bindings={3000: 3000},
            binds={'/var/run/docker.sock': {
                'bind': '/var/run/docker.sock',
                'mode': 'rw'
            }
        }),
        command='')

    response = cli.start(container=container.get('Id'))
