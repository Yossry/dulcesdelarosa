# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _action_confirm(self):
        super(SaleOrder, self)._action_confirm()
        # passing the analytic_account parameter to the stock moves lines and the stock moves
        if self.order_line and self.analytic_account_id:
            moves = self.env['stock.move'].search([('sale_line_id', 'in', self.order_line.ids)])
            if moves:
                move_lines = self.env['stock.move.line'].search([('move_id', 'in', moves.ids)])
                moves.write({'analytic_account_id': self.analytic_account_id.id})
                move_lines.write({'analytic_account_id': self.analytic_account_id.id})

