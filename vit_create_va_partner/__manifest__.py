# -*- coding: utf-8 -*-
{
    'name': "Create VA Partner",

    'summary': """
        Create Virtual Account for partner
    """,

    'description': """
        Create Virtual Account for partner
    """,

    'author': "Arman Nur Hidayat, richard.angga51@gmail.com",
    'website': "My Company",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/master_bank.xml',
        'views/views.xml',
    ],
}