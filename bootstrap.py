import sys
import logging
import argparse

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='/var/log/dcbackup.log'
)


def get_input_params():
    parser = argparse.ArgumentParser(description='Backup/restore container volumes')
    parser.add_argument('--command', required=True,
                        help='command')
    parser.add_argument('--apps-path', metavar='apps_path', required=True,
                        help='input path')
    parser.add_argument('--backup-path', metavar='backup_path', required=True,
                        help='backup path')

    return parser.parse_args()


def exit_with_error():
    get_help_line()
    sys.exit(2)
