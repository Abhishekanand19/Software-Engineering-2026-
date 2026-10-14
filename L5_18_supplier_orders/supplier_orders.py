"""Module for managing and auditing supplier orders."""

import sqlite3
import subprocess


def create_database():
    """Initialize an in-memory SQLite database and orders table."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            supplier TEXT,
            item TEXT,
            quantity INTEGER,
            received INTEGER
        )
        """
    )
    return conn


def place_order(conn, supplier, item, quantity):
    """Insert a new order using parameterized queries."""
    conn.execute(
        "INSERT INTO orders "
        "(supplier, item, quantity, received) VALUES (?, ?, ?, 0)",
        (supplier, item, quantity),
    )
    return quantity


def mark_received(conn, order_id, remarks=None):
    """Mark an order as received in the database."""
    _ = remarks
    conn.execute(
        "UPDATE orders SET received = 1 WHERE id = ?",
        (order_id,),
    )


def notify_warehouse(supplier):
    """Notify warehouse about a supplier safely via subprocess."""
    subprocess.run(
        ["echo", f"notifying warehouse about {supplier}"],
        check=True,
    )


def cleanup(conn):
    """Remove all received orders from the database."""
    try:
        conn.execute("DELETE FROM orders WHERE received = 1")
    except sqlite3.OperationalError as error:
        print(f"Cleanup failed: {error}")


def pending_count(conn):
    """Return count of pending orders."""
    cursor = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    )
    return cursor.fetchone()[0]


def main():
    """Run the main supplier orders workflow."""
    conn = create_database()
    order_total = 0

    order_total += place_order(conn, "Acme Steel", "rods", 40)
    order_total += place_order(conn, "Bolt Co", "bolts", 500)
    mark_received(conn, 1, "ok")
    notify_warehouse("Acme")

    print(pending_count(conn), order_total)
    cleanup(conn)
    conn.close()


if __name__ == "__main__":
    main()