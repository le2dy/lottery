import os
import requests
import json

questions_list = {}
answer_list = []
questions = []
answers = []
inputs = []
question_count = 0
from_day = 0
to_day = 0
question_type = 0
test_type = 0
timer = 0
start_time = 0
idx = 0


def set_count():
    os.system('clear')
    global question_count
    global from_day
    global to_day
    global question_type

    try:
        print("출제 범위 입력")
        from_day = int(input("시작 날짜(1~30): "))
        if from_day not in range(1, 31):
            print("날짜는 범위 내로 입력해주세요.")
            set_count()
        to_day = int(input("끝 날짜(1~30): "))
        if to_day not in range(1, 31):
            print("날짜는 범위 내로 입력해주세요.")
            set_count()
        print("문제 유형")
        print("1. 뜻 맞히기")
        print("2. 빈출 영단어 맞히기")
        print("3. 뜻 + 빈출 영단어 맞히기")
        question_type = int(input("입력: "))
        if question_type not in range(1, 4):
            print("유형은 범위 내로 입력해주세요.")
            set_count()
            return
        if question_type == 3:
            question_type = "1,02"
        question_count = int(input("문제 개수 입력(1~100): "))
        if question_count not in range(1, 101):
            print("문제 개수는 범위 내로 입력해주세요.")
            set_count()
            return
    except ValueError:
        print("숫자로 입력해주세요.")
        set_count()


def load_questions():
    global questions
    global answers

    while len(questions_list) < question_count:
        url_get_guid = 'https://toeic.eduwill.net/api/voca/create/_115F22VCB11'

        headers = {"Content-Type": "application/json"}
        params = {"fromDay": from_day, "toDay": to_day, "vocaTypeList": "01,02,03",
                  "quesTypeList": "0" + str(question_type),
                  "quesCnt": "35"}
        # 1~35

        res = requests.post(url_get_guid, headers=headers, data=json.dumps(params)).json()

        guid = res['Guid']

        url_get_questions = 'https://toeic.eduwill.net/api/voca/_115F22VCB11/' + guid

        res = requests.get(url_get_questions, headers=headers).json()

        for i in res['QuestionList']:
            answer_list.append([])
            for j in i["AnswerList"]:
                answer_list[len(answer_list) - 1].append(j["ANSWER"])

            if i['QUESTION'] in questions_list.keys():
                questions_list[i['QUESTION']] += ", " + i['ANSWER']
            else:
                questions_list[i['QUESTION']] = i['ANSWER']

            if len(questions_list) == question_count:
                break

        questions = list(questions_list.keys())
        answers = list(questions_list.values())
    start_test()


# 30 문제 = 3 분  30 = 180 1 : 6
def start_test():
    print_questions()


def print_questions():
    global idx
    os.system('clear')

    print(questions[idx])
    for i in range(len(answer_list[idx])):
        print(str(i + 1) + ". " + answer_list[idx][i], end=' ')
    print()
    inputs.append(input("Answer: "))

    idx += 1
    if idx != len(questions):
        print_questions()
    else:
        result()


def result():
    os.system('clear')

    for i in range(len(answers)):
        if answers[i].__eq__(answer_list[i][int(inputs[i]) - 1]):
            a = '\033[94m' + inputs[i] + '\033[0m'
        else:
            a = '\033[91m' + inputs[i] + '\033[0m'
        print(str(i + 1) + '. ', questions[i], answers[i], a)


if __name__ == '__main__':
    set_count()
    load_questions()
