import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'oncotyping/oncotyping.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'oncotyping/db_repository')
SIJAX_STATIC_PATH = os.path.join(basedir, 'static/js/sijax/')
SIJAX_JSON_URI = os.path.join(basedir, '/static/js/sijax/json2.js')
WTF_CSRF_ENABLED = True
SECRET_KEY = 'x\xb7\xfb\x9b\x17:\xd1\xd72\xea\x17-\x13\xd4/\x93\x08>\xa1\xd3\x96\x15\xe7\xd1'
