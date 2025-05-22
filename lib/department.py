from __init__ import CURSOR, CONN


class Department:


    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"
        
from __init__ import CURSOR, CONN

class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create the departments table if it doesn't exist."""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the departments table if it exists."""
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()   
    
    def save(self):
        """Save the Department instance to the database and assign an id."""
        if self.id is None:  # If there's no id, we need to insert it
            sql = """
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.location))
            CONN.commit()

            # Retrieve the id of the last inserted row
            self.id = CURSOR.lastrowid
        else:
            sql = """
                UPDATE departments
                SET name = ?, location = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.location, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Create a new department and return the Department instance."""
        department = cls(name, location)  # Create an instance with the given data
        department.save()  # Save the department to the database
        return department  # Return the department instance   
    
    def update(self):
        """Update the department's row in the database with the current attribute values."""
        if self.id is None:
            raise ValueError("Cannot update a department that has not been saved to the database.")
        
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the department's corresponding row in the database."""
        if self.id is None:
            raise ValueError("Cannot delete a department that has not been saved to the database.")
        
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()