from email.policy import default

from odoo import models , fields , api

from odoo.exceptions import ValidationError

# self.env.user.employee_id

class RealEstate(models.Model):

    _name = 'real.estate'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(required=True,tracking=1)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True,tracking=1)
    selling_price = fields.Float(required=True , default=0,tracking=1)
    difference = fields.Float(compute='_compute_difference',store=1)
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),
    ])
    owner_id = fields.Many2one('owner',default=lambda self: self.env['owner'].search([('user_id', '=', self.env.user.id)], limit=1))
    tag_ids = fields.Many2many('tag',string='Tags')
    state = fields.Selection([('draft','Draft'),('pending','Pending'),('sold','Sold'),],default='draft')

    bedroom_ids = fields.One2many('bedroom','real_estate_id')

    @api.constrains('expected_price')
    def _check_price(self):
        for rec in self:
            if rec.expected_price <= 0:
                raise ValidationError('Incorrect Price')

    @api.depends('expected_price','selling_price')
    def _compute_difference(self):
        for rec in self:
            rec.difference=rec.expected_price-rec.selling_price

    @api.model_create_multi
    #overriding crud
    def create(self, vals):
        res = super(RealEstate,self).create(vals)
        # logic
        return res
    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(RealEstate,self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside search methode")
        return res


    def write(self,vals):
        res = super(RealEstate,self).write(vals)
        print("updated")
        return res

    def unlink(self):
        res = super(RealEstate,self).unlink()
        print("deleted")
        return res

    def action_draft(self):
        for rec in self:
            print("inside draft action")
            rec.state='draft'

    def action_sold(self):
        for rec in self:
            rec.state='sold'

    def action_pending(self):
        for rec in self:
            rec.state='pending'


class Bedrooms(models.Model):
    _name = "bedroom"

    real_estate_id=fields.Many2one('real.estate')
    area =fields.Float()
    description= fields.Char()

