from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from quadbase import qb_views
from oncotyping import onco_views, onco_admin
from indiafightasthma import ifa_views
