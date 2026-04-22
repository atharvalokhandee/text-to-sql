import sqlite3, os

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/sample.db")

conn.executescript("""
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        country TEXT
    );

    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        created_at TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    INSERT INTO customers VALUES (1, 'Alice',  'alice@mail.com',  'India');
    INSERT INTO customers VALUES (2, 'Bob',    'bob@mail.com',    'USA');
    INSERT INTO customers VALUES (3, 'Carol',  'carol@mail.com',  'UK');
    INSERT INTO customers VALUES (4, 'David',  'david@mail.com',  'India');
    INSERT INTO customers VALUES (5, 'Emma',   'emma@mail.com',   'Canada');

    INSERT INTO orders VALUES (1, 1, 1500.0, '2024-01-10');
    INSERT INTO orders VALUES (2, 1, 2200.0, '2024-02-15');
    INSERT INTO orders VALUES (3, 2,  800.0, '2024-03-01');
    INSERT INTO orders VALUES (4, 3, 3200.0, '2024-03-20');
    INSERT INTO orders VALUES (5, 4,  950.0, '2024-04-05');
    INSERT INTO orders VALUES (6, 5, 4100.0, '2024-04-18');
    INSERT INTO orders VALUES (7, 2, 1300.0, '2024-04-22');
""")

conn.commit()
conn.close()
print("Database seeded successfully.")