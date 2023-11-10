from os import getenv
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


@dataclass
class DatabaseConfig:
    DB_NAME = getenv('DB_NAME')
    DB_PORT = getenv('DB_PORT')
    DB_HOST = getenv('DB_HOST')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_USER = getenv('DB_USER')

    driver: str = 'asyncpg'
    database_system = 'postgresql'

    def build_connection_str(self) -> str:
        """
        This function build a connection string
        """
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.DB_USER,
            database=self.DB_NAME,
            password=self.DB_PASSWORD,
            port=self.DB_PORT,
            host=self.DB_HOST,
        ).render_as_string(hide_password=False)


@dataclass
class BotConfig:
    BOT_TOKEN = getenv('BOT_TOKEN')
    BOT_NAME = getenv('BOT_NAME')


@dataclass
class RedisConfig:
    """Redis connection variables."""

    db: int = int(getenv('REDIS_DATABASE', 1))
    """ Redis Database ID """
    host: str = getenv('REDIS_HOST', 'redis')
    port: int = int(getenv('REDIS_PORT', 6379))
    state_ttl: int | None = getenv('REDIS_TTL_STATE', None)
    data_ttl: int | None = getenv('REDIS_TTL_DATA', None)


@dataclass
class Configuration:
    db = DatabaseConfig()
    bot = BotConfig()
    redis = RedisConfig()
    nats_server = 'nats://localhost:4222'
    admin_ids = ['822248811', '827961067']


conf = Configuration()
