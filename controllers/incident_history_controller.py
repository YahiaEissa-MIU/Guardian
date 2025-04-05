import os
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess
import logging


class IncidentHistoryController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        # Add the view as an observer to the model
        self.model.add_observer(self.view.update_incidents)
        # Initial data load
        self.refresh_incidents()

    def refresh_incidents(self):
        """Refreshes incidents from Shuffle SOAR"""
        try:
            success = self.model.sync_incidents()
            if success:
                self.view.update_incidents()
                return True
            else:
                self.view.show_message("Failed to fetch incidents from Shuffle", "red")
                return False
        except Exception as e:
            logging.error(f"Error refreshing incidents: {str(e)}")
            self.view.show_message(f"Error refreshing incidents: {str(e)}", "red")
            return False

    def get_incidents(self, filter_type=None, filter_value=None):
        """Gets filtered incidents from the model."""
        try:
            return self.model.get_incidents(filter_type, filter_value)
        except Exception as e:
            logging.error(f"Error getting incidents: {str(e)}")
            self.view.show_message(f"Error retrieving incidents: {str(e)}", "red")
            return []

    def export_incident_history(self):
        """Handles exporting filtered incident history to a CSV file."""
        try:
            filter_type = self.view.get_filter_type()
            filter_value = self.view.get_filter_value()
            incidents = self.get_incidents(filter_type, filter_value)

            if not incidents:
                self.view.show_message("No incidents to export.", "red")
                return

            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"incident_history_{timestamp}.csv"

            success, message = self.model.export_to_csv(filename)

            if success:
                self.view.show_message(message, "green")
            else:
                self.view.show_message(message, "red")

        except Exception as e:
            logging.error(f"Error in export_incident_history: {str(e)}")
            self.view.show_message(f"Error exporting incidents: {str(e)}", "red")

    def generate_pdf(self):
        """Generates a new PDF file with the incident history."""
        try:
            filter_type = self.view.get_filter_type()
            filter_value = self.view.get_filter_value()
            incidents = self.get_incidents(filter_type, filter_value)

            if not incidents:
                self.view.show_message("No incidents to export.", "red")
                return None

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"incident_history_{timestamp}.pdf"
            pdf_path = os.path.join(os.getcwd(), filename)

            c = canvas.Canvas(pdf_path, pagesize=letter)

            # Set up the document
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 750, "Incident Response History")
            c.setFont("Helvetica", 12)
            c.drawString(100, 730, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Add filter information if applied
            if filter_type != "All" and filter_value:
                c.drawString(100, 710, f"Filter: {filter_type} - {filter_value}")

            c.line(100, 700, 500, 700)

            # Add incidents
            y_position = 680
            for incident in incidents:
                # Check if we need a new page
                if y_position < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = 750

                # Format each incident entry
                date_text = f"Date: {incident['Date']}"
                incident_text = f"Incident: {incident['Incident']}"
                action_text = f"Action: {incident['Action']}"

                c.drawString(100, y_position, date_text)
                c.drawString(100, y_position - 15, incident_text)
                c.drawString(100, y_position - 30, action_text)

                # Add a separator line
                c.line(100, y_position - 40, 500, y_position - 40)

                y_position -= 60

            c.save()
            self.view.show_message(f"PDF successfully created: {filename}", "green")
            return pdf_path

        except Exception as e:
            logging.error(f"Error generating PDF: {str(e)}")
            self.view.show_message(f"Error generating PDF: {str(e)}", "red")
            return None

    def print_incident_history(self):
        """Generates a new PDF and sends it to the printer."""
        try:
            pdf_file = self.generate_pdf()

            if not pdf_file or not os.path.exists(pdf_file):
                self.view.show_message("Error: PDF file not found!", "red")
                return

            if os.name == 'nt':  # Windows
                try:
                    print_command = f'cmd /c start /min "" "{pdf_file}" /p'
                    subprocess.run(print_command, shell=True, check=True)
                    self.view.show_message("Document sent to printer", "green")
                except subprocess.CalledProcessError as e:
                    raise Exception(f"Printing failed: {str(e)}")
            else:  # Unix/Linux/Mac
                try:
                    print_command = f'lpr "{pdf_file}"'
                    subprocess.run(print_command, shell=True, check=True)
                    self.view.show_message("Document sent to printer", "green")
                except subprocess.CalledProcessError as e:
                    raise Exception(f"Printing failed: {str(e)}")

        except Exception as e:
            logging.error(f"Error in print_incident_history: {str(e)}")
            self.view.show_message(f"Error printing document: {str(e)}", "red")

    def cleanup_old_files(self, max_age_days=7):
        """Cleans up old PDF and CSV files"""
        try:
            current_time = datetime.now()
            for filename in os.listdir(os.getcwd()):
                if filename.startswith("incident_history_") and (
                        filename.endswith(".pdf") or filename.endswith(".csv")):
                    file_path = os.path.join(os.getcwd(), filename)
                    file_age = datetime.now() - datetime.fromtimestamp(os.path.getctime(file_path))

                    if file_age.days > max_age_days:
                        os.remove(file_path)
                        logging.info(f"Cleaned up old file: {filename}")
        except Exception as e:
            logging.error(f"Error cleaning up old files: {str(e)}")