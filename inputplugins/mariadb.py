import os
import logging
from lib import shell
from dockerutil import demon
from dockerutil import compose


def backup(app_path, dest_path):
    app_compose_path = app_path + '/docker-compose.yml'
    app_name = os.path.basename(app_path)
    compose_config = compose.load(app_compose_path)
    mariadb_containers = extract_mariadb_containers_from_config(compose_config)

    for k, v in mariadb_containers:
        password = get_password(v)
        if password:
            container_meta = demon.find_container("/" + app_name + "_mariadb_")
            if container_meta:
                mysqldump('root', password, container_meta['Names'][0][1:], 'mariadb' ,dest_path)


def extract_mariadb_containers_from_config(compose_config):
    mariadb_containers = []

    if 'version' in compose_config and 'services' in compose_config:
        services = compose_config['services']
    else:
        services = compose_config

    for k, v in services.items():
        if "mariadb" == k:
            mariadb_containers.append((k, v))

    if mariadb_containers.count == 0:
        return False
    else:
        return mariadb_containers


def get_password(container_config):
    if 'environment' in container_config:
        env = container_config['environment']
        if 'MARIADB_ROOT_PASSWORD' in env:
            return env['MARIADB_ROOT_PASSWORD']
    return False


def mysqldump(user, password, cnt_full_name, cnt_name, dest_path):
    dest_full_path = dest_path + "/" + cnt_name + ".sql.gz"
    command = "docker exec -i " + cnt_full_name + " sh -c \"MYSQL_PWD=" + password + " mysqldump -u " + user + \
              " --all-databases --add-drop-database --routines -E --triggers --single-transaction | gzip\" > " + \
              dest_full_path
    shell.retry_run([command], 3)
    statinfo = os.stat(dest_full_path)
    logging.info("Saved mariadb db: " + dest_full_path + " using : " + str(statinfo.st_size/1024/1024) + " MB")
    return True
