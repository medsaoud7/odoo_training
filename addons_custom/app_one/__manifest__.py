{
    'name': "App One",
    'author': "Mohamed Saoud",
    'category': 'Services',
    'version': '17.0.0.1.0',
    'depends': ['base','sale_management','purchase','mail'
                ],
    'data': [
        'views/base_menu.xml',
        'views/property_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/res_users.xml',
        'views/sale_order_inherit_view.xml',


    ],
    'application': True,
    'images': ['static/description/icon.png'],

}