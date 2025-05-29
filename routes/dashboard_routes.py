from flask import Blueprint, render_template
from controllers.dashboard_controller import DashboardController

dashboard_bp = Blueprint('dashboard', __name__)
controller = DashboardController()

@dashboard_bp.route('/')
def dashboard():
    return controller.index()
