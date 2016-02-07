# dcbackup

## Info
Highly opinionated backup tool for docker-compose.yml based containers.

## Features
 - Backup and restore volumes
 - Backups are made in incremental fashion to save disk space
 - To exclude certain sub-folders just add an empty .backupignore file inside
 - When mysql container is detected mysqldump is used

## Requirements
 - docker
 - docker-py
 - python 2.7
 - rdiff-backup
 - python-yaml

## Assumptions
This tool takes as input folder containing docker app(s). Each app folder should contain:
 - ./data - folder with state-full assets
 - ./docker-compose.yaml
 - each mysql container needs to be called mysql and contain below section:
```yaml
   environment:
       MYSQL_ROOT_PASSWORD: xxxxx
```

## Usage
Backup all apps:
```bash
$ ./dcbackup --apps-path=/path/to/apps --backup-path=server::/backup/location --command=backup
```
Backup single app
```bash
$ ./dcbackup --apps-path=/path/to/apps/appname --backup-path=server::/backup/location --command=backup
```


## Disclaimer
This is just a hack, I can't guarantee if it works or if I'll provide any updates, patches or tests.
You have been warned, use it on your own risk!

However, if you think you have patches, found a bug or cool idea which this project would benefit from, feel free to contribute!


## Todo
 - Restore functionality
