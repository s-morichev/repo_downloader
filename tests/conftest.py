"""Pytest fixtures."""
from typing import Literal

import pytest

READ_MODE = 'r'

GITHUB_ROOT_PAGE = './tests/test_html_pages/github_root_page.html'
GITHUB_SUBFOLDER_PAGE = './tests/test_html_pages/github_subfolder_page.html'
GITEA_ROOT_PAGE = './tests/test_html_pages/gitea_root_page.html'
GITEA_SUBFOLDER_PAGE = './tests/test_html_pages/gitea_subfolder_page.html'

SESSION_SCOPE: Literal['session'] = 'session'


@pytest.fixture(scope=SESSION_SCOPE)
def github_root_page() -> str:
    with open(GITHUB_ROOT_PAGE, mode=READ_MODE) as file_obj:
        return file_obj.read()


@pytest.fixture(scope=SESSION_SCOPE)
def github_subfolder_page() -> str:
    with open(GITHUB_SUBFOLDER_PAGE, mode=READ_MODE) as file_obj:
        return file_obj.read()


@pytest.fixture(scope=SESSION_SCOPE)
def gitea_root_page() -> str:
    with open(GITEA_ROOT_PAGE, mode=READ_MODE) as file_obj:
        return file_obj.read()


@pytest.fixture(scope='session')
def gitea_subfolder_page() -> str:
    with open(GITEA_SUBFOLDER_PAGE, mode=READ_MODE) as file_obj:
        return file_obj.read()
