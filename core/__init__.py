from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy


secret_key = "0n)4~Uj)7<p:>dZm5ANGrs,yIaDK46h`S#@cDRb~V?D*3F)0]8~Lb@4B%%$b'N(]X-p`P~o+^2,vG!Z!72@m4+HAdRik@xjOv0WY{w<Z(A'dZXPo{Ez!2oE{hpN1E:5D-nuqjQaT*/SCuOkJ?WGU*0QDw)O8^,%8D1m>`H8L%nC9I1p&8v>T01%V@u&Y:5sBcvf4!D'}\W`5TXPV6rR{Du?y&mVB.j}uQ2z~cYnNFHN!;g!s"


db = SQLAlchemy()
db_name = 'students_data_mining_table.db'
def create_database(app, db):
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql'):
        with app.app_context():
            db.create_all()
            print('Database Created')

def index():
    return "Welcome to the main page! <a href='/gauth/logout'><button>Logout</button></a>"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:wahid@localhost:5432/students_data_mining_table'
    db.init_app(app)
    

    from .Authorization.controllers.logout import logout
    app.register_blueprint(logout, url_prefix = '/api/auth')
    from .Authorization.controllers.login import login
    app.register_blueprint(login, url_prefix = '/api')
    from .Authorization.controllers.signup import signup
    app.register_blueprint(signup, url_prefix = '/api/auth')
    from .testpages.test_google_login import test
    app.register_blueprint(test, url_prefix='/gauth')
    from .Authorization.controllers.google_auth import google_login_bp
    app.register_blueprint(google_login_bp, url_prefix='/gauth')
    from .resume_crud.re_crud import pdf_upload
    app.register_blueprint(pdf_upload, url_prefix='/resume')
    from .resume_crud.re_headline_crud import resume_headline_bp
    app.register_blueprint(resume_headline_bp, url_prefix='/api')
    from .key_skill.keyskill_crud import user_skill_bp
    app.register_blueprint(user_skill_bp, url_prefix='/key')
    from core.eduction_crud.edu_crud import education_bp
    app.register_blueprint(education_bp, url_prefix='/api')
    from core.basicdetails.basic_details import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/base')



    app.add_url_rule('/', 'index', index)
    create_database(app,db)
    return app

