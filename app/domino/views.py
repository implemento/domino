from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from .models import Server
from docker import Client
from . import generate_xtermjs_command_file
from .docker import Docker


def index(request):
    servers = Server.objects.order_by('name')
    return render(request, 'index.html', {"servers": servers})


class OpenTerminalRedirectView(RedirectView):

    xtermjs_start_port = 3000
    xtermjs_current_port = xtermjs_start_port

    cli = Client(base_url='unix://var/run/docker.sock')

    def create_vpn_config_file(self, server):
        fp = open('/config/'+server.customer.vpn.container_name+'.conf', mode='w', encoding='utf8')

        fp.write(server.customer.vpn.conf_file)
        fp.close()

        return fp.name

    def create_host_config_vpn(self):
        host_config = self.cli.create_host_config(
            port_bindings={3000: 3000},
            privileged=True,
            binds={'/var/run/docker.sock': {
                        'bind': '/var/run/docker.sock',
                        'mode': 'rw'},
                   'domino_config': {
                        'bind': '/config',
                        'mode': 'ro'},
                  })

        return host_config

    def create_host_config_xtermjs(self, xtermjs_config_file):
        host_config = self.cli.create_host_config(
            port_bindings={3000: 3000},
            privileged=True,
            binds={'/var/run/docker.sock': {
                        'bind': '/var/run/docker.sock',
                        'mode': 'rw'},
                   'domino_config': {
                        'bind': '/config',
                        'mode': 'ro'}
                  })

        return host_config

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
            volumes=['/config'],
            host_config=self.create_host_config_vpn(),
            command=vpn_command + ' ' + vpn_conf_file)

        self.cli.start(container=vpn_container.get('Id'))

    def get_container_by_name(self, container_name):
        for container in self.cli.containers(all=True):
            if '/'+container_name in container['Names']:
                return container

        return None

    def create_xtermjs_container(self, server):
        container_name = 'xtermjs_port' + str(self.xtermjs_current_port)
        xtermjs_config_file = generate_xtermjs_command_file.generate_xtermjs_command_file(server, container_name)

        xtermjs_container = self.cli.create_container(
            image='implemento/xtermjs',
            detach=True,
            name=container_name,
            volumes=['/config'],
            host_config=self.create_host_config_xtermjs(xtermjs_config_file),
            command='npm start'
        )

        self.cli.start(container=xtermjs_container.get('Id'))
        Docker.copy(None, xtermjs_config_file, '/config/command_file.js', container_name);


    def get_redirect_url(self, *args, **kwargs):
        server = Server.objects.get(pk=kwargs['server_id'])
        if server.customer.vpn is not None:
            self.create_vpn_container(server)

        self.create_xtermjs_container(server)

        return super(OpenTerminalRedirectView, self).get_redirect_url(*args, **kwargs)
