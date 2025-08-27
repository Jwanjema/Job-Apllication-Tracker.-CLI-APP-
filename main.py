from database import init_db, get_session, add_application, get_all_applications, update_application_status, delete_application, search_applications, get_companies_stats
from utils import clear_screen, get_valid_date, get_valid_option, press_enter_to_continue, display_menu, display_applications, display_companies_stats
from datetime import date


class JobApplicationTracker:
    def __init__(self):
        self.engine = init_db()
        self.session = get_session(self.engine)

    def add_application(self):
        """Add a new job application"""
        clear_screen()
        print("=== Add New Job Application ===\n")

        job_title = input("Job Title: ").strip()
        company = input("Company: ").strip()
        app_date = get_valid_date(
            "Application Date (YYYY-MM-DD, today if blank): ", allow_blank=True) or date.today()

        status_options = ["Applied", "Interviewing",
                          "Offer", "Rejected", "Accepted", "Withdrawn"]
        status = get_valid_option("Select status:", status_options)

        deadline = get_valid_date(
            "Deadline (YYYY-MM-DD, optional): ", allow_blank=True)
        notes = input("Notes (optional): ").strip()

        # Save to database
        app_id = add_application(
            self.session, job_title, company, app_date, status, deadline, notes)
        print(
            f"\nApplication for {job_title} at {company} added successfully (ID: {app_id})!")
        press_enter_to_continue()

    def view_applications(self):
        """View all job applications"""
        clear_screen()
        print("=== All Job Applications ===\n")

        applications = get_all_applications(self.session)
        display_applications(applications)

    def update_application(self):
        """Update an application's status"""
        clear_screen()
        print("=== Update Application Status ===\n")

        # First show all applications
        applications = get_all_applications(self.session)
        if not applications:
            print("No applications found.")
            press_enter_to_continue()
            return

        print("Current Applications:\n")
        for app in applications:
            print(
                f"{app.id}. {app.job_title} at {app.company} - Current Status: {app.status}")

        # Get application to update
        while True:
            try:
                app_id = int(
                    input("\nEnter the ID of the application to update: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        # Get new status
        status_options = ["Applied", "Interviewing",
                          "Offer", "Rejected", "Accepted", "Withdrawn"]
        new_status = get_valid_option("Select new status:", status_options)

        # Update database
        success = update_application_status(self.session, app_id, new_status)
        if success:
            print("Application status updated successfully!")
        else:
            print(f"No application found with ID {app_id}.")

        press_enter_to_continue()

    def delete_application(self):
        """Delete an application"""
        clear_screen()
        print("=== Delete Application ===\n")

        # First show all applications
        applications = get_all_applications(self.session)
        if not applications:
            print("No applications found.")
            press_enter_to_continue()
            return

        print("Current Applications:\n")
        for app in applications:
            print(f"{app.id}. {app.job_title} at {app.company}")

        # Get application to delete
        while True:
            try:
                app_id = int(
                    input("\nEnter the ID of the application to delete: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        # Confirm deletion
        confirm = input(
            f"Are you sure you want to delete application {app_id}? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled.")
            press_enter_to_continue()
            return

        # Delete from database
        success = delete_application(self.session, app_id)
        if success:
            print("Application deleted successfully!")
        else:
            print(f"No application found with ID {app_id}.")

        press_enter_to_continue()

    def search_applications(self):
        """Search applications by company or job title"""
        clear_screen()
        print("=== Search Applications ===\n")

        search_term = input(
            "Enter company name or job title to search for: ").strip()

        if not search_term:
            print("Please enter a search term.")
            press_enter_to_continue()
            return

        applications = search_applications(self.session, search_term)

        clear_screen()
        print(f"=== Search Results for '{search_term}' ===\n")
        display_applications(applications)

    def view_companies(self):
        """View statistics by company"""
        clear_screen()
        print("=== Company Statistics ===\n")

        companies_stats = get_companies_stats(self.session)
        display_companies_stats(companies_stats)

    def run(self):
        """Main application loop"""
        while True:
            display_menu()

            choice = input("\nEnter your choice (1-7): ").strip()

            if choice == '1':
                self.add_application()
            elif choice == '2':
                self.view_applications()
            elif choice == '3':
                self.update_application()
            elif choice == '4':
                self.delete_application()
            elif choice == '5':
                self.search_applications()
            elif choice == '6':
                self.view_companies()
            elif choice == '7':
                print("Goodbye!")
                self.session.close()
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                press_enter_to_continue()


if __name__ == "__main__":
    tracker = JobApplicationTracker()
    tracker.run()
