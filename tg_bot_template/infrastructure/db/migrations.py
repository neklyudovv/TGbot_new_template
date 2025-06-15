import peewee
import peewee_async
import playhouse.migrate
from loguru import logger



def _dev_drop_tables(database: peewee_async.PooledPostgresqlDatabase, tables: list[peewee.ModelBase]) -> None:
    with database:
        database.drop_tables(tables, safe=True)
    logger.info("Tables dropped")


def _create_tables(database: peewee_async.PooledPostgresqlDatabase, tables: list[peewee.ModelBase]) -> None:
    with database:
        database.create_tables(tables, safe=True)
    logger.info("Tables created")


def _make_migrations(database: peewee_async.PooledPostgresqlDatabase) -> None:
    migrator = playhouse.migrate.PostgresqlMigrator(database)  # noqa: F841
    try:
        with database.atomic():
            playhouse.migrate.migrate(
                # migrator.add_column("users", "social_id", peewee.BigIntegerField(null=True)),  # noqa: ERA001
                # migrator.drop_not_null("users", "name"),  # noqa: ERA001
                # migrator.alter_column_type("users", "social_id", peewee.BigIntegerField(null=False)),  # noqa: ERA001
            )
        logger.info("Tables migrated")
    except peewee.ProgrammingError as e:
        logger.exception(f"Tables migrating error: {str(e)}")