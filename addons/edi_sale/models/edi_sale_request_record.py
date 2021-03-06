"""EDI sale order request records"""

from odoo import api, fields, models


class EdiSaleRequestRecord(models.Model):
    """EDI sale order request record

    This is the base model for EDI sale order request records.  Each
    row represents a sale order that will be created or updated when
    the document is executed.

    The fields within each record represent the fields within the
    source document, which may not exactly correspond to fields of the
    ``sale.order`` model.

    Derived models should implement :meth:`~.target_values`.
    """

    _name = 'edi.sale.request.record'
    _inherit = 'edi.record.sync'
    _description = "Sale Request"

    _edi_sync_target = 'sale_id'
    _edi_sync_via = 'name'
    _edi_sync_domain = [('state', '!=', 'cancel')]

    sale_id = fields.Many2one('sale.order', string="Sale",
                              required=False, readonly=True, index=True)
    customer_key = fields.Char('Customer Name', required=True, readonly=True,
                               index=True, edi_relates='customer_id.name')
    customer_id = fields.Many2one('res.partner', string='Customer',
                                  required=False, readonly=True, index=True)

    _sql_constraints = [('doc_name_uniq', 'unique (doc_id, name)',
                         "Each name may appear at most once per document")]

    @api.model
    def target_values(self, record_vals):
        """Construct ``sale.order`` value dictionary"""
        sale_vals = super().target_values(record_vals)
        sale_vals.update({
            'name': record_vals['name'],
            'partner_id': record_vals['customer_id'],
        })
        return sale_vals
