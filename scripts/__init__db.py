from dotenv import load_dotenv
from app.db import connect_db

load_dotenv()


if __name__ == "__main__":
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        with open("scripts/imoveis.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()

        for stmt in sql_script.split(";"):
            if stmt.strip():
                cursor.execute(stmt)

        conn.commit()
        cursor.close()
        conn.close()