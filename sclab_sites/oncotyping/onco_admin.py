from sclab_sites import app
from flask_admin import Admin
from flask_admin.contrib import sqla
from sclab_sites.oncotyping.onco_models import Patient
from sclab_sites.oncotyping.onco_views import oncotypingdb as db

admin = Admin(app, name='Oncotyping')


class OncoAdmin(sqla.ModelView):
    column_display_pk = True

admin.add_view(OncoAdmin(Patient, db.session))
