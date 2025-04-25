import datetime
import os
import csv
import string
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

# === Отримання типу запису від користувача ===
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

# === Клас для обробки файлів ===
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

# === Генерація статистики у CSV ===
def generate_statistics():
    file_path = "../news_feed.txt"
    if not os.path.exists(file_path):
        print("news_feed.txt not found.")
        return

    with open(file_path, 'r') as f:
        text = f.read()

    # === Word count ===
    words = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    word_counts = Counter(words)

    with open("word_count.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word", "count"])
        for word, count in word_counts.items():
            writer.writerow([word, count])

    # === Letter count ===
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
    process_file_input = input("Do you want to process a file? (y/n): ").strip().lower()
    if process_file_input == "y":
        file_path = input("Enter the path to the file (or press Enter to use the default): ").strip()
        file_processor = FileProcessor(file_path if file_path else None)
        file_processor.process_file()

    get_user_input()
    commit_to_git()
    generate_statistics()
    print("✔ Record added, committed to Git, and statistics CSVs generated.")
