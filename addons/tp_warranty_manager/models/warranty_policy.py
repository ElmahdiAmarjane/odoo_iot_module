from odoo import fields, models


class WarrantyPolicy(models.Model):
    _name = 'warranty.policy'
    _description = 'Warranty Policy'

    name = fields.Char(
        string='Name',
        required=True,
    )

    duration_months = fields.Integer(
        string='Duration (Months)',
        default=12,
    )

    coverage = fields.Selection(
        selection=[
            ('parts', 'Parts'),
            ('parts_labor', 'Parts and Labor'),
            ('complete', 'Complete'),
        ],
        string='Coverage',
        default='parts',
    )

    description = fields.Html(
        string='Description',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
    )