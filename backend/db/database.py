# db/database.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
from core.config import settings
from core.logger import db_logger

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, 
    echo=settings.LOG_SQL_QUERIES,
    connect_args={
        "timeout": 30,
        "autocommit": False,
    },
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if settings.LOG_SQL_QUERIES:
    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())
        db_logger.debug(f"SQL Query: {statement}")

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        if total > 0.1:
            db_logger.info(f"Slow SQL query took {total:.3f}s")

def get_db():
    db = SessionLocal()
    try:
        yield db
        db_logger.debug("Database session completed successfully")
    except Exception as e:
        db_logger.error(f"Database session error: {str(e)}", exc_info=True)
        raise
    finally:
        db.close()

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        db_logger.info("Database tables created successfully")
    except Exception as e:
        db_logger.error(f"Error creating tables: {e}", exc_info=True)
        raise