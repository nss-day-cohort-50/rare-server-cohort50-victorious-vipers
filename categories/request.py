def get_all_categorys():
    # Open a connection to the database
    with sqlite3.connect("./kennel.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            c.id,
            c.label         
        FROM category c
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
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            c.id,
            c.label            
        FROM category c
        WHERE c.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an category instance from the current row
        category = Category(
            data["id"],
            data["label"],            
        )

        return json.dumps(category.__dict__)