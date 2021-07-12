# -*- coding: utf-8 -*-
##############################################################################
#
#    SIE CENTER custom module for Odoo
#    Copyright (C) 2021
#    @author: @cyntiafelix
#
##############################################################################

{
    'name': "SIE CENTER Application",
    'summary': """
        SIE CENTER custom module for recalculate Inventory Valuation""",
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'author': "Cyntia Felix",
    'license': 'Other proprietary',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'account',
        'product',
        'stock',
    ],
    'data': [
        'views/product_template_views.xml',
    ]
}
