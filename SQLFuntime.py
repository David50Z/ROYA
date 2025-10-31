import os
import psycopg2
import time
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # we'll set this in .env

DATABASE_URL = os.environ["DATABASE_URL"]
if "?sslmode=" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

def require_ssl(u: str) -> str:
    p = urlparse(u)
    q = dict(parse_qsl(p.query))
    q.setdefault("sslmode", "require")
    return urlunparse(p._replace(query=urlencode(q)))

conn1 = psycopg2.connect(DATABASE_URL)
cur1 = conn1.cursor()


def get_connection():
    return psycopg2.connect(require_ssl(DATABASE_URL))




def find_numbers(): 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM numbers
        """,
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_message(num, message):
    print(num)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE numbers SET messages = array_append(messages, %s) WHERE number = %s
        """, (message,  str(num))
    )
    updated = cur.rowcount
    conn.commit()
    conn.close()
    if updated == 0:
        return False
    else:
        return True

def get_messages(num):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT messages FROM numbers where number = %s
        """, (str(num),)
    )
    row = cur.fetchall()
    conn.close()
    print(row)
    flat = [msg for (inner,) in row for msg in inner]
    return flat



def create_number(num, message):
    conn = get_connection()
    cur = conn.cursor()
    id = int(time.time() * 1000)
    cur.execute(
        """
        INSERT INTO numbers (id, number, messages) VALUES (%s, %s, %s)
        """, (id,  "+1" + str(num), [message])
    )
    # row = cur.fetchone()
    print("ROOOOW")
    # print(row)
    conn.commit()
    conn.close()

    return True


def get_number_or_create_number(num, message):
    print("\n\n\n\n" + str(num) + "\n\n\n\n")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT messages FROM numbers where number = %s
        """, ( str(num),)
    )
    row = cur.fetchall()
    if row == None:
        create_number(num, message)
    
        cur.execute(
        """
        SELECT messages FROM numbers where number = %s
        """, ( str(num),)
        )
        row = cur.fetchall()
        conn.close()
        return row
    else:
        conn.close()
        return row
        
        
print(get_messages("+1777"))
#print(insert_message(7256001255, "."))