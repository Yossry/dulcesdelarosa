# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True,
                                          states={'confirmed': [('readonly', False)], 'planned': [('readonly', False)],
                                                  'progress': [('readonly', False)]},
                                          copy=False, oldname='project_id')


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.multi
    def record_production(self):
        super(MrpWorkorder, self).record_production()
        for move in self.move_raw_ids:
            if self.production_id.analytic_account_id:
                    move_line = self.env['stock.move.line'].search([('move_id', '=', move.id)])
                    move.write({'analytic_account_id': self.production_id.analytic_account_id.id})
                    move_line.write({'analytic_account_id': self.production_id.analytic_account_id.id})

        for move in self.move_line_ids:
            move.write({'analytic_account_id': self.production_id.analytic_account_id.id})
            move_move = self.env['stock.move'].search([('id', '=', move.move_id.id)])
            move_move.write({'analytic_account_id': self.production_id.analytic_account_id.id})

        production_move = self.production_id.move_finished_ids
        production_move.write({'analytic_account_id': self.production_id.analytic_account_id.id})
        for move in production_move:
            move_line = self.env['stock.move.line'].search([('move_id', '=', move.id)])
            move_line.write({'analytic_account_id': self.production_id.analytic_account_id.id})


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.multi
    def do_produce(self):
        super(MrpProductProduce, self).do_produce()
        for move in self.production_id.move_finished_ids:
            if self.production_id.analytic_account_id:
                    move_line = self.env['stock.move.line'].search([('move_id', '=', move.id)])
                    move.write({'analytic_account_id': self.production_id.analytic_account_id.id})
                    move_line.write({'analytic_account_id': self.production_id.analytic_account_id.id})

        for move in self.produce_line_ids:
            move_line = self.env['stock.move.line'].search([('move_id', '=', move.move_id.id)])
            move_line.write({'analytic_account_id': self.production_id.analytic_account_id.id})
            move_move = self.env['stock.move'].search([('id', '=', move.move_id.id)])
            move_move.write({'analytic_account_id': self.production_id.analytic_account_id.id})





