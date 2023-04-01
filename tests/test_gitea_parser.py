"""Tests for GiteaHtmlPageParser."""

from parsers import GiteaHtmlPageParser

REPO_URL = 'https://gitea.com/user/repo'
BRANCH = 'master'


def test_parse_root_page(gitea_root_page: str):
    parser = GiteaHtmlPageParser(REPO_URL, branch=BRANCH)
    links = parser.parse_links(gitea_root_page, '')
    answer = [
        (
            'https://gitea.com/user/repo/raw/branch/master/subfolder',
            'https://gitea.com/user/repo/src/branch/master/subfolder',
            'subfolder',
        ),
        (
            'https://gitea.com/user/repo/raw/branch/master/file.txt',
            'https://gitea.com/user/repo/src/branch/master/file.txt',
            'file.txt',
        ),
    ]
    assert links == answer


def test_parse_subfolder_page(gitea_subfolder_page: str):
    parser = GiteaHtmlPageParser(REPO_URL, branch=BRANCH)
    links = parser.parse_links(gitea_subfolder_page, 'subfolder')
    answer = [
        (
            'https://gitea.com/user/repo/raw/branch/master/subfolder/inner_subfolder',  # noqa: E501
            'https://gitea.com/user/repo/src/branch/master/subfolder/inner_subfolder',  # noqa: E501
            'subfolder/inner_subfolder',
        ),
        (
            'https://gitea.com/user/repo/raw/branch/master/subfolder/inner_file.txt',  # noqa: E501
            'https://gitea.com/user/repo/src/branch/master/subfolder/inner_file.txt',  # noqa: E501
            'subfolder/inner_file.txt',
        ),
    ]
    assert links == answer
