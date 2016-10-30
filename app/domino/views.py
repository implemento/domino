from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from .models import Server
from docker import Client
import tempfile


def index(request):
    servers = Server.objects.order_by('name')
    return render(request, 'index.html', {"servers": servers})


class OpenTerminalRedirectView(RedirectView):

    cli = Client(base_url='unix://var/run/docker.sock')
    #permanent = False
    #query_string = True
    #pattern_name = 'sshlogon'

    def create_vpn_config_file(self, server):
        fp = open('/config/'+server.customer.vpn.container_name+'.conf', mode='w', encoding='utf8')

        fp.write(server.customer.vpn.conf_file)
        fp.close()

        return fp.name

    def create_vpn_container(self, server):
        vpn_conf_file = self.create_vpn_config_file(server)
        vpn_command = server.customer.vpn.vpn_type.command
        vpn_container_name = server.customer.vpn.container_name
        vpn_container = self.get_container_by_name(vpn_container_name)

        if vpn_container is not None:
            if vpn_container['State'] == 'exited':
                self.cli.start(container=vpn_container.get('Id'))
                return
            elif vpn_container['State'] == 'running':
                return

        vpn_container = self.cli.create_container(
            image='implemento/vpn',
            detach=True,
            name=vpn_container_name,
            volumes=['domino_config:/config'],
            host_config=self.cli.create_host_config(
                port_bindings={3000: 3000},
                binds={'/var/run/docker.sock': {
                            'bind': '/var/run/docker.sock',
                            'mode': 'rw'},
                      }),
            command="vpnc --no-detach /config/mumed_vpn.conf")
            #command=vpn_command + ' ' + vpn_conf_file)

        print(vpn_command + ' ' + vpn_conf_file)

        self.cli.start(container=vpn_container.get('Id'))

    def get_container_by_name(self, container_name):
        for container in self.cli.containers(all=True):
            if '/'+container_name in container['Names']:
                return container

        return None


    def get_redirect_url(self, *args, **kwargs):
        server = Server.objects.get(pk=kwargs['server_id'])
        if server.customer.vpn is not None:
            self.create_vpn_container(server)

        return super(OpenTerminalRedirectView, self).get_redirect_url(*args, **kwargs)
