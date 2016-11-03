from jinja2 import Environment, FileSystemLoader
import tempfile

#TODO eseguire la funzione correttamente
def generate_xtermjs_command_file(server, container_name):
    templateEnv = Environment(loader=FileSystemLoader(''))
    template = templateEnv.get_template('./xtermjs/command_file.js')
    templateVars = {
        'container_name': container_name
    }

    file_content = template.render(templateVars)

    fp = tempfile.NamedTemporaryFile(prefix="/config/", delete=False)
    fp.write(file_content.encode("utf8"))
    fp.close()

    return fp.name
