"""Pytest fixtures."""
import asyncio
from typing import Literal

import constants
import pytest

READ_MODE = 'r'
SESSION_SCOPE: Literal['session'] = 'session'


@pytest.fixture(scope=SESSION_SCOPE)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope=SESSION_SCOPE)
def github_root_page() -> str:
    with open(constants.GITHUB_ROOT_PAGE, mode=READ_MODE) as file_obj:
        return file_obj.read()


@pytest.fixture(scope=SESSION_SCOPE)
def github_subfolder_page() -> str:
    with open(constants.GITHUB_SUBFOLDER_PAGE, mode=READ_MODE) as file_obj:
        return file_obj.read()


@pytest.fixture(scope=SESSION_SCOPE)
def gitea_root_page() -> str:
    with open(constants.GITEA_ROOT_PAGE, mode=READ_MODE) as file_obj:
        return file_obj.read()


@pytest.fixture(scope='session')
def gitea_subfolder_page() -> str:
    with open(constants.GITEA_SUBFOLDER_PAGE, mode=READ_MODE) as file_obj:
        return file_obj.read()
