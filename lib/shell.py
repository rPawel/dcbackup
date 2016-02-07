import logging
from time import sleep
from subprocess import call

retry_interval = 0.1


def retry_run(command, retry):
    logging.info("Executing: " + ', '.join(command))
    for i in range(0, retry):
        try:
            status = call(command, shell=True)
            if 0 != status:
                raise ValueError('Shell did not return success: ' + str(status))
            return True

        except (IOError, ValueError):
            logging.exception("retrying in " + str(retry_interval * (i + 1)))
            sleep(retry_interval * (i + 1))
    logging.error("Giving up on: " + command)
    return False
