import argparse
import re

question_answer = dict()

parser = argparse.ArgumentParser(
    description="Добаляет новые вопросы и ответы на них для игры в викторину."
)
parser.add_argument("file_path", help="Путь до файла с данными.")
args = parser.parse_args()

with open(args.file_path, 'r', encoding='KOI8-R') as file:
    split_file = file.read().split('\n\n')

for index, text in enumerate(split_file):
    phrase = r'Вопрос (\d{0,5}):'
    check = re.match(phrase, text)
    if check:
        question = re.sub(phrase, '', text)
        answer = re.sub('Ответ:', '', split_file[index + 1])
        question_answer[question] = answer