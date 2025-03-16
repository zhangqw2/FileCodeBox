'''
author: zhangquanwei
Date: 2025-03-07 22:32:24
'''
from tortoise import connections


async def create_file_codes_table():
    conn = connections.get("default")
    await conn.execute_script(
        """
        CREATE TABLE IF NOT EXISTS filecodes
        (
            id             SERIAL PRIMARY KEY,
            code           VARCHAR(255) NOT NULL UNIQUE,
            prefix         VARCHAR(255) DEFAULT '' NOT NULL,
            suffix         VARCHAR(255) DEFAULT '' NOT NULL,
            uuid_file_name VARCHAR(255),
            file_path      VARCHAR(255),
            size           INT DEFAULT 0 NOT NULL,
            text           TEXT,
            expired_at     TIMESTAMPTZ,
            expired_count  INT DEFAULT 0 NOT NULL,
            used_count     INT DEFAULT 0 NOT NULL,
            created_at     TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_filecodes_code_1c7ee7
            ON filecodes (code);
    """
    )


async def create_key_value_table():
    conn = connections.get("default")
    await conn.execute_script(
        """
        CREATE TABLE IF NOT EXISTS keyvalue
        (
            id         SERIAL PRIMARY KEY,
            key        VARCHAR(255) NOT NULL UNIQUE,
            value      JSONB,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_keyvalue_key_eab890
            ON keyvalue (key);
    """
    )


async def migrate():
    await create_file_codes_table()
    await create_key_value_table()
