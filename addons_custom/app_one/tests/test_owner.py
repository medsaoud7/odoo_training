from odoo.tests.common import TransactionCase


class TestOwner(TransactionCase):

    def setUp(self,*args,**kwargs):
        super(TestOwner,self).setUp()


        self.owner_01 = self.env['owner'].create({
            'name': 'owner_01',
            'phone': '859522',
            'address': 'Lac 3',

        })


    def test_01_owner_values(self):
        owner_id = self.owner_01

        self.assertRecordValues(owner_id,[{
            'name': 'owner_01',
            'phone': '859522',
            'address': 'Lac 3',
        }])



