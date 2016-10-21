from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from .models import Server
from docker import Client
import tempfile
import os


def index(request):
    servers = Server.objects.order_by('name')
    return render(request, 'index.html', {"servers": servers})


class OpenTerminalRedirectView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'sshlogon'

    def create_vpn_container(self, server):
        vpn_conf_file_name = create_vpn_config_file(server)
        vpn_command = server.customer.vpn.vpn_type.command

        cli = Client(base_url='unix://var/run/docker.sock')
        container = cli.create_container(
            image='implemento/vpn', detach=True,
            host_config=cli.create_host_config(
                port_bindings={3000: 3000},
                binds={'/var/run/docker.sock': {
                            'bind': '/var/run/docker.sock',
                            'mode': 'rw'},
                       '/tmp/' + vpn_conf_file_name: {
                            'bind': '/config/vpn.conf',
                            'mode': 'ro'}
                      }),
            command=vpn_command)
        response = cli.start(container=container.get('Id'))

    def create_vpn_config_file(self, server):
        fp = tempfile.NamedTemporaryFile()
        fp.write(server.customer.vpn.conf_file)

        return os.path.basename(fp.name)

    def get_redirect_url(self, *args, **kwargs):
        server = Server.objects.get(pk=kwargs['server_id'])
        if server.customer.vpn is not None:
            #
            # spin up vpn (vpnc, openvpn) container with assigned private
            # network
            pass

        self.create_vpn_container(server)

        return super(OpenTerminalRedirectView, self).get_redirect_url(*args, **kwargs)


