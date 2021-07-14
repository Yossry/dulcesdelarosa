# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account',
                                          copy=False, oldname='project_id')

    @api.multi
    def do_scrap(self):
        super(StockScrap, self).do_scrap()
        if self.analytic_account_id:
            move = self.env['stock.move'].search([('scrapped', '=', True),('product_id','=', self.product_id.id),
                                                  ('reference','=',self.name)],limit=1)
            if move:
                move_line = self.env['stock.move.line'].search([('move_id', '=', move.id)])
                move.write({'analytic_account_id': self.analytic_account_id.id})
                move_line.write({'analytic_account_id': self.analytic_account_id.id})