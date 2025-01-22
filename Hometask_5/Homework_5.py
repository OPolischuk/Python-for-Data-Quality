import datetime
import os


# Function to write to the file in the required format
def write_to_file(record):
    file_path = "news_feed.txt"
    with open(file_path, 'a') as f:
        f.write(record + "\n")


# Function to handle 'News' type
def handle_news():
    city = input("Enter the city for the news: ")
    text = input("Enter the news text: ")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    record = f"NEWS|{current_date}|{city}|{text}"
    write_to_file(record)


# Function to handle 'Private Ad' type
def handle_private_ad():
    text = input("Enter the ad text: ")
    expiration_date = input("Enter the expiration date (YYYY-MM-DD): ")

    expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
    today = datetime.datetime.now()
    days_left = (expiration_date - today).days

    record = f"PRIVATE_AD|{text}|{expiration_date.strftime('%Y-%m-%d')}|{days_left} days left"
    write_to_file(record)


# Function for a custom record type (Unique)
def handle_custom_record():
    title = input("Enter the custom record title: ")
    description = input("Enter the custom record description: ")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    record = f"CUSTOM|{current_date}|{title}|{description}"
    write_to_file(record)


# Function to get user input for the type of record
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


# Function to commit the file to Git
def commit_to_git():
    os.system("git add news_feed.txt")
    os.system('git commit -m "Added new record to news_feed"')


if __name__ == "__main__":
    get_user_input()
    commit_to_git()
    print("Record added successfully and committed to git!")
