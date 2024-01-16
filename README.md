# Описание

Реализация игры "Викторина" с помощью ботов на двух платформах - ВК и телеграм. Интерфейс ботов очень прост: при запуске бота, выскакивает меню, состоящее из 3 кнопок - "Новый вопрос", "Сдаться", "Мой счёт".

Ознакомиться и поиграть можно, перейдя по следующим ссылкам:

- [ВК](https://vk.com/club224264443)
- [Телеграм](https://t.me/very_good_quiz_bot)

# Запуск проекта локально

## Установка зависимостей

Создайте виртуальное окружение и установите необходимые пакеты для работы скриптов, выполнив следующую команду:

```sh
pip install -r requirements.txt
```

## Установка Redis

Для того, чтобы установить redis на необходимую операционную систему, ознакомьтесь с инструкцией:

[Установка и настройка Redis для разных ОС](https://timeweb.cloud/tutorials/redis/ustanovka-i-nastrojka-redis-dlya-raznyh-os)

## Переменные окружения

Создайте файл `.env` и поместите в него переменные окружения.

**Обязательные переменные окружения**:

```
TELEGRAM_BOT_TOKEN - <токен телеграм бота для викторины>
LOGGER_BOT_TOKEN - <токен телеграм бота для логирования ошибок>
CHAT_ID - <ваш chat_id из телеграм>
VK_BOT_TOKEN - <токен VK бота для викторины>
```

Необязательные(с дефолтными значениями) переменные окружения:

```
HOST - <ip сервера, на котором хранятся БД с данными>
PORT - <порт для соединения с БД>
QUESTIONS_DB - <БД с вопросами для викторины>
QUESTIONS_DB_PASSWORD - <пароль от БД с вопросами>
USERS_DB - <БД с пользователями>
USERS_DB_PASSWORD - <пароль от БД с пользователями>
POINTS_DB - <БД с количеством очков для каждого пользователя>
POINTS_DB_PASSWORD - <пароль от БД с баллами>
```

## adding_questions.py

Скрипт для редактирования файла с вопросами и ответами для Викторины. Открывает переданный файл с данными о Викторине, редактирует их под необходимый формат и сохраняет в БД `questions_redis` в виде словаря `{'вопрос':'ответ'}` либо добавляет новые вопросы к уже имеющимся.

Для того, чтобы добавить новые вопросы, необходимо запустить скрипт и передать ему в виде аргумента путь к файлу с вопросами:

```sh
python adding_questions.py $PATH
```

[Архив](https://dvmn.org/media/modules_dist/quiz-questions.zip) с вопросами.


## tg_bot.py

Телеграм бот для игры в викторину. Для запуска бота необходимо выбрать из меню (или ввести вручную) команду `/start`. Для выхода из игры - команду `/cancel`.

Запуск бота:

```sh
python tg_bot.py
```

## vk_bot.py

ВК бот для игры в викторину. Для начала нововй игры введите команду `Начать`.

Запуск бота:

```sh
python vk_bot.py
```


# Результаты

Пример результата для Telegram:

![image](https://github.com/owwwl666/virtual_quiz/assets/131767856/0be19f8f-14c4-4b74-9683-61942af671dd)

Пример результата для Вконтакте:

![image](https://github.com/owwwl666/virtual_quiz/assets/131767856/243883f2-f7fd-403e-82b5-a6c5439db731)
