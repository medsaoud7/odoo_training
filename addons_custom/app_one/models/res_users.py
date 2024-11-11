from dataclasses import fields
from importlib.resources import _

from odoo import  api,models,fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    owner_ids = fields.One2many('owner','user_id')
    owners_count = fields.Integer(compute='_compute_owners_count')





    @api.depends('owner_ids')
    def _compute_owners_count(self):
        for rec in self:
            rec.owners_count = len(rec.owner_ids)



    def action_open_owners(self):
        self.ensure_one()
        owners = self.owner_ids
        model = 'owner'
        print(len(owners))
        if len(owners) > 1:
            return {
                'name': _('Related Owners'),
                'type': 'ir.actions.act_window',
                'res_model': model,
                'view_mode': 'kanban,tree,form',
                'domain': [('id', 'in', owners.ids)],
            }
        else:
            return {
            'name': _('Owner'),
            'type': 'ir.actions.act_window',
            'res_model': model,
            'res_id': owners.id,
            'view_mode': 'form',
        }
