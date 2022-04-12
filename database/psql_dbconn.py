from sqlalchemy.engine import create_engine
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
# DB Setup
engine = create_engine(
    f'postgresql+psycopg2://{os.getenv("PSQL_USERNAME")}:{os.getenv("PSQL_PASSWORD")}'
    f'@{os.getenv("PSQL_HOSTNAME")}:5433/'
    f'{os.getenv("PSQL_DBNAME")}')
