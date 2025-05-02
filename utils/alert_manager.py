# Create a new file: utils/alert_manager.py
class AlertManager:
    _instance = None
    _acknowledged_alerts = set()
    _observers = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlertManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def load_acknowledged_alerts(cls):
        try:
            with open('acknowledged_alerts.txt', 'r') as f:
                cls._acknowledged_alerts = set(line.strip() for line in f)
            print(f"Loaded {len(cls._acknowledged_alerts)} acknowledged alerts")
        except FileNotFoundError:
            print("No acknowledged alerts file found")
            cls._acknowledged_alerts = set()

    @classmethod
    def add_acknowledged_alert(cls, alert_id):
        cls._acknowledged_alerts.add(alert_id)
        with open('acknowledged_alerts.txt', 'a') as f:
            f.write(f"{alert_id}\n")
        cls.notify_observers()

    @classmethod
    def is_acknowledged(cls, alert_id):
        return alert_id in cls._acknowledged_alerts

    @classmethod
    def add_observer(cls, observer):
        if observer not in cls._observers:
            cls._observers.append(observer)

    @classmethod
    def notify_observers(cls):
        for observer in cls._observers:
            observer.on_alerts_updated()