from sclab_sites.oncotyping.onco_views import oncotypingdb as db


class User(db.Model):
    id = db.Column(db.String(64), primary_key=True, index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)

    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username


class Patient(db.Model):

    code = db.Column(db.String(200), primary_key=True, unique=True)
    pathology_report_id = db.Column(db.String(200), unique=True)
    date_of_collection = db.Column(db.DateTime)
    date_of_resection = db.Column(db.DateTime)
    place_of_collection = db.Column(db.String(200))
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    menopause = db.Column(db.Boolean)
    hiv_status = db.Column(db.Boolean)
    familial_history = db.Column(db.String(200))
    normal_sample_collected = db.Column(db.Boolean)
    normal_tissue_proximity = db.Column(db.String(200))
    excision_method = db.Column(db.String(200))
    tumour_type = db.Column(db.String(200))
    tumour_site = db.Column(db.String(200))
    tnm_staging = db.Column(db.String(200))
    er_status = db.Column(db.Boolean)
    pr_status = db.Column(db.Boolean)
    her2_status = db.Column(db.Boolean)
    neo_adjuvant_chemotherapy = db.Column(db.String(200))
    neo_adjuvant_radiotherapy = db.Column(db.String(200))
    adjuvant_chemotherapy = db.Column(db.String(200))
    adjuvant_radiotherapy = db.Column(db.String(200))
    targeted_molecular_therapy = db.Column(db.String(200))
    patient_alive = db.Column(db.Boolean)
    date_of_death = db.Column(db.DateTime)
    date_of_last_contact = db.Column(db.DateTime)
    remission_history = db.Column(db.String(200))
    comments = db.Column(db.String(200))

    def __init__(self, code, pathology_report_id, date_of_collection, date_of_resection,
                 place_of_collection, age, weight, menopause, hiv_status, familial_history,
                 normal_sample_collected, normal_tissue_proximity, excision_method, tumour_type,
                 tumour_site, tnm_staging, er_status, pr_status, her2_status, neo_adjuvant_chemotherapy,
                 neo_adjuvant_radiotherapy, adjuvant_chemotherapy, adjuvant_radiotherapy,
                 targeted_molecular_therapy, patient_alive, date_of_death, date_of_last_contact,
                 remission_history, comments):

        self.code = code
        self.pathology_report_id = pathology_report_id
        self.date_of_collection = date_of_collection
        self.date_of_resection = date_of_resection
        self.place_of_collection = place_of_collection
        self.age = age
        self.weight = weight
        self.menopause = menopause
        self.hiv_status = hiv_status
        self.familial_history = familial_history
        self.normal_sample_collected = normal_sample_collected
        self.normal_tissue_proximity = normal_tissue_proximity
        self.excision_method = excision_method
        self.tumour_type = tumour_type
        self.tumour_site = tumour_site
        self.tnm_staging = tnm_staging
        self.er_status = er_status
        self.pr_status = pr_status
        self.her2_status = her2_status
        self.neo_adjuvant_chemotherapy = neo_adjuvant_chemotherapy
        self.neo_adjuvant_radiotherapy = neo_adjuvant_radiotherapy
        self.adjuvant_chemotherapy = adjuvant_chemotherapy
        self.adjuvant_radiotherapy = adjuvant_radiotherapy
        self.targeted_molecular_therapy = targeted_molecular_therapy
        self.patient_alive = patient_alive
        self.date_of_death = date_of_death
        self.date_of_last_contact = date_of_last_contact
        self.remission_history = remission_history
        self.comments = comments

    def __str__(self):
        return '<Patient code %r>' % self.code
