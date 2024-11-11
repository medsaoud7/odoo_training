from odoo import api,fields,models


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    real_estate_id= fields.Many2one('real.estate')


    def action_confirm(self):
        res = super(SaleOrderInherit,self).action_confirm()
        print("confirm")
        return res

