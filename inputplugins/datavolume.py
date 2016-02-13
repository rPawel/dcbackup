from lib import shell

rdiff_backup = "/usr/bin/rdiff-backup"
remove_older_than = "10D"


def backup(app_path, dst_path):
    app_data_path = app_path + "/data"
    backup_cmd = rdiff_backup + " --verbosity 1 --exclude-device-files --exclude-fifos --exclude-sockets " \
                                "--exclude-if-present .backupignore " + app_data_path + " " + dst_path
    shell.retry_run([backup_cmd], 3)

    remove_old_cmd = rdiff_backup + " --verbosity 1 --remove-older-than " + remove_older_than + " --force " + dst_path
    shell.retry_run([remove_old_cmd], 3)
