'''
author: zhangquanwei
Date: 2025-03-07 22:32:24
'''
from tortoise import connections


async def create_upload_chunk_and_update_file_codes_table():
    conn = connections.get("default")
    await conn.execute_script(
        """
        ALTER TABLE "filecodes" ADD COLUMN "file_hash" VARCHAR(128);
        ALTER TABLE "filecodes" ADD COLUMN "is_chunked" BOOLEAN NOT NULL DEFAULT FALSE;
        ALTER TABLE "filecodes" ADD COLUMN "upload_id" VARCHAR(128);
        CREATE TABLE "uploadchunk" (
            id SERIAL PRIMARY KEY,
            "upload_id" VARCHAR(36) NOT NULL,
            "chunk_index" INT NOT NULL,
            "chunk_hash" VARCHAR(128) NOT NULL,
            "total_chunks" INT NOT NULL,
            "file_size" BIGINT NOT NULL,
            "chunk_size" INT NOT NULL,
            "created_at" TIMESTAMPTZ NOT NULL,
            "file_name" VARCHAR(255) NOT NULL,
            "completed" BOOLEAN NOT NULL
        );
    """
    )


async def migrate():
    await create_upload_chunk_and_update_file_codes_table()
