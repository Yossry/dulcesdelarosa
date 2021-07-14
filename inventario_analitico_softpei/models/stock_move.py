# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True,
                                          states={'draft': [('readonly', False)], 'waiting': [('readonly', False)],
                                                  'confirmed': [('readonly', False)], 'assigned': [('readonly', False)]},
                                           oldname='project_id')



    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        res = super(StockMove, self)._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        if self.analytic_account_id:
            res['analytic_account_id'] = self.analytic_account_id.id
        return res


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True,
                                          states={'draft': [('readonly', False)], 'waiting': [('readonly', False)],
                                                  'confirmed': [('readonly', False)],
                                                  'assigned': [('readonly', False)]},
                                          oldname='project_id')


