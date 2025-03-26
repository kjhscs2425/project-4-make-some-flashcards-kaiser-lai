import random
import json
import os
from datetime import datetime

# 🔧 Set the filename to store performance data
DATA_FILE = "performance_data.json"

# 📋 Flashcards: Add more if you want!
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "2 + 2 =", "answer": "4"},
    {"question": "What planet is known as the Red Planet?", "answer": "Mars"},
    {"question": "Boiling point of water in Celsius?", "answer": "100"},
    {"question": "Who wrote Hamlet?", "answer": "Shakespeare"},
    {"question": "Square root of 64?", "answer": "8"},
    {"question": "Chemical formula for water?", "answer": "H2O"},
    {"question": "Capital of Japan?", "answer": "Tokyo"},
    {"question": "How many continents?", "answer": "7"},
    {"question": "Gas plants breathe in?", "answer": "Carbon dioxide"},
    {"question": "What is 10 x 10?", "answer": "100"},
    {"question": "US currency?", "answer": "Dollar"},
    {"question": "Hardest natural substance?", "answer": "Diamond"},
    {"question": "Opposite of 'hot'?", "answer": "Cold"},
    {"question": "Who painted Mona Lisa?", "answer": "Leonardo da Vinci"},
    {"question": "Shape with 3 sides?", "answer": "Triangle"},
    {"question": "Largest ocean?", "answer": "Pacific"},
    {"question": "What do bees make?", "answer": "Honey"},
    {"question": "What is 9 + 10?", "answer": "19"},
    {"question": "How many legs does a spider have?", "answer": "8"},
    {"question": "Name of our galaxy?", "answer": "Milky Way"},
    {"question": "What is 15 ÷ 3?", "answer": "5"}
]


def load_data():
    if os.path.exists(DATA_FILE):
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

    print("Overall Performance Summary:")
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
            if wrong_counts > 10:
                print("y u dumb")

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
    total = 20

    print("Starting Quiz:")
    for i, card in enumerate(questions[:total], 1):
        print(f"Q{i}: {card['question']}")
        answer = input("Your answer: ").strip()
        if answer.lower() == card['answer'].lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong, The correct answer is: {card['answer']}\n")
            wrong.append(card['question'])

    accuracy = round((score / total) * 100, 2)

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
