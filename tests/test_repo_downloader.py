"""Tests for RepoDownloader."""
from pathlib import Path
from unittest.mock import DEFAULT, MagicMock, patch

import constants
import pytest
from aiohttp import ClientResponseError, ClientSession

from downloader import RepoDownloader

REPO_URL = 'https://gitea.com/user/repo'


class MockGiteaParser(object):
    """Мок парсера."""

    def parse_links(self: 'MockGiteaParser', html: str, subfolder: str):
        """Возвращает заданный набор ссылок."""
        if subfolder == '':
            return constants.GITEA_ROOT_PARSED_LINKS
        elif subfolder == 'subfolder':
            return constants.GITEA_SUBFOLDER_PARSED_LINKS
        elif subfolder == 'subfolder/inner_subfolder':
            return ()

        raise ValueError(
            'Mocking folder {0} not supported'.format(subfolder),
        )


@pytest.fixture(scope='module')
def gitea_loader():
    parser = MockGiteaParser()
    temp_path = Path('./temp')
    return RepoDownloader(REPO_URL, root_dir=temp_path, parser=parser)


@pytest.mark.asyncio()
async def test_get_html(gitea_loader: RepoDownloader):
    mock = ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.text.return_value = (
        'test content'
    )

    async with ClientSession() as session:
        html_content = await gitea_loader._get_html('url', session)

    assert html_content == 'test content'


@pytest.mark.asyncio()
async def test_download_file(gitea_loader):
    mock = ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.read.return_value = (
        b'test content'
    )

    with patch('downloader._write_file') as mock_write:
        async with ClientSession() as session:
            await gitea_loader._download_file('url', 'test.txt', session)

        mock_write.assert_called_with(
            gitea_loader.root_dir / 'test.txt',
            b'test content',
        )


@pytest.mark.asyncio()
async def test_load_root_folder(gitea_loader):
    def raise_if_not_txt(url: str, *args, **kwargs):
        if url.endswith('.txt'):
            return DEFAULT
        raise ClientResponseError(None, (None,))

    with patch.object(gitea_loader, '_get_html') as mock_get_html:
        with patch.object(
            gitea_loader,
            '_download_file',
            side_effect=raise_if_not_txt,
        ) as mock_download:
            async with ClientSession() as session:
                await gitea_loader._load_folder('url', '', session)

            assert mock_get_html.call_count == 3
            assert mock_download.call_count == 4
