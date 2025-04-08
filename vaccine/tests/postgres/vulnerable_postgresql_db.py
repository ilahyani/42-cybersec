from fastapi import FastAPI, Request, HTTPException
import psycopg2
import time

# Database connection setup
def get_db_connection():
    retries = 0
    for x in range(5):
        try:
            retries += 1
            return psycopg2.connect(
                dbname="vulnerable_db",
                user="postgres",
                password="postgres",
                host="postgres_db",
                port="5432",
            )
        except Exception as e:
            if retries >= 5:
                return e
            print(f"Connection attempt {retries + 1} failed. Retrying in 5 seconds...")
            time.sleep(5)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id TEXT, username TEXT, password TEXT) ;")
    cursor.execute("INSERT INTO users (id, username, password) VALUES ('1', 'admin', 'admin123') ON CONFLICT DO NOTHING ;")
    cursor.execute("INSERT INTO users (id, username, password) VALUES ('2', 'user', 'user123') ON CONFLICT DO NOTHING ;")
    cursor.execute("INSERT INTO users (id, username, password) VALUES ('3', 'hacker', 'hacker123') ON CONFLICT DO NOTHING ;")
    cursor.execute("INSERT INTO users (id, username, password) VALUES ('4', 'guest', 'guest123') ON CONFLICT DO NOTHING ;")
    conn.commit()
    conn.close()

app = FastAPI()
init_db()

@app.get("/")
def root():
    return { "msg", "Postgres app is up" }

@app.get("/user")
async def get_user(id: str):
    """
    Vulnerable to Union-based SQL Injection, Payloads:
        '
        ' UNION SELECT '1', version() --
        ' UNION SELECT username, password FROM users LIMIT 1 OFFSET 0 -- 
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT id, username FROM users WHERE id = '{id}'"
        # query = f"{id}"
        print("Executing query:", query)
        cursor.execute(query)
        user = cursor.fetchall()
        print("Query result:", user)
        conn.close()

        if user:
            return { "user": user }
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        return { "error": f"{e}" }

@app.post("/login")
async def login(request: Request):
    """
    Vulnerable to Error-based SQL Injection, Payload:
    {
        "username": "' || (SELECT CAST((SELECT username || ':' || password FROM users LIMIT 1 OFFSET 0) AS INTEGER)) -- ",
        "password": "any"
    }
    """
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("Executing query:", query)
        cursor.execute(query, ())
        user = cursor.fetchone()
        conn.close()

        if user:
            return {"message": "Login successful", "user_id": user[0]}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    except Exception as e:
        return { "error": f"{e}" }
