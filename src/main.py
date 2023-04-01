"""Скрипт для загрузки файлов из репозитория.

По условиям задачи необходимо асинхронно в три корутины загрузить файлы из
указанного репозитория и посчитать sha256 хеши файлов.
Из-за ограничений задачи каждый файл загружается по отдельности.
"""
import asyncio
import hashlib
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import aiofiles
from aiofiles.os import makedirs
from aiohttp import ClientResponseError, ClientSession

import parsers

MAX_CONCURRENT_TASKS = 3
REPO_URL = 'https://gitea.radium.group/radium/project-configuration'  # noqa: SC100
BRANCH_NAME = 'master'


def _validate_url(url: str) -> None:
    url = urlparse(url)
    if not url.scheme or not url.netloc or not url.path:
        sys.stdout.write(
            'URL must be in form http(s)://hostname/path/to/repo',
        )
        raise SystemExit(2)


async def _write_file(filepath: Path, filecontent: bytes) -> None:
    await makedirs(str(filepath.parent), exist_ok=True)
    async with aiofiles.open(str(filepath), mode='wb') as file_handler:
        await file_handler.write(filecontent)


def calculate_sha256(dir_path: Path) -> None:
    """
    Выводит в stdout sha256 хеши файлов в папке.

    :param dir_path: Путь до папки.
    """
    for pathname in dir_path.rglob('*'):
        if pathname.is_file():
            digest = hashlib.sha256()
            with pathname.open(mode='rb') as file_obj:
                digest.update(file_obj.read())
            line = '{0} {1}\n'.format(
                digest.hexdigest(),
                pathname.relative_to(dir_path),
            )
            sys.stdout.write(line)

    sys.stdout.flush()


class RepoDownloader(object):
    """Загрузчик файлов из репозитория."""

    def __init__(
        self: 'RepoDownloader',
        repo_url: str,
        root_dir: Path,
        parser: parsers.RepoHtmlPageParser,
    ) -> None:
        """
        Конструктор.

        :param repo_url:
        :param root_dir:
        :param parser:
        """
        self.repo_url = repo_url
        self.parser = parser
        self.semaphore = None
        self.root_dir = root_dir

    async def load_repo(self: 'RepoDownloader') -> None:
        """Загружает файлы из репозитория."""
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
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


async def main() -> None:
    """Execute script."""
    url = REPO_URL
    _validate_url(url)

    if 'github.com' in url:
        parser = parsers.GithubHtmlPageParser(url, branch=BRANCH_NAME)
    elif 'gitea' in url:
        parser = parsers.GiteaHtmlPageParser(url, branch=BRANCH_NAME)
    else:
        sys.stdout.write(
            'Only gitea and github hosting supported',
        )
        raise SystemExit(2)

    with tempfile.TemporaryDirectory() as dirname:
        temp_path = Path(dirname).resolve()

        loader = RepoDownloader(url, root_dir=temp_path, parser=parser)
        await loader.load_repo()

        calculate_sha256(temp_path)


if __name__ == '__main__':
    asyncio.run(main())
