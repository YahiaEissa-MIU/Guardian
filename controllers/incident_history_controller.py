import os
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess


class IncidentHistoryController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def get_incidents(self, filter_type=None, filter_value=None):
        """Gets filtered incidents from the model."""
        return self.model.get_incidents(filter_type, filter_value)

    def export_incident_history(self, filename="incident_history.csv"):
        """Handles exporting filtered incident history to a CSV file."""
        filter_type = self.view.get_filter_type()  # ✅ Fetch filter type
        filter_value = self.view.get_filter_value()  # ✅ Fetch filter value

        incidents = self.get_incidents(filter_type, filter_value)  # ✅ Use correct values

        if not incidents:
            self.view.show_message("No incidents to export.", "red")
            return

        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Date", "Incident", "Action"])
                writer.writeheader()
                writer.writerows(incidents)

            self.view.show_message(f"Exported successfully to {filename}", "green")
        except Exception as e:
            self.view.show_message(f"Error exporting file: {e}", "red")

    def generate_pdf(self):
        """Generates a new PDF file with the incident history."""

        # ✅ Use method calls instead of attributes
        filter_type = self.view.get_filter_type()
        filter_value = self.view.get_filter_value()

        incidents = self.get_incidents(filter_type, filter_value)

        if not incidents:
            self.view.show_message("No incidents to export.", "red")
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"incident_history_{timestamp}.pdf"
            pdf_path = os.path.join(os.getcwd(), filename)

            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica", 12)

            c.drawString(100, 750, "Incident History Report")
            c.line(100, 745, 500, 745)

            y_position = 730
            for incident in incidents:
                line = f"{incident['Date']} - {incident['Incident']} - Action: {incident['Action']}"
                c.drawString(100, y_position, line)
                y_position -= 20

            c.save()
            self.view.show_message(f"PDF successfully created: {pdf_path}", "green")
            return pdf_path  # ✅ Return the file path

        except Exception as e:
            self.view.show_message(f"Error generating PDF: {e}", "red")
            return None

    def print_incident_history(self):
        """Generates a new PDF and sends it to the printer."""
        pdf_file = self.generate_pdf()  # Always create a new PDF

        if not pdf_file or not os.path.exists(pdf_file):
            self.view.show_message("Error: PDF file not found!", "red")
            return

        try:
            print_command = f'cmd /c start /min "" "{pdf_file}" /p'
            subprocess.run(print_command, shell=True, check=True)
        except Exception as e:
            print(f"Error printing PDF: {e}")
