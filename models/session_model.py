from extensions.database import db

class UserSoalSession(db.Model):
    __tablename__ = 'user_soal_session'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    soal_id = db.Column(db.Integer, nullable=False)
    jawaban = db.Column(db.String(1))
    is_benar = db.Column(db.Boolean)
    lives_remaining = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
