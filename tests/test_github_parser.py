"""Tests for GithubHtmlPageParser."""

from parsers import GithubHtmlPageParser

REPO_URL = 'https://github.com/user/repo'
BRANCH = 'main'


def test_parse_root_page(github_root_page: str):
    parser = GithubHtmlPageParser(REPO_URL, branch=BRANCH)
    links = parser.parse_links(github_root_page, '')
    answer = [
        (
            'https://raw.githubusercontent.com/user/repo/main/subfolder',
            'https://github.com/user/repo/tree/main/subfolder',
            'subfolder',
        ),
        (
            'https://raw.githubusercontent.com/user/repo/main/file.txt',
            'https://github.com/user/repo/tree/main/file.txt',
            'file.txt',
        ),
    ]
    assert links == answer


def test_parse_subfolder_page(github_subfolder_page: str):
    parser = GithubHtmlPageParser(REPO_URL, branch=BRANCH)
    links = parser.parse_links(github_subfolder_page, 'subfolder')
    answer = [
        (
            'https://raw.githubusercontent.com/user/repo/main/subfolder/inner_subfolder',  # noqa: E501
            'https://github.com/user/repo/tree/main/subfolder/inner_subfolder',
            'subfolder/inner_subfolder',
        ),
        (
            'https://raw.githubusercontent.com/user/repo/main/subfolder/inner_file.txt',  # noqa: E501
            'https://github.com/user/repo/tree/main/subfolder/inner_file.txt',
            'subfolder/inner_file.txt',
        ),
    ]
    assert links == answer
