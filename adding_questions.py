import argparse
import re

from settings_db import questions_redis


def formats_answer(answer, formatted_answer):
    """Форматирует ответ на вопрос:

    Удаляет пояснения,точки и запятые,перенос строк.
    Каждое слово приводит к нижнему регистру."""
    answer = re.split(r'[.\n\s",;!?]', answer)
    for string in answer:
        if not set(string) & {"[", "]", "(", ")"}:
            formatted_answer.append(string.lower())
    return " ".join(filter(lambda string: string != "", formatted_answer)).strip()


def get_new_questions(quiz_information, question_answer):
    """Возвращает словарь с новыми вопросами и ответами на них."""
    for index, text in enumerate(quiz_information):
        phrase = r"Вопрос (\d{0,5}):"
        check = re.match(phrase, text)
        if check:
            question = re.sub(phrase, "", text).replace("\n", "")
            answer = re.sub("Ответ:", "", quiz_information[index + 1])
            question_answer[question] = formats_answer(answer, [])
    return question_answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Добавляет новые вопросы и ответы на них для игры в викторину."
    )
    parser.add_argument("file_path", help="Путь до файла с данными.")
    args = parser.parse_args()

    with open(args.file_path, "r", encoding="KOI8-R") as file:
        quiz_information = file.read().split("\n\n")

    new_questions = get_new_questions(
        quiz_information=quiz_information, question_answer={}
    )

    quiz = questions_redis.hgetall("quiz") | new_questions

    questions_redis.hset("quiz", mapping=quiz)
