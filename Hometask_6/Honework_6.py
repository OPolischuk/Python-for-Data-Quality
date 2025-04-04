import datetime
import os


# Функція для запису в файл
def write_to_file(record):
    file_path = "../news_feed.txt"
    with open(file_path, 'a') as f:
        f.write(record + "\n")


# Функція для обробки 'News' типу
def handle_news():
    city = input("Enter the city for the news: ")
    text = input("Enter the news text: ")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    record = f"NEWS|{current_date}|{city}|{text}"
    write_to_file(record)


# Функція для обробки 'Private Ad' типу
def handle_private_ad():
    text = input("Enter the ad text: ")
    expiration_date = input("Enter the expiration date (YYYY-MM-DD): ")

    expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
    today = datetime.datetime.now()
    days_left = (expiration_date - today).days

    record = f"PRIVATE_AD|{text}|{expiration_date.strftime('%Y-%m-%d')}|{days_left} days left"
    write_to_file(record)


# Функція для обробки кастомного запису
def handle_custom_record():
    title = input("Enter the custom record title: ")
    description = input("Enter the custom record description: ")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    record = f"CUSTOM|{current_date}|{title}|{description}"
    write_to_file(record)


# Функція для отримання вводу від користувача щодо типу запису
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


# Функція для коміту до git
def commit_to_git():
    os.system("git add news_feed.txt")
    os.system('git commit -m "Added new record to news_feed"')


# Клас для обробки записів з файлу
class FileProcessor:
    def __init__(self, file_path=None):
        self.file_path = file_path or "default_folder/records.txt"  # Якщо шлях не вказаний, використовуємо папку за замовчуванням
        self.normalized_records = []

    # Нормалізація регістру тексту
    def normalize_case(self, text):
        return text.lower()  # Наприклад, приведення до нижнього регістру

    # Функція для обробки файлу
    def process_file(self):
        if not os.path.exists(self.file_path):
            print(f"The file {self.file_path} does not exist.")
            return

        with open(self.file_path, 'r') as file:
            records = file.readlines()
            for record in records:
                normalized_record = self.normalize_case(record.strip())  # Нормалізуємо регістр
                self.normalized_records.append(normalized_record)
                print(f"Processed record: {normalized_record}")

        # Видаляємо файл після успішної обробки
        self.remove_file()

    # Функція для видалення файлу
    def remove_file(self):
        try:
            os.remove(self.file_path)
            print(f"File {self.file_path} has been successfully processed and removed.")
        except Exception as e:
            print(f"Error removing file {self.file_path}: {e}")


if __name__ == "__main__":
    # Питання користувачу, чи він хоче завантажити файл для обробки
    process_file_input = input("Do you want to process a file? (y/n): ").strip().lower()

    if process_file_input == "y":
        file_path = input("Enter the path to the file (or press Enter to use the default): ").strip()
        file_processor = FileProcessor(file_path if file_path else None)
        file_processor.process_file()

    # Отримуємо ввід від користувача для ручного додавання записів
    get_user_input()
    commit_to_git()
    print("Record added successfully and committed to git!")
