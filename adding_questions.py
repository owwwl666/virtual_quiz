import argparse
import re

import redis


def save_new_questions(quiz_information, question_answer):
    """Сохраняет в словарь новые вопросы и ответы на них."""
    for index, text in enumerate(quiz_information):
        phrase = r'Вопрос (\d{0,5}):'
        check = re.match(phrase, text)
        if check:
            question = re.sub(phrase, '', text).replace('\n', '')
            answer = re.sub('Ответ:', '', quiz_information[index + 1])
            question_answer[question] = answer
        return question_answer


if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

    parser = argparse.ArgumentParser(
        description="Добавляет новые вопросы и ответы на них для игры в викторину."
    )
    parser.add_argument("file_path", help="Путь до файла с данными.")
    args = parser.parse_args()

    with open(args.file_path, 'r', encoding='KOI8-R') as file:
        quiz_information = file.read().split('\n\n')

    new_questions = save_new_questions(
        quiz_information=quiz_information,
        question_answer={}
    )

    quiz = r.hgetall("quiz")
    r.hset("quiz", mapping=new_questions | quiz)
