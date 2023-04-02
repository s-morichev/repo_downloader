### Тестовое задание

Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое
HEAD репозитория https://gitea.radium.group/radium/project-configuration во
временную папку. После выполнения всех асинхронных задач скрипт должен посчитать
sha256 хэши от каждого файла. Код должен проходить без замечаний проверку линтером
wemake-python-styleguide. Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration
Обязательно 100% покрытие тестами

### Описание решения

Простым решением было бы скачать архив репозитория или склонировать репозиторий,
например, с помощью gitpython. Однако по условиям нужно скачивание асинхронно
в три одновременные задачи. При клонировании не удается установить количество
задач. Для параллельной загрузки архива нужно заранее узнать размер архива,
чтобы разбить его на части, а хостинги не возвращают Content-Length при скачивании
архива. Можно было бы скачать архив в три части - первый байт, второй байт и все
остальное, но это формальный подход для соответствия условиям задания.

Поэтому выбрал сложный подход с парсингом html страниц. Алгоритм следующий:
1. Скачиваем html станицу, представляющую корневую папку репозитория
2. Парсим на ссылки, ведущие к файлам и подпапкам
3. Скачиваем файлы
4. Рекурсивно скачиваем файлы из подпапок


