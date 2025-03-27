import random
import json
import os
from datetime import datetime


DATA_FILE = "performance_data.json"


flashcards = [
    {
        "question": "who is in paris?",
        "answer": "Kanye and JayZ",
        "choices": ["Cod word", "homies", "neighbors"]
    },
    {
        "question": "9 + 10 =",
        "answer": "21",
        "choices": ["19", "20", "22"]
    },
    {
        "question": "aint no party like a 'blank' party",
        "answer": "diddy",
        "choices": ["pizza", "birthday", "tea"]
    },
    {
        "question": "is luigi mangione innocent?",
        "answer": "no",
        "choices": ["yes", "maybe", "idk"]
    },
    {"question": "what is massive",
     "answer": "low taper fade meme",
     "choices":["the world","ur mom","universe"]

    }
]

def load_data():
    with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"history": []}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

def show_summary(data):
    print("Previous Session Summary:")
    if data["history"]:
        last = data["history"][-1]
        print(f"Date: {last['timestamp']}")
        print(f"Score: {last['score']}/{last['total']}")
        print(f"Accuracy: {last['accuracy']}%")
    else:
        print("No previous data found.")

    print("\nOverall Performance Summary:")
    if data["history"]:
        scores = [h["score"] for h in data["history"]]
        totals = [h["total"] for h in data["history"]]
        avg = round(sum(scores) / len(scores), 2)
        print(f"Total Sessions: {len(data['history'])}")
        print(f"Average Score: {avg}/{totals[0]}")
    else:
        print("No performance data yet.")

def adapt_flashcards(data):
    wrong_counts = {}
    for history in data["history"]:
        for missed in history.get("wrong", []):
            wrong_counts[missed] = wrong_counts.get(missed, 0) + 1
            if wrong_counts[missed] > 10:
                print("y u dumb also KeepYourselfSafe")

    def card_sort(card):
        return -wrong_counts.get(card["question"], 0) + random.random()

    return sorted(flashcards, key=card_sort)

def run_quiz():
    data = load_data()
    show_summary(data)

    questions = adapt_flashcards(data)
    random.shuffle(questions)

    score = 0
    wrong = []
    total = min(20, len(questions))  

    print("Starting Multiple Choice Quiz:")

    for i, card in enumerate(questions[:total], 1):
        correct_answer = card['answer']
        custom_wrong_choices = card.get("choices", [])
        choices = custom_wrong_choices + [correct_answer]
        random.shuffle(choices)

        option_labels = ['A', 'B', 'C', 'D']
        option_map = dict(zip(option_labels, choices))

        print(f"Q{i}: {card['question']}")
        for label in option_labels:
            print(f"  {label}) {option_map[label]}")

        while True:
            user_choice = input("Your answer (A/B/C/D): ").upper()
            if user_choice in option_map:
                break
            print("Invalid input. Please enter A, B, C, or D.")

        if option_map[user_choice].lower() == correct_answer.lower():
            print("Correct!")
            score += 1
        else:
            print(f" Y u dumb? Also, KeepYourselfSafe: {correct_answer}\n")
            wrong.append(card["question"])

    accuracy = round((score / total) * 100, 2)

    print("Quiz Finished!")
    print(f"Score: {score}/{total}")
    print(f"Accuracy: {accuracy}%")

    data["history"].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "total": total,
        "accuracy": accuracy,
        "wrong": wrong
    })

    save_data(data)


run_quiz()
