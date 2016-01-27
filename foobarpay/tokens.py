import base64

from barcode import EAN13
from cairosvg import svg2pdf
from io import BytesIO
from jinja2 import Template
from random import randrange
from time import time

from foobarpay.model.customer import Customer
from foobarpay.logic import Logic

class TokenGenerator(object):

    def __init__(self, db):
        self.db = db

    def make_barcode(self):
        while True:
            id = randrange(999999999)
            if not self.db.get(Customer, id=id):
                self.db.get_or_create(Customer, id=id)
                self.db.commit()
                break
        ean = EAN13("{}{}".format(Logic.USER_ID_PREFIX, str(id).zfill(9)))
        f = BytesIO()
        ean.write(f, {'write_text': False})
        return base64.encodestring(f.getvalue()).decode('utf-8')

    def generate(self):
        with open('resource/customer_tokens_template.svg') as f:
            t = Template(f.read())
        with open('customer_tokens_{}.pdf'.format(time()), 'wb') as f:
            f.write(svg2pdf(t.render(make_barcode=self.make_barcode)))
