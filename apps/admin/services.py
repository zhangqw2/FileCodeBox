import os
import time
import pwd  # 添加此行
from typing import Tuple, List
import glob
from core.response import APIResponse
from core.storage import FileStorageInterface, storages
from core.settings import settings
from apps.base.models import FileCodes, KeyValue
from apps.base.utils import get_expire_info, get_file_path_name
from fastapi import HTTPException
from core.settings import data_root
from pathlib import Path

class FileService:
    def __init__(self):
        self.file_storage: FileStorageInterface = storages[settings.file_storage]()

    async def delete_file(self, file_id: int):
        file_code = await FileCodes.get(id=file_id)
        await self.file_storage.delete_file(file_code)
        await file_code.delete()

    async def list_files(self, page: int, size: int, keyword: str = ""):
        offset = (page - 1) * size
        files = (
            await FileCodes.filter(prefix__icontains=keyword).limit(size).offset(offset)
        )
        total = await FileCodes.filter(prefix__icontains=keyword).count()
        return files, total

    async def download_file(self, file_id: int):
        file_code = await FileCodes.filter(id=file_id).first()
        if not file_code:
            raise HTTPException(status_code=404, detail="文件不存在")
        if file_code.text:
            return APIResponse(detail=file_code.text)
        else:
            return await self.file_storage.get_file_response(file_code)

    async def share_local_file(self, item):
        local_file = LocalFileClass(item.filename)
        if not await local_file.exists():
            raise HTTPException(status_code=404, detail="文件不存在")

        text = await local_file.read()
        expired_at, expired_count, used_count, code = await get_expire_info(
            item.expire_value, item.expire_style
        )
        path, suffix, prefix, uuid_file_name, save_path = await get_file_path_name(item)

        await self.file_storage.save_file(text, save_path)

        await FileCodes.create(
            code=code,
            prefix=prefix,
            suffix=suffix,
            uuid_file_name=uuid_file_name,
            file_path=path,
            size=local_file.size,
            expired_at=expired_at,
            expired_count=expired_count,
            used_count=used_count,
        )

        return {
            "code": code,
            "name": local_file.file,
        }

    async def share_local_to_share_file(self, item):
        local_file = LocalFileClass(item.filename)
        if not await local_file.exists():
            raise HTTPException(status_code=404, detail="文件不存在")

        text = await local_file.read()
        expired_at, expired_count, used_count, code = await get_expire_info(
            item.expire_value, item.expire_style
        )
        path, suffix, prefix, uuid_file_name, save_path = await get_file_path_name(item)
        # 覆盖原始文件名
        save_path = f"{path}/{item.fileName}"
        await self.file_storage.save_local_to_share_file(text, save_path)

        await FileCodes.create(
            code=code,
            prefix=prefix,
            suffix=suffix,
            uuid_file_name=item.fileName,
            file_path=path,
            size=local_file.size,
            expired_at=expired_at,
            expired_count=expired_count,
            used_count=used_count,
        )

        return {
            "code": code,
            "name": local_file.file,
        }
class ConfigService:
    def get_config(self):
        return settings.items()

    async def update_config(self, data: dict):
        admin_token = data.get("admin_token")
        if admin_token is None or admin_token == "":
            raise HTTPException(status_code=400, detail="管理员密码不能为空")

        for key, value in data.items():
            if key not in settings.default_config:
                continue
            if key in [
                "errorCount",
                "errorMinute",
                "max_save_seconds",
                "onedrive_proxy",
                "openUpload",
                "port",
                "s3_proxy",
                "uploadCount",
                "uploadMinute",
                "uploadSize",
            ]:
                data[key] = int(value)
            elif key in ["opacity"]:
                data[key] = float(value)
            else:
                data[key] = value

        await KeyValue.filter(key="settings").update(value=data)
        for k, v in data.items():
            settings.__setattr__(k, v)


class LocalFileService:
    async def find_files_by_name(
            self,
            filename: str,
            page: int = 1,
            size: int = 10
    ) -> Tuple[List, int]:
        base_path = Path(settings.local_path)
        # 处理扩展名（移除点号并转小写）
        allowed_extensions = {
            ext.lower().lstrip('.')
            for ext in settings.local_file_format.split(",")
        }
        base_path.mkdir(parents=True, exist_ok=True)

        matched_files = []
        # 构造跨平台兼容的路径模式
        pattern = str(base_path / "**" / filename)

        for full_path in glob.iglob(pattern, recursive=True):
            # 提取文件扩展名（移除点号并转小写）
            _, ext = os.path.splitext(full_path)
            file_ext = ext.lstrip('.').lower()
            if file_ext not in allowed_extensions:
                continue

            # 精确匹配文件名（不包含路径）
            file_name = os.path.basename(full_path)
            if file_name != filename:
                continue

            relative_path = os.path.relpath(full_path, base_path)
            matched_files.append(LocalFileClass(relative_path))

        total = len(matched_files)
        start = (page - 1) * size
        end = start + size
        return matched_files[start:end], total

    async def list_files(self, page: int = 1, size: int = 6,keyword: str = ""):
        base_path = Path(settings.local_path)
        allowed_extensions = tuple(settings.local_file_format.split(","))
        base_path.mkdir(parents=True, exist_ok=True)

        all_files = []
        for root, _, filenames in os.walk(base_path):
            for f in filenames:
                if not f.endswith(allowed_extensions):  # 保留扩展名过滤
                    continue
                file_path = os.path.relpath(os.path.join(root, f), base_path)

                # 新增关键字过滤逻辑
                if keyword and keyword.lower() not in file_path.lower():
                    continue

                all_files.append(LocalFileClass(file_path))

        total = len(all_files)
        start = (page - 1) * size
        end = start + size
        paginated_files = all_files[start:end]

        return paginated_files, total

    async def delete_file(self, filename: str):
        file = LocalFileClass(filename)
        if await file.exists():
            await file.delete()
            return "删除成功"
        raise HTTPException(status_code=404, detail="文件不存在")


class LocalFileClass:
    def __init__(self, file):
        self.file = file
        self.path = Path(settings.local_path)  / file
        self.ctime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(self.path))
        )
        self.fileName = os.path.basename(Path(settings.local_path)  / file)
        self.size = os.path.getsize(self.path)
        self.owner = self.get_owner()  # 添加此行

    def get_owner(self):
        return "默认用户"  # 添加此行

    async def read(self):
        return open(self.path, "rb")

    async def write(self, data):
        with open(self.path, "w") as f:
            f.write(data)

    async def delete(self):
        os.remove(self.path)

    async def exists(self):
        return os.path.exists(self.path)
