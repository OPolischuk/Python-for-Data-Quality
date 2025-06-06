import datetime
import os
import csv
import string
import json
import xml.etree.ElementTree as ET
from collections import Counter

# === Функція для запису в файл ===
def write_to_file(record):
    file_path = "../news_feed.txt"
    with open(file_path, 'a') as f:
        f.write(record + "\n")

# === Функції обробки записів вручну ===
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

# === Меню для ручного вводу ===
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

# === Клас для обробки текстових файлів ===
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

# === Клас для обробки JSON файлів ===
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

# === Клас для обробки XML файлів ===
class XMLProcessor:
    def __init__(self, xml_path=None):
        self.xml_path = xml_path or "default_folder/records.xml"

    def process_xml(self):
        if not os.path.exists(self.xml_path):
            print(f"The file {self.xml_path} does not exist.")
            return

        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()

            for elem in root.findall('record'):
                self.process_record(elem)

            self.remove_file()

        except Exception as e:
            print(f"Failed to process XML file: {e}")

    def process_record(self, elem):
        record_type = elem.attrib.get("type", "").lower()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        if record_type == "news":
            city = elem.findtext("city", default="Unknown")
            text = elem.findtext("text", default="")
            record = f"NEWS|{current_date}|{city}|{text}"

        elif record_type == "private_ad":
            text = elem.findtext("text", default="")
            exp_date_str = elem.findtext("expiration_date", default="")
            try:
                expiration_date = datetime.datetime.strptime(exp_date_str, "%Y-%m-%d")
                days_left = (expiration_date - datetime.datetime.now()).days
                record = f"PRIVATE_AD|{text}|{expiration_date.strftime('%Y-%m-%d')}|{days_left} days left"
            except ValueError:
                print(f"Invalid date format for ad: {exp_date_str}")
                return

        elif record_type == "custom":
            title = elem.findtext("title", default="")
            description = elem.findtext("description", default="")
            record = f"CUSTOM|{current_date}|{title}|{description}"

        else:
            print(f"Unknown record type: {record_type}")
            return

        write_to_file(record)
        print(f"Processed XML record: {record}")

    def remove_file(self):
        try:
            os.remove(self.xml_path)
            print(f"XML file {self.xml_path} processed and removed.")
        except Exception as e:
            print(f"Error removing XML file {self.xml_path}: {e}")

# === Статистика у CSV ===
def generate_statistics():
    file_path = "../news_feed.txt"
    if not os.path.exists(file_path):
        print("news_feed.txt not found.")
        return

    with open(file_path, 'r') as f:
        text = f.read()

    # Слова
    words = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    word_counts = Counter(words)

    with open("word_count.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word", "count"])
        for word, count in word_counts.items():
            writer.writerow([word, count])

    # Літери
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

# === Головна частина ===
if __name__ == "__main__":
    # Plain text
    if input("Do you want to process a plain text file? (y/n): ").strip().lower() == "y":
        file_path = input("Enter the path to the file (or press Enter to use the default): ").strip()
        FileProcessor(file_path if file_path else None).process_file()

    # JSON
    if input("Do you want to process a JSON file? (y/n): ").strip().lower() == "y":
        json_path = input("Enter the path to the JSON file (or press Enter to use the default): ").strip()
        JSONProcessor(json_path if json_path else None).process_json()

    # XML
    if input("Do you want to process an XML file? (y/n): ").strip().lower() == "y":
        xml_path = input("Enter the path to the XML file (or press Enter to use the default): ").strip()
        XMLProcessor(xml_path if xml_path else None).process_xml()

    # Manual input
    get_user_input()
    commit_to_git()
    generate_statistics()
    print("✔ All records processed, committed to Git, and statistics CSVs generated.")
