"""Константы для тестирования."""

GITHUB_ROOT_PAGE = './tests/test_html_pages/github_root_page.html'
GITHUB_SUBFOLDER_PAGE = './tests/test_html_pages/github_subfolder_page.html'
GITEA_ROOT_PAGE = './tests/test_html_pages/gitea_root_page.html'
GITEA_SUBFOLDER_PAGE = './tests/test_html_pages/gitea_subfolder_page.html'

GITEA_ROOT_PARSED_LINKS = (
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
)

GITEA_SUBFOLDER_PARSED_LINKS = (
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
)

GITHUB_ROOT_PARSED_LINKS = (
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
)

GITHUB_SUBFOLDER_PARSED_LINKS = (
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
)
