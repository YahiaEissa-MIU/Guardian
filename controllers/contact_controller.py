class ContactController:
    def __init__(self, view):
        self.view = view

    def handle_feedback(self, feedback):
        """Process feedback and return message tuple"""
        feedback = feedback.strip()
        if not feedback:
            return ("Empty Message",
                    "Please write something before submitting.",
                    "warning")

        # Add actual submission logic here (email, database, etc)
        print(f"Feedback Submitted: {feedback}")
        return ("Thank you!",
                "Your feedback has been submitted.",
                "info")
