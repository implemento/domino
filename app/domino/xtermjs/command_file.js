function xtermjs_initContainer() {
    var container_name = "{{ container_name }}";
    var server_name = "{{ server_name }}"

    term.socket.send("docker exec -it " + container_name + " ssh " + server_name);
}
