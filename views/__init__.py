# views/__init__.py
from .dashboard_view import DashboardView
from .settings_view import SettingsView
from .alerts_view import AlertsView
from .incident_history_view import IncidentHistoryView
from .about_system_view import AboutSystemView

__all__ = [
    'DashboardView',
    'SettingsView',
    'AlertsView',
    'IncidentHistoryView',
    'AboutSystemView',
]
