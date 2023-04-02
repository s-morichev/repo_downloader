"""Скрипт для загрузки файлов из репозитория.

По условиям задачи необходимо асинхронно в три корутины загрузить файлы из
указанного репозитория и посчитать sha256 хеши файлов.
Из-за ограничений задачи каждый файл загружается по отдельности.
"""
import asyncio
import hashlib
import io
import sys
import tempfile
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import parsers
from downloader import RepoDownloader

MAX_CONCURRENT_TASKS = 3
REPO_URL = (
    'https://gitea.radium.group/radium/project-configuration'  # noqa: SC100
)
BRANCH_NAME = 'master'


def validate_url(url: str) -> None:
    """Проверяет наличие схемы, хоста и пути в URL."""
    url = urlparse(url)
    if not url.scheme or not url.netloc or not url.path:
        sys.stdout.write(
            'URL must be in form http(s)://hostname/path/to/repo',
        )
        raise SystemExit(2)


def calculate_sha256(
    dir_path: Path,
    stream: Optional[io.TextIOBase] = None,
) -> None:
    """
    Рассчитывает sha256 хеши файлов в папке.

    Результаты выводятся в stream.

    :param dir_path: Путь до папки.
    :param stream: Текстовый поток для записи результатов. Если None, то
        результаты выводятся в sys.stdout.
    """
    if stream is None:
        stream = sys.stdout

    for pathname in dir_path.rglob('*'):
        if pathname.is_file():
            digest = hashlib.sha256()
            with pathname.open(mode='rb') as file_obj:
                digest.update(file_obj.read())
            line = '{0} {1}\n'.format(
                digest.hexdigest(),
                pathname.relative_to(dir_path),
            )
            stream.write(line)

    stream.flush()


async def main() -> None:
    """Выполняем скрипт."""
    validate_url(REPO_URL)

    if 'github.com' in REPO_URL:
        parser = parsers.GithubHtmlPageParser(REPO_URL, branch=BRANCH_NAME)
    elif 'gitea' in REPO_URL:
        parser = parsers.GiteaHtmlPageParser(REPO_URL, branch=BRANCH_NAME)
    else:
        sys.stdout.write(
            'Only gitea and github hosting supported',
        )
        raise SystemExit(2)

    with tempfile.TemporaryDirectory() as dirname:
        temp_path = Path(dirname).resolve()
        loader = RepoDownloader(
            REPO_URL,
            root_dir=temp_path,
            parser=parser,
            max_tasks=MAX_CONCURRENT_TASKS,
        )
        await loader.load_repo()

        calculate_sha256(temp_path)


if __name__ == '__main__':
    asyncio.run(main())
