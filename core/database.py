'''
author: zhangquanwei
Date: 2025-03-07 22:32:24
'''
import glob
import importlib
import os

from tortoise import Tortoise

from core.logger import logger
from core.settings import data_root


async def init_db():
    try:
        # 使用正确的Tortoise初始化配置格式
        db_config = {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "host": "localhost",
                        "port": "5432",
                        "user": "postgres",
                        "password": "postgres",
                        "database": "postgres"
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["apps.base.models","system.user.models"],
                    "default_connection": "default",
                }
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai"
        }

        await Tortoise.init(config=db_config)

        # 创建migrations表
        await Tortoise.get_connection("default").execute_script("""
            CREATE TABLE IF NOT EXISTS migrates (
                id SERIAL PRIMARY KEY,
                migration_file VARCHAR(255) NOT NULL UNIQUE,
                executed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 执行迁移
        await execute_migrations()

    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise


async def execute_migrations():
    """执行数据库迁移"""
    try:
        # 收集迁移文件
        migration_files = []
        for root, dirs, files in os.walk("apps"):
            if "migrations" in dirs:
                migration_path = os.path.join(root, "migrations")
                migration_files.extend(glob.glob(os.path.join(migration_path, "migrations_*.py")))

        # 按文件名排序
        migration_files.sort()

        for migration_file in migration_files:
            file_name = os.path.basename(migration_file)

            # 检查是否已执行
            executed = await Tortoise.get_connection("default").execute_query(
                "SELECT id FROM migrates WHERE migration_file = $1", [file_name]
            )

            if not executed[1]:
                logger.info(f"执行迁移: {file_name}")
                # 导入并执行migration
                module_path = migration_file.replace("/", ".").replace("\\", ".").replace(".py", "")
                try:
                    migration_module = importlib.import_module(module_path)
                    if hasattr(migration_module, "migrate"):
                        await migration_module.migrate()
                        # 记录执行
                        await Tortoise.get_connection("default").execute_query(
                            "INSERT INTO migrates (migration_file) VALUES ($1)",
                            [file_name]
                        )
                        logger.info(f"迁移完成: {file_name}")
                except Exception as e:
                    logger.error(f"迁移 {file_name} 执行失败: {str(e)}")
                    raise

    except Exception as e:
        logger.error(f"迁移过程发生错误: {str(e)}")
        raise
