import inspect
import peewee
import peewee_async

from .migrations import _create_tables, _make_migrations
from tg_bot_template.config.settings import settings
import tg_bot_template.infrastructure.db.models as models

ALL_TABLES = [data for _, data in inspect.getmembers(models) if isinstance(data, peewee.ModelBase)]
_db_manager: peewee_async.Manager | None = None

def setup_db(settings: settings) -> peewee_async.Manager:
    global _db_manager
    # psql postgresql://tg_bot_user:tg_bot_user@localhost:5432/tg_bot_user
    # ---------------- DB INIT ----------------
    database = peewee_async.PooledPostgresqlDatabase(
        settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
    )
    database.bind(ALL_TABLES)

    # ---------------- MIGRATIONS ----------------
    # _dev_drop_tables(database, ALL_TABLES)  # noqa: ERA001
    _create_tables(database, ALL_TABLES)
    _make_migrations(database)

    database.close()
    _db_manager = database.set_allow_sync(False)

    return peewee_async.Manager(database)


def get_db_conn() -> peewee_async.Manager:
    return setup_db(settings)
