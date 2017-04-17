import docker

base_url='unix://var/run/docker.sock'


def find_container(needle):
    cli = docker.APIClient(base_url='unix://var/run/docker.sock',version='1.24')
    for container in cli.containers():
        for name in container['Names']:
            if needle in name:
                return container
    return False
