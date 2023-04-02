"""Загрузчик файлов из репозитория."""
import asyncio
from pathlib import Path

import aiofiles
from aiofiles.os import makedirs
from aiohttp import ClientResponseError, ClientSession

import parsers


async def _write_file(filepath: Path, filecontent: bytes) -> None:
    await makedirs(str(filepath.parent), exist_ok=True)
    async with aiofiles.open(str(filepath), mode='wb') as file_handler:
        await file_handler.write(filecontent)


class RepoDownloader(object):
    """Загрузчик файлов из репозитория."""

    def __init__(
        self: 'RepoDownloader',
        repo_url: str,
        root_dir: Path,
        parser: parsers.RepoHtmlPageParser,
        max_tasks: int = 3,
    ) -> None:
        """
        Конструктор.

        :param repo_url:
        :param root_dir:
        :param parser:
        """
        self.repo_url = repo_url
        self.parser = parser
        self.semaphore = asyncio.Semaphore(max_tasks)
        self.root_dir = root_dir

    async def load_repo(self: 'RepoDownloader') -> None:
        """Загружает файлы из репозитория."""
        async with ClientSession(raise_for_status=True) as session:
            await self._load_folder(self.repo_url, '', session)

    async def _load_folder(
        self: 'RepoDownloader',
        folder_url: str,
        folder_path: str,
        session: ClientSession,
    ) -> None:
        try:
            html = await self._get_html(folder_url, session)
        except ClientResponseError:
            return

        links = self.parser.parse_links(html, folder_path)
        for file_url, subfolder_url, subpath in links:
            try:
                await self._download_file(file_url, subpath, session)
            except ClientResponseError:
                await self._load_folder(subfolder_url, subpath, session)

    async def _get_html(
        self: 'RepoDownloader',
        url: str,
        session: ClientSession,
    ) -> str:
        async with self.semaphore:
            async with session.get(url) as response:
                return await response.text()

    async def _download_file(
        self: 'RepoDownloader',
        file_url: str,
        path_to_save: str,
        session: ClientSession,
    ) -> None:
        async with self.semaphore:
            async with session.get(file_url) as response:
                file_content = await response.read()

        filepath = self.root_dir / path_to_save
        await _write_file(filepath, file_content)
