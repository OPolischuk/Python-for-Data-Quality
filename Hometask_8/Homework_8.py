import datetime
import os
import csv
import string
import json
from collections import Counter

# === Функція для запису в файл ===
def write_to_file(record):
    file_path = "../news_feed.txt"
    with open(file_path, 'a') as f:
        f.write(record + "\n")

# === Функції обробки записів ===
def handle_news():
    city = input("Enter the city for the news: ")
    text = input("Enter the news text: ")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    record = f"NEWS|{current_date}|{city}|{text}"
    write_to_file(record)

def handle_private_ad():
    text = input("Enter the ad text: ")
    expiration_date = input("Enter the expiration date (YYYY-MM-DD): ")
    expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
    today = datetime.datetime.now()
    days_left = (expiration_date - today).days
    record = f"PRIVATE_AD|{text}|{expiration_date.strftime('%Y-%m-%d')}|{days_left} days left"
    write_to_file(record)

def handle_custom_record():
    title = input("Enter the custom record title: ")
    description = input("Enter the custom record description: ")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    record = f"CUSTOM|{current_date}|{title}|{description}"
    write_to_file(record)

# === Обробка вводу вручну ===
def get_user_input():
    print("Select the type of record you want to add:")
    print("1. News")
    print("2. Private Ad")
    print("3. Custom Record")
    record_type = input("Enter your choice (1/2/3): ")
    if record_type == "1":
        handle_news()
    elif record_type == "2":
        handle_private_ad()
    elif record_type == "3":
        handle_custom_record()
    else:
        print("Invalid choice. Please try again.")
        get_user_input()

# === Коміт у Git ===
def commit_to_git():
    os.system("git add ../news_feed.txt")
    os.system('git commit -m "Added new record to news_feed"')

# === Клас для обробки текстового файлу ===
class FileProcessor:
    def __init__(self, file_path=None):
        self.file_path = file_path or "default_folder/records.txt"
        self.normalized_records = []

    def normalize_case(self, text):
        return text.lower()

    def process_file(self):
        if not os.path.exists(self.file_path):
            print(f"The file {self.file_path} does not exist.")
            return
        with open(self.file_path, 'r') as file:
            records = file.readlines()
            for record in records:
                normalized_record = self.normalize_case(record.strip())
                self.normalized_records.append(normalized_record)
                write_to_file(normalized_record)
                print(f"Processed record: {normalized_record}")
        self.remove_file()

    def remove_file(self):
        try:
            os.remove(self.file_path)
            print(f"File {self.file_path} has been successfully processed and removed.")
        except Exception as e:
            print(f"Error removing file {self.file_path}: {e}")

# === Клас для обробки JSON ===
class JSONProcessor:
    def __init__(self, json_path=None):
        self.json_path = json_path or "default_folder/records.json"

    def process_json(self):
        if not os.path.exists(self.json_path):
            print(f"The file {self.json_path} does not exist.")
            return

        try:
            with open(self.json_path, 'r') as file:
                data = json.load(file)

            for item in data:
                self.process_record(item)

            self.remove_file()

        except Exception as e:
            print(f"Failed to process JSON file: {e}")

    def process_record(self, item):
        record_type = item.get("type", "").lower()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        if record_type == "news":
            city = item.get("city", "Unknown")
            text = item.get("text", "")
            record = f"NEWS|{current_date}|{city}|{text}"

        elif record_type == "private ad":
            text = item.get("text", "")
            exp_date_str = item.get("expiration_date", "")
            try:
                expiration_date = datetime.datetime.strptime(exp_date_str, "%Y-%m-%d")
                days_left = (expiration_date - datetime.datetime.now()).days
                record = f"PRIVATE_AD|{text}|{expiration_date.strftime('%Y-%m-%d')}|{days_left} days left"
            except ValueError:
                print(f"Invalid date format for ad: {exp_date_str}")
                return

        elif record_type == "custom":
            title = item.get("title", "")
            description = item.get("description", "")
            record = f"CUSTOM|{current_date}|{title}|{description}"

        else:
            print(f"Unknown record type: {record_type}")
            return

        write_to_file(record)
        print(f"Processed JSON record: {record}")

    def remove_file(self):
        try:
            os.remove(self.json_path)
            print(f"JSON file {self.json_path} processed and removed.")
        except Exception as e:
            print(f"Error removing JSON file {self.json_path}: {e}")

# === Генерація статистики у CSV ===
def generate_statistics():
    file_path = "../news_feed.txt"
    if not os.path.exists(file_path):
        print("news_feed.txt not found.")
        return

    with open(file_path, 'r') as f:
        text = f.read()

    words = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    word_counts = Counter(words)

    with open("word_count.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word", "count"])
        for word, count in word_counts.items():
            writer.writerow([word, count])

    all_letters = [char for char in text if char.isalpha()]
    letter_counts = Counter(char.lower() for char in all_letters)
    upper_counts = Counter(char for char in text if char.isupper())

    with open("letter_count.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["letter", "count_all", "count_uppercase", "percentage"])
        for letter in sorted(letter_counts):
            count_all = letter_counts[letter]
            count_upper = upper_counts.get(letter.upper(), 0)
            percentage = round((count_upper / count_all) * 100, 2) if count_all else 0
            writer.writerow([letter, count_all, count_upper, f"{percentage}%"])

# === Основна частина ===
if __name__ == "__main__":
    # Текстовий файл
    process_file_input = input("Do you want to process a plain text file? (y/n): ").strip().lower()
    if process_file_input == "y":
        file_path = input("Enter the path to the file (or press Enter to use the default): ").strip()
        file_processor = FileProcessor(file_path if file_path else None)
        file_processor.process_file()

    # JSON файл
    process_json_input = input("Do you want to process a JSON file? (y/n): ").strip().lower()
    if process_json_input == "y":
        json_path = input("Enter the path to the JSON file (or press Enter to use the default): ").strip()
        json_processor = JSONProcessor(json_path if json_path else None)
        json_processor.process_json()

    # Вручну
    get_user_input()
    commit_to_git()
    generate_statistics()
    print("✔ All records processed, committed to Git, and statistics CSVs generated.")
