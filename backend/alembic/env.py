from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Import app settings and metadata so Alembic can autogenerate migrations.
from app.core.config import settings
from app.db.session import Base

# Import all models here so they register on Base.metadata before autogenerate.
from app.models.user import User  # noqa: F401
from app.models.preferences import UserPreferences  # noqa: F401

# Alembic Config object (reads alembic.ini).
config = context.config

# Inject the database URL from our .env-backed settings.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging setup.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate' support.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (emits SQL without a DBAPI connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with a live DBAPI connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
