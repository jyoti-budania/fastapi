from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLQLCHEMY_DATABASE_URL='postgresql://postgres:2207@localhost/demo'

engine=create_engine(SQLQLCHEMY_DATABASE_URL)


sessionlocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base=declarative_base()

