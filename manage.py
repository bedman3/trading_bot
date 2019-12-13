"""Django's command-line utility for administrative tasks."""
import os
import sys

from main.util.logger.init_logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info('Enter main')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    logger.info('Finish import main.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
