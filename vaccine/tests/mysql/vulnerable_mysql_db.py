from fastapi import FastAPI, Request, HTTPException
import mysql.connector
from mysql.connector import Error
import time

DB_CONFIG = {
    "host": "mysql",
    "user": "notroot",
    "password": "notpassword",
    "database": "vulnerable_app"
}

def init_db():
    try:
        retries = 0
        for x in range(5):
            try:
                retries += 1
                conn = mysql.connector.connect(
                    host=DB_CONFIG["host"],
                    user=DB_CONFIG["user"],
                    password=DB_CONFIG["password"]
                )
                break
            except Exception as e:
                if retries >= 5:
                    return e
                print(f"Connection attempt {retries + 1} failed. Retrying in 5 seconds...")
                time.sleep(5)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.close()
        
        # Connect to the database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL
        )
        """)
        
        # Check if users already exist
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert sample users
            users = [
                ('1', 'admin', 'admin123'),
                ('2', 'user', 'user123'),
                ('3', 'hacker', 'hacker123'),
                ('4', 'guest', 'guest123')
            ]
            
            cursor.executemany(
                "INSERT INTO users (id, username, password) VALUES (%s, %s, %s)",
                users
            )
            
            conn.commit()
            print("Database initialized with sample users")
        
        conn.close()
    except Error as e:
        print(f"Error initializing database: {e}")

app = FastAPI()

init_db()

@app.get("/")
def root():
    return {"msg": "MySQL app is up"}

@app.get("/user")
async def get_user(id: str):
    """
    Vulnerable to Union-based SQL Injection, Payloads:
        '
        ' UNION SELECT '1', VERSION() -- 
        ' UNION SELECT username, password FROM users LIMIT 1 OFFSET 0 -- 
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = f"SELECT id, username FROM users WHERE id = '{id}'"
        print("Executing query:", query)
        
        cursor.execute(query)
        user = cursor.fetchall()
        conn.close()
        
        print("Query result:", user)
        if user:
            return { "user": user }
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        return {"error": f"{e}"}

@app.post("/login")
async def login(request: Request):
    """
    Vulnerable to Error-based SQL Injection, Payloads:
    {
        "username": "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT password FROM users WHERE username='admin'),0x7e)) -- ",
        "password": "anything"
    }
    """
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Vulnerable to SQL injection
        query = f"SELECT id, username FROM users WHERE username = '{username}' AND password = '{password}'"
        print("Executing query:", query)
        
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        print("Query result:", user)
        if user:
            return {"message": "Login successful", "user": user}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        return {"error": f"{e}"}
