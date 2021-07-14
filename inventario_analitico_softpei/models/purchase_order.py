from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def button_confirm(self):
        super(PurchaseOrder, self).button_confirm()
        for order in self.order_line:
            analytic_account_id = order.account_analytic_id.id
            moves = self.env['stock.move'].search([('purchase_line_id', '=', order.id)])
            if moves:
                move_lines = self.env['stock.move.line'].search([('move_id', 'in', moves.ids)])
                moves.write({'analytic_account_id': analytic_account_id})
                move_lines.write({'analytic_account_id': analytic_account_id})
