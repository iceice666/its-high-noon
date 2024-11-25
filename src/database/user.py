import dataclasses
import logging
from typing import Dict, List

import psycopg2

LOGGER = logging.getLogger("db.user")


@dataclasses.dataclass
class Users:
    id: str
    enabled: bool
    lang: str


class UsersManager:
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: int = 5432):
        """Initialize database connection."""
        try:
            LOGGER.info(f"Connecting to database {dbname}@{host}:{port}")
            self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        except psycopg2.Error as e:
            raise Exception(f"Unable to connect to database: {e}")

        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        try:
            self.conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS Users
                (
                    id      text NOT NULL PRIMARY KEY,
                    enabled boolean NOT NULL DEFAULT FALSE,
                    lang  text NOT NULL DEFAULT 'en'
                );
            """)
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Error creating user table: {e}")

    def disconnect(self) -> None:
        """Close database connection."""
        self.conn.close()

    def add_user(self, user_id: str) -> bool:
        """Add a user to the database."""
        try:
            (self.conn.cursor()
            .execute(
                """INSERT INTO Users (id, enabled) VALUES (%s, False)""",
                (user_id,)))

            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Error creating user table: {e}")

    def remove_user(self, user_id: str) -> bool:
        """Delete a user by its ID."""
        try:
            with self.conn.cursor() as cur:
                query = "DELETE FROM Users WHERE id = %s"
                cur.execute(query, (user_id,))
                self.conn.commit()
                return cur.rowcount > 0
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Error deleting question: {e}")

    def toggle_enabled(self, user_id: str) -> bool:
        """Toggle the enabled status of a user."""
        try:
            with self.conn.cursor() as cur:
                query = "UPDATE Users SET enabled = NOT enabled WHERE id = %s"
                cur.execute(query, (True, user_id))
                return cur.rowcount > 0
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Error updating question: {e}")

    def get_enabled_users(self) -> Dict[str, List[str]]:
        """Return a list of enabled users."""
        try:
            with self.conn.cursor() as cur:
                query = "SELECT id, lang FROM Users WHERE enabled = TRUE"
                cur.execute(query)
                result = cur.fetchall()
                users = {}

                for user_id, lang in result:
                    users.get(lang, []).append(user_id)

                return users

        except psycopg2.Error as e:
            raise Exception(f"Error getting enabled users: {e}")

    def get_all_users(self) -> List[str]:
        """Return a list of all users."""
        try:
            with self.conn.cursor() as cur:
                query = "SELECT id FROM Users"
                cur.execute(query)
                result = cur.fetchall()
                return [x for x, in result]
        except psycopg2.Error as e:
            raise Exception(f"Error getting all users: {e}")
