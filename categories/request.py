import sqlite3
import json
from models import Category

def get_all_categorys():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            c.id,
            c.label         
        FROM Categories c
        """
        )

        # Initialize an empty list to hold all category representations
        categorys = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an category instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Category class above.
            category = Category(
                row["id"],
                row["label"],                
            )

            categorys.append(category.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(categorys)


def get_single_category(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            c.id,
            c.label            
        FROM Categories c
        WHERE c.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an category instance from the current row
        category = Category(
            data["id"],
            data["label"]            
        )

        return json.dumps(category.__dict__)

def create_category(new_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            (id, label)
        VALUES (?, ?);
        """, (new_category['id'], new_category['label'], ))
        

        id = db_cursor.lastrowid
        new_category['id'] = id
    return json.dumps(new_category)

def get_categories_by_label(label):

    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        WHERE c.label = ?
        """, ( label, ))

        categories = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'], row['label'])
            categories.append(category.__dict__)

    return json.dumps(categories)

def get_categories_by_id(id):

    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
        FROM Categories c
        WHERE c.id = ?
        """, ( id, ))

        categories = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'], row['label'])
            categories.append(category.__dict__)

    return json.dumps(categories)