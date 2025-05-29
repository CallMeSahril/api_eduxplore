from models.soal_model import SoalModel
from models.user_model import UserModel
from utils.file_helper import save_image_from_url
from datetime import datetime


class SoalController:
    from datetime import datetime

    def get_soal_for_user(self, user_id):
        user_model = UserModel()
        user = user_model.find_by_id(user_id)
        if not user:
            user_model.close()
            return {'message': 'User tidak ditemukan'}, 404

        kelas_id = user['kelas_id']

        soal_model = SoalModel()
        soal = soal_model.get_random_soal_by_kelas(kelas_id)
        soal_model.close()
        user_model.close()

        if not soal:
            return {'message': 'Soal tidak ditemukan untuk kelas ini'}, 404

        # Ubah semua datetime jadi string
        for k, v in soal.items():
            if isinstance(v, datetime):
                soal[k] = v.isoformat()

        soal.pop('jawaban_benar', None)
        return soal, 200

    def create_soal(self, args, gambar_file):
        import os
        from flask import current_app
        from models.soal_model import SoalModel

        pertanyaan = args.get("pertanyaan")
        pilihan_a = args.get("pilihan_a")
        pilihan_b = args.get("pilihan_b")
        pilihan_c = args.get("pilihan_c")
        pilihan_d = args.get("pilihan_d")
        jawaban_benar = args.get("jawaban_benar")
        kelas_id = args.get("kelas_id")
        province_id = args.get("province_id")  # ← ambil dari form

        if not pertanyaan and not gambar_file:
            return {"message": "Minimal pertanyaan atau gambar harus diisi."}, 400

        gambar_path = None
        if gambar_file:
            try:
                folder = os.path.join(current_app.root_path, 'uploads')
                os.makedirs(folder, exist_ok=True)

                filename = f"soal_{str(hash(gambar_file.filename))}.jpg"
                file_path = os.path.join(folder, filename)
                gambar_file.save(file_path)

                gambar_path = f"uploads/{filename}"
            except Exception as e:
                return {"message": f"Gagal menyimpan gambar: {str(e)}"}, 500

        try:
            soal_model = SoalModel()
            soal_model.create_soal(
                pertanyaan=pertanyaan or "",
                gambar_path=gambar_path,
                pilihan_a=pilihan_a,
                pilihan_b=pilihan_b,
                pilihan_c=pilihan_c,
                pilihan_d=pilihan_d,
                jawaban_benar=jawaban_benar,
                kelas_id=kelas_id,
                province_id=province_id  # ← disimpan ke DB
            )
            soal_model.close()
            return {"message": "Soal berhasil ditambahkan"}, 201
        except Exception as e:
            return {"message": f"Gagal menyimpan soal: {str(e)}"}, 500

    def get_all_soal(self):
        try:
            soal_model = SoalModel()
            daftar_soal = soal_model.get_all_soal()
            soal_model.close()

            # Format datetime jadi string & gambar
            for soal in daftar_soal:
                for k, v in soal.items():
                    if isinstance(v, datetime):
                        soal[k] = v.isoformat()
            return daftar_soal
        except Exception as e:
            print("[ERROR] Gagal mengambil soal:", e)
            return []
