from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.soal_model import SoalModel
from models.user_model import UserModel
from models.kelas_model import KelasModel
from models.province_model import ProvinceModel
from models.island_model import IslandModel
from controllers.soal_controller import SoalController

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route("/delete/<int:soal_id>", methods=["POST"])
def delete_soal(soal_id):
    controller = SoalController()
    result, status = controller.delete_soal(soal_id)
    flash(result["message"], "success" if status == 200 else "error")
    return redirect(url_for("dashboard.dashboard", tab="soal"))


@dashboard_bp.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        controller = SoalController()
        result, status = controller.create_soal(
            request.form, request.files.get("gambar"))
        flash(result["message"], "success" if status == 201 else "error")

        return redirect(url_for("dashboard.dashboard"))

    soal_model = SoalModel()
    soal_data = soal_model.get_all_soal()
    soal_model.close()

    kelas_model = KelasModel()
    kelas_data = kelas_model.get_all_kelas()
    kelas_model.close()

    user_model = UserModel()
    user_data = user_model.get_all_users()
    user_model.close()

    province_model = ProvinceModel()
    province_data = province_model.get_all_provinces()
    province_model.close()

    island_model = IslandModel()
    island_data = island_model.get_all_islands()
    island_model.close()

    active_tab = request.args.get("tab", "soal")
    return render_template("dashboard.html",
                           kelas=kelas_data,
                           soal=soal_data,
                           users=user_data,
                           provinces=province_data,
                           islands=island_data,
                           active_tab=active_tab)
