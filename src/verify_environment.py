from sqlalchemy import create_engine, text

CONNECTION_STRING = "postgresql+psycopg2://dss150p:dss150p_lab@localhost:5432/dss150p_lab"

def main():
    engine = create_engine(CONNECTION_STRING)
    try:
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version();")).scalar()
            db_name = conn.execute(text("SELECT current_database();")).scalar()
            print("Connection successful.")
            print("PostgreSQL version:", version)
            print("Connected to database:", db_name)
    except Exception as exc:
        print("Connection FAILED:", exc)
        raise

if __name__ == "__main__":
    main()