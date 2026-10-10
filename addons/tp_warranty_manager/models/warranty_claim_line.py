from odoo import api, fields, models


class WarrantyClaimLine(models.Model):
    _name = 'warranty.claim.line'
    _description = 'Warranty Claim Line'

    claim_id = fields.Many2one(
        'warranty.claim',
        string='Claim',
        required=True,
        ondelete='cascade',
    )

    description = fields.Char(
        string='Description',
        required=True,
    )

    line_type = fields.Selection(
        selection=[
            ('repair', 'Repair'),
            ('replacement', 'Replacement'),
            ('labor', 'Labor'),
        ],
        string='Type',
        required=True,
        default='repair',
    )

    quantity = fields.Float(
        string='Quantity',
        default=1.0,
    )

    unit_cost = fields.Monetary(
        string='Unit Cost',
        currency_field='currency_id',
    )

    subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
    )

    currency_id = fields.Many2one(
        related='claim_id.company_id.currency_id',
        string='Currency',
        store=True,
    )

    @api.depends('quantity', 'unit_cost')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_cost