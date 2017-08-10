import os
import logging
from lib import shell
from dockerutil import demon
from dockerutil import compose


def backup(app_path, dest_path):
    app_compose_path = app_path + '/docker-compose.yml'
    app_name = os.path.basename(app_path)
    compose_config = compose.load(app_compose_path)
    mysql_containers = extract_mysql_containers_from_config(compose_config)

    for k, v in mysql_containers:
        password = get_password(v)
        if password:
            container_meta = demon.find_container("/" + app_name + "_mysql_")
            if container_meta:
                mysqldump('root', password, container_meta['Names'][0][1:], 'mysql' ,dest_path)


def extract_mysql_containers_from_config(compose_config):
    mysql_containers = []

    if 'version' in compose_config and 'services' in compose_config:
        services = compose_config['services']
    else:
        services = compose_config

    for k, v in services.items():
        if "mysql" == k:
            mysql_containers.append((k, v))

    if mysql_containers.count == 0:
        return False
    else:
        return mysql_containers


def get_password(container_config):
    if container_config.has_key('environment'):
        env = container_config['environment']
        if env.has_key('MYSQL_ROOT_PASSWORD'):
            return env['MYSQL_ROOT_PASSWORD']
    return False


def mysqldump(user, password, cnt_full_name, cnt_name, dest_path):
    dest_full_path = dest_path + "/" + cnt_name + ".sql.gz"
    command = "docker exec -i " + cnt_full_name + " MYSQL_PWD=" + password + " mysqldump -u " + user + \
              " --all-databases --add-drop-database --routines -E --triggers --single-transaction | gzip > " + \
              dest_full_path
    shell.retry_run([command], 3)
    statinfo = os.stat(dest_full_path)
    logging.info("Saved mysql db: " + dest_full_path + " using : " + str(statinfo.st_size/1024/1024) + " MB")
    return True
