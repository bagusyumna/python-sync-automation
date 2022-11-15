import os
import logging
import datetime
from controllers.controller import ControllerSync


def main():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    date_today = datetime.datetime.now().date().strftime("%d_%m_%Y")
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] - %(message)s', filename=f'{base_dir}/logs/log_sync_{date_today}.log', filemode='w')

    controller = ControllerSync()
    controller.sync_karyawan()

if __name__ == '__main__':
    main()
