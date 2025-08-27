import datetime
from datetime import date
import os


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_date(prompt, allow_blank=False):
    """Get a valid date from user input"""
    while True:
        date_str = input(prompt).strip()

        if allow_blank and not date_str:
            return None

        if not date_str and not allow_blank:
            print("This field is required.")
            continue

        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def get_valid_option(prompt, options):
    """Get a valid option from a list of choices"""
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        try:
            choice = int(input("\nEnter your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Please enter a valid number.")


def press_enter_to_continue():
    """Wait for user to press Enter to continue"""
    input("\nPress Enter to continue...")


def display_menu():
    """Display the main menu"""
    clear_screen()
    print("=" * 50)
    print("      JOB APPLICATION TRACKER")
    print("=" * 50)
    print("1. Add a new application")
    print("2. View all applications")
    print("3. Update application status")
    print("4. Delete an application")
    print("5. Search applications")
    print("6. View companies")
    print("7. Exit")
    print("=" * 50)


def display_applications(applications):
    """Display a list of applications"""
    if not applications:
        print("No applications found.")
        press_enter_to_continue()
        return

    for app in applications:
        print(app.display())

    press_enter_to_continue()


def display_companies_stats(companies_stats):
    """Display company statistics"""
    if not companies_stats:
        print("No company data found.")
        press_enter_to_continue()
        return

    for company in companies_stats:
        name, total, applied, interviewing, offers, rejected, accepted, withdrawn = company

        print(f"Company: {name}")
        print(f"Total Applications: {total}")
        print(
            f"  Applied: {applied}, Interviewing: {interviewing}, Offers: {offers}")
        print(
            f"  Rejected: {rejected}, Accepted: {accepted}, Withdrawn: {withdrawn}")
        print("-" * 40)

    press_enter_to_continue()
