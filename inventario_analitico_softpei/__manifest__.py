# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Softpei Analitic Inventories',
    'version': '1.0',
    'summary': 'Analytic for Inventories',
    'description': """

====================
This Module allow include the annalitic accounts field in the modules of Inventories and Manufactoring and his reports 
    """,
    'category': 'Invoicing Management',
    'depends': ['analytic', 'stock', 'mrp', 'sale', 'purchase'],
    'data': [
        'views/stock_move_view.xml',
        'views/mrp_production_views.xml',
        'views/configuration_analytic_account_menus.xml',
        'views/stock_scrap_view.xml',
        'views/stock_inventory_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
