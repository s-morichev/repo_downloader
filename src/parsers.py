"""Парсеры html страниц хостингов репозиториев."""
from abc import abstractmethod
from urllib.parse import urlparse

import bs4

HREF = 'href'
HOST_PATH_SUBPATH = '{0}{1}{2}'


class RepoHtmlPageParser(object):
    """Базовый класс для парсеров."""

    @abstractmethod
    def __init__(
        self: 'RepoHtmlPageParser',
        repo_url: str,
        branch: str,
    ) -> None:
        """Конструктор."""

    @abstractmethod
    def parse_links(
        self: 'RepoHtmlPageParser',
        html: str,
        current_folder: str,
    ) -> list[tuple[str, str, str]]:
        """
        Парсит ссылки на html странице для скачивания файлов.

        :param html: Содержимое страницы.
        :param current_folder: Папка, содержимое которой показывает страница.
        :return: Список кортежей из трех строк. Каждой ссылке на файл или
            подпапку соответствует один кортеж. Первая строка - ссылка на
            содержимое файла, вторая строка - ссылка на подпапку, третья строка
            - путь до подпапки. Поскольку по  ссылке не всегда можно
            определить, ведет ли она к файлу или подпапке, это должен решить
            вызывающий код.
        """


class GiteaHtmlPageParser(RepoHtmlPageParser):
    """Парсер html страниц репозитория на хостинге gitea."""

    def __init__(
        self: 'GiteaHtmlPageParser',
        repo_url: str,
        branch: str,
    ) -> None:
        """
        Конструктор.

        :param repo_url: URL репозитория.
        :param branch: Имя ветки.
        """
        url = urlparse(repo_url)
        self._host = '{scheme}://{host}'.format(
            scheme=url.scheme,
            host=url.netloc,
        )
        self._folder_http_path_to_branch = '{0}/src/branch/{1}/'.format(
            url.path,
            branch,
        )
        self._content_http_path_to_branch = '{0}/raw/branch/{1}/'.format(
            url.path,
            branch,
        )

    def parse_links(
        self: 'GiteaHtmlPageParser',
        html: str,
        current_folder: str,
    ) -> list[tuple[str, str, str]]:
        """
        Парсит ссылки на html странице для скачивания файлов.

        :param html: Содержимое страницы.
        :param current_folder: Папка, содержимое которой показывает страница.
        :return: Список кортежей из трех строк. Каждой ссылке на файл или
            подпапку соответствует один кортеж. Первая строка - ссылка на
            содержимое файла, вторая строка - ссылка на подпапку, третья строка
            - путь до подпапки. Поскольку по  ссылке не всегда можно
            определить, ведет ли она к файлу или подпапке, это должен решить
            вызывающий код.
        """
        prefix = self._folder_http_path_to_branch + current_folder
        soup = bs4.BeautifulSoup(html, features='html.parser')
        links = []
        for link in soup.find_all('a'):
            if link.has_attr(HREF) and link[HREF].startswith(prefix):
                link_path = link[HREF]
                links.append(self._assemble_links(link_path))

        return links

    def _assemble_links(
        self: 'GiteaHtmlPageParser',
        link_http_path: str,
    ) -> tuple[str, str, str]:
        subpath = link_http_path.replace(self._folder_http_path_to_branch, '')
        file_link = HOST_PATH_SUBPATH.format(
            self._host,
            self._content_http_path_to_branch,
            subpath,
        )
        folder_link = HOST_PATH_SUBPATH.format(
            self._host,
            self._folder_http_path_to_branch,
            subpath,
        )
        return file_link, folder_link, subpath


class GithubHtmlPageParser(RepoHtmlPageParser):
    """Парсер html страниц репозитория на хостинге github."""

    def __init__(
        self: 'GithubHtmlPageParser',
        repo_url: str,
        branch: str,
    ) -> None:
        """Create class instance."""
        url = urlparse(repo_url)
        self._host = '{0}://{1}'.format(url.scheme, url.netloc)
        self._raw_content_host = 'https://raw.githubusercontent.com'
        self._folder_http_path_to_branch = '{0}/tree/{1}/'.format(
            url.path,
            branch,
        )
        self._content_http_path_to_branch = '{0}/{1}/'.format(url.path, branch)

    def parse_links(
        self: 'GithubHtmlPageParser',
        html: str,
        current_folder: str,
    ) -> list[tuple[str, str, str]]:
        """
        Парсит ссылки на html странице для скачивания файлов.

        :param html: Содержимое страницы.
        :param current_folder: Папка, содержимое которой показывает страница.
        :return: Список кортежей из трех строк. Каждой ссылке на файл или
            подпапку соответствует один кортеж. Первая строка - ссылка на
            содержимое файла, вторая строка - ссылка на подпапку, третья строка
            - путь до подпапки. Поскольку по  ссылке не всегда можно
            определить, ведет ли она к файлу или подпапке, это должен решить
            вызывающий код.
        """
        prefix = self._content_http_path_to_branch + current_folder
        soup = bs4.BeautifulSoup(html, features='html.parser')
        links = []
        for link in soup.find_all('a'):
            if link.has_attr(HREF):
                link_path = (
                    link[HREF].replace('blob/', '', 1).replace('tree/', '', 1)
                )
                if link_path.startswith(prefix):
                    links.append(self._assemble_links(link_path))

        return links

    def _assemble_links(
        self: 'GithubHtmlPageParser',
        link_http_path: str,
    ) -> tuple[str, str, str]:
        subpath = link_http_path.replace(self._content_http_path_to_branch, '')
        file_link = HOST_PATH_SUBPATH.format(
            self._raw_content_host,
            self._content_http_path_to_branch,
            subpath,
        )
        folder_link = HOST_PATH_SUBPATH.format(
            self._host,
            self._folder_http_path_to_branch,
            subpath,
        )
        return file_link, folder_link, subpath
