from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class WarrantyClaim(models.Model):
    _name = 'warranty.claim'
    _description = 'Warranty Claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Claim Reference',
        required=True,
        copy=False,
        default='New',
        tracking=True,
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True,
    )

    policy_id = fields.Many2one(
        'warranty.policy',
        string='Warranty Policy',
        required=True,
    )

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sales Order',
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
    )

    lot_id = fields.Many2one(
        'stock.lot',
        string='Lot / Serial Number',
    )

    delivery_date = fields.Date(
        string='Delivery Date',
    )

    warranty_end_date = fields.Date(
        string='Warranty End Date',
        compute='_compute_warranty_end_date',
        store=True,
    )

    is_under_warranty = fields.Boolean(
        string='Under Warranty',
        compute='_compute_is_under_warranty',
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('approved', 'Approved'),
            ('refused', 'Refused'),
            ('done', 'Done'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )

    user_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user,
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )

    line_ids = fields.One2many(
        'warranty.claim.line',
        'claim_id',
        string='Claim Lines',
    )

    total_cost = fields.Monetary(
        string='Total Cost',
        compute='_compute_total_cost',
        store=True,
    )

    currency_id = fields.Many2one(
        related='company_id.currency_id',
        string='Currency',
        store=True,
    )

    @api.depends('delivery_date', 'policy_id.duration_months')
    def _compute_warranty_end_date(self):
        for claim in self:
            if claim.delivery_date and claim.policy_id:
                claim.warranty_end_date = (
                    claim.delivery_date
                    + relativedelta(
                        months=claim.policy_id.duration_months
                    )
                )
            else:
                claim.warranty_end_date = False

    @api.depends('warranty_end_date')
    def _compute_is_under_warranty(self):
        today = fields.Date.context_today(self)

        for claim in self:
            claim.is_under_warranty = (
                bool(claim.warranty_end_date)
                and today <= claim.warranty_end_date
            )

    @api.depends('line_ids.subtotal')
    def _compute_total_cost(self):
        for claim in self:
            claim.total_cost = sum(claim.line_ids.mapped('subtotal'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'warranty.claim'
                ) or 'New'

        return super().create(vals_list)


    @api.constrains('delivery_date', 'warranty_end_date')
    def _check_warranty_dates(self):
        for claim in self:
            if (
                claim.delivery_date
                and claim.warranty_end_date
                and claim.warranty_end_date < claim.delivery_date
            ):
                raise ValidationError(
                    'The warranty end date cannot be before the delivery date.'
                )

    @api.constrains('policy_id')
    def _check_policy_duration(self):
        for claim in self:
            if claim.policy_id and claim.policy_id.duration_months <= 0:
                raise ValidationError(
                    'The warranty duration must be greater than zero.'
                )

    def action_submit(self):
        for claim in self:
            if claim.state != 'draft':
                continue

            claim.state = 'submitted'

        return True

    def action_approve(self):
        for claim in self:
            if claim.state != 'submitted':
                continue

            claim.state = 'approved'

        return True

    def action_refuse(self):
        for claim in self:
            if claim.state != 'submitted':
                continue

            claim.state = 'refused'

        return True

    def action_done(self):
        for claim in self:
            if claim.state != 'approved':
                continue

            claim.state = 'done'

        return True

    @api.depends('name', 'partner_id')
    def _compute_display_name(self):
        for claim in self:
            if claim.partner_id:
                claim.display_name = f'{claim.name} - {claim.partner_id.name}'
            else:
                claim.display_name = claim.name

    def unlink(self):
        for claim in self:
            if claim.state not in ('draft', 'refused'):
                raise ValidationError(
                    'A submitted, approved, or done claim cannot be deleted.'
                )

        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = 'New'
        default['state'] = 'draft'
        return super().copy(default)
    