from urllib.parse import quote_plus as urlquote

SECRET_KEY = 'your_secret_key_here'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://admin:{urlquote("reju@20220601!")}@{"180.76.100.226"}:3306/lwm2m'
SQLALCHEMY_TRACK_MODIFICATIONS = False
