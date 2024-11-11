from odoo import api,fields,models



class Trainer(models.Model):
    _name = "trainer"

    session_ids = fields.Many2many('session', string="Sessions")

    name = fields.Char(required =1)
    number_registration=fields.Integer(required=1)
    diploma=fields.Char()

