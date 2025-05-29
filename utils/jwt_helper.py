import jwt

class JWTHelper:
    @staticmethod
    def encode_token(payload, secret):
        """
        Menghasilkan JWT token dari payload dengan HS256.
        """
        try:
            token = jwt.encode(payload, secret, algorithm='HS256')
            # Untuk Python < 3.9: jwt.encode() mengembalikan bytes
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            return token
        except Exception as e:
            print(f"Error encoding token: {e}")
            return None

    @staticmethod
    def decode_token(token, secret):
        """
        Meng-decode JWT token dan mengembalikan payload jika valid.
        """
        try:
            return jwt.decode(token, secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            print("Token telah kedaluwarsa.")
            return None
        except jwt.InvalidTokenError:
            print("Token tidak valid.")
            return None
