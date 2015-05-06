from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class OncoLoginForm(Form):
    username = StringField(label='Oncotyping Username', validators=[DataRequired('Please enter username')])
    password = PasswordField(label='Password', validators=[DataRequired('You forgot to enter password')])
    remember_me = BooleanField(label='Remember me', default=False)


class OncoEntryForm(Form):
    code = StringField(label='Patient code')
    pathology_report_id = StringField(label='Histopathology number')
    date_of_collection = DateField(label='Date of Sample collection')
    date_of_resection = DateField(label='Date of Tumour resection')
    place_of_collection = StringField(label='Place of sample collection')
    age = IntegerField(label='Patient age')
    weight = IntegerField(label='Patient weight')
    menopause = BooleanField(label='Menopause ?')
    hiv_status = BooleanField(label='Is patient HIV positive ?')
    familial_history = StringField(label='History of cancer in patient family')
    normal_sample_collected = BooleanField(label='Normal sample collected?')
    normal_tissue_proximity = StringField(label='Normal tissue proximity')
    excision_method = StringField(label='Tumour excision methodology')
    tumour_type = StringField(label='Tumour type')
    tumour_site = StringField(label='Tumour site')
    tnm_staging = StringField(label='TNM staging')
    er_status = BooleanField(label='ER positive ?')
    pr_status = BooleanField(label='PR positive ?')
    her2_status = BooleanField(label='HER2 positive ?')
    neo_adjuvant_chemotherapy = StringField(label='Neo adjuvant chemotherapy')
    neo_adjuvant_radiotherapy = StringField(label='Neoadjuvant radiotherapy')
    adjuvant_chemotherapy = StringField(label='Adjuvant chemotherapy')
    adjuvant_radiotherapy = StringField(label='Adjuvant radiotherapy')
    targeted_molecular_therapy = StringField(label='Hormonal therapy?')
    patient_alive = BooleanField(label='Patient alive?')
    date_of_death = DateField(label='Date of death')
    date_of_last_contact = DateField(label='Date of last contact')
    remission_history = StringField(label='Remission history')
    comments = StringField(label="Other comments")
