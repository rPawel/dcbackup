from docker import Client

base_url='unix://var/run/docker.sock'


def find_container(needle):
    cli = Client(base_url='unix://var/run/docker.sock')
    for container in cli.containers():
        for name in container['Names']:
            if needle in name:
                return container
    return False
