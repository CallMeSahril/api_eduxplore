from flask import render_template

class DashboardController:
    def index(self):
        return render_template('dashboard.html', title="Dashboard Admin")
