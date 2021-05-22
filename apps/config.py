class Config:
    SECRET_KEY = '19f714e604daf22d7689ebd80964265f'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:''@localhost/ruu_ciptaker'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/assets/files'
