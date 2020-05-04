from logging import getLogger
from invoke import task


logger = getLogger(__name__)


@task
def tests(context, verbose=True, coverage=True):
    """Run test cases."""
    logger.info("Running test cases")
    context.run("python manage.py test")
    logger.info("Done")


@task
def clean(context, bytecode=False, extra=''):
    """Clean up cache files."""
    logger.info("Cleaning cache files")
    context.run("find . -type f -name \"*.py[co]\" -exec rm -r {} +")
    context.run("find . -type d -name \"__pycache__\" -exec rm -r {} +")
    logger.info("Done")
