"""
Author: Dimitris Gkoulis
Created on: Tuesday 24 June 2025
"""

__all__ = [
    "instantiate_internals",
    "insert",
    "get_first_by_source",
]

import os
import sqlite3
from typing import Optional


class _SqliteWrapper:
    _TABLE_NAME: str = "TranslationCache"

    def __init__(
        self, directory: str, name: str, make_directories: bool = True
    ) -> None:
        if make_directories is True:
            os.makedirs(directory, exist_ok=True)
        path_to_file: str = os.path.join(directory, name)
        self.conn = sqlite3.connect(path_to_file)
        self._create_table()

    def _create_table(self):
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection
        self.conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self._TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_language TEXT NOT NULL,
                source_value TEXT NOT NULL,
                target_language TEXT NOT NULL,
                target_value INTEGER NOT NULL
            )
        """
        )
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection
        self.conn.execute(
            f"""
               CREATE INDEX IF NOT EXISTS idx_source_language_source_value_target_language
               ON {self._TABLE_NAME} (source_language, source_value, target_language)
               """
        )
        self.conn.commit()

    def insert(
        self,
        source_language: str,
        source_value: str,
        target_language: str,
        target_value: str,
    ) -> None:
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection
        self.conn.execute(
            f"""
              INSERT INTO {self._TABLE_NAME} (source_language, source_value, target_language, target_value)
              VALUES (?, ?, ?, ?)
              """,
            (
                source_language,
                source_value,
                target_language,
                target_value,
            ),
        )
        self.conn.commit()

    def get_first_by_source(
        self, source_language: str, source_value: str, target_language: str
    ) -> Optional[tuple[str, str, str, str]]:
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection
        cursor = self.conn.execute(
            f"""
            SELECT source_language, source_value, target_language, target_value
            FROM {self._TABLE_NAME}
            WHERE source_language = ? AND source_value = ? AND target_language = ?
            LIMIT 1
            """,
            (source_language, source_value, target_language),
        )
        row = cursor.fetchone()
        return (row[0], row[1], row[2], row[3]) if row else None

    def close(self):
        self.conn.close()


_SQLITE_WRAPPER: Optional[_SqliteWrapper] = None


def instantiate_internals(name: str = "default.db") -> None:
    global _SQLITE_WRAPPER
    if _SQLITE_WRAPPER is not None:
        return
    _SQLITE_WRAPPER = _SqliteWrapper(
        directory=os.path.expanduser("~/.json-translation/"), name=name
    )


def insert(
    source_language: str, source_value: str, target_language: str, target_value: str
) -> None:
    _SQLITE_WRAPPER.insert(
        source_language=source_language,
        source_value=source_value,
        target_language=target_language,
        target_value=target_value,
    )


def get_first_by_source(
    source_language: str, source_value: str, target_language: str
) -> Optional[tuple[str, str, str, str]]:
    return _SQLITE_WRAPPER.get_first_by_source(
        source_language=source_language,
        source_value=source_value,
        target_language=target_language,
    )
