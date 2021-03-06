"""EDI stock location tutorial

This example shows the code required to implement a simple EDI stock
location document format comprising a CSV file with a fixed list of
columns:

* Location barcode
* Location name
* Shelf number
"""

import csv
from odoo import api, fields, models


class EdiDocument(models.Model):
    """Extend ``edi.document`` to include EDI location tutorial records"""

    _inherit = 'edi.document'

    location_tutorial_ids = fields.One2many('edi.location.tutorial.record',
                                            'doc_id', string="Locations")


class EdiLocationTutorialRecord(models.Model):
    """EDI stock location tutorial record"""

    _edi_sync_deactivator = 'edi.inactive.location.record'

    _name = 'edi.location.tutorial.record'
    _inherit = 'edi.location.record'
    _description = "Stock Location"

    shelf = fields.Integer(string="Shelf", required=True, readonly=True,
                           help="Shelf number")

    @api.model
    def target_values(self, record_vals):
        """Construct ``stock.location`` field value dictionary"""
        loc_vals = super().target_values(record_vals)
        loc_vals.update({
            'posy': record_vals['shelf'],
        })
        return loc_vals


class EdiLocationTutorialDocument(models.AbstractModel):
    """EDI stock location tutorial document model"""

    _name = 'edi.location.tutorial.document'
    _inherit = 'edi.location.document'
    _description = "Tutorial stock location CSV file"

    @api.model
    def location_record_values(self, data):
        reader = csv.reader(data.decode().splitlines())
        return ({
            'name': barcode,
            'description': name,
            'shelf': int(shelf),
        } for barcode, name, shelf in reader)
