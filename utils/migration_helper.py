from alembic.config import Config
from alembic import command

from engine.db import engine

from utils.logger_helper import logger

alembic_cfg = Config(f"alembic.ini")


def run_migrations_online():
    logger.warning("about to run migrations")
    try:
        with engine.begin() as connection:
            alembic_cfg.attributes['connection'] = connection
            command.upgrade(alembic_cfg, "head")

            logger.warning("Migrations upgraded!!")
    except Exception as e:
        logger.error(f"Error running migrations. Error detail: {e}")
