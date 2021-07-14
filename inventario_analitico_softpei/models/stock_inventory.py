# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Inventory(models.Model):
    _inherit = "stock.inventory"

    def action_validate(self):
        super(Inventory, self).action_validate()
        for line in self.line_ids:
            analytic_account = line.analytic_account_id.id
            moves = self.env['stock.move'].search([('partner_id', '=', self.partner_id.id),('inventory_id', '=', line.inventory_id.id),('product_id', '=', line.product_id.id)])
            if moves:
                moves.write({'analytic_account_id': analytic_account})
                for move in moves:
                    move_lines = self.env['stock.move.line'].search([('move_id', '=', move.id)])
                    move_lines.write({'analytic_account_id': analytic_account})






class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True,
                                          states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                          copy=False, oldname='project_id')
