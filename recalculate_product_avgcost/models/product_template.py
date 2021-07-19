# -*- coding: utf-8 -*-
##############################################################################
#
#    SIE CENTER custom module for Odoo
#    Copyright (C) 2021
#    @author: @cyntiafelix
#
##############################################################################

from odoo import api, fields, models
from odoo.tools import float_is_zero
from odoo.exceptions import Warning, ValidationError

class MyProduct(models.Model):
    _inherit = 'product.template'

    def action_recalculate_avgcost(self):
        for product in self:
            log = []
            log.append("RECALCULO DE COSTO PROMEDIO Y VALUACION DE INVENTARIO")
            #Action applies only for average cost method
            if product.cost_method not in ('average'):
                product.message_post(body = ("El método de costo %s para el producto no aplica a esta acción"%product.cost_method))
                continue

            #Deleting all valuation lines for the product
            log.append("Las siguientes líneas de valoración y contabilidad fueron eliminadas")
            valuation_lines = self.env['stock.valuation.layer'].search([('product_id', '=', product.id)])
            account_moves_ids = []
            for valuation in valuation_lines:
                if (valuation.account_move_id):
                    account_moves_ids.append(valuation.account_move_id.id)
                log.append("--------------------------------------------------")
                log.append("Valoración Inventario: %s"%(valuation.description))
                log.append("Asiento Contable: %s"%(valuation.account_move_id.name))
            valuation_lines.sudo().unlink()

            #Unreconcile account moves before deleting
            account_moves = self.env['account.move'].search([('id', 'in', account_moves_ids)])
            for move in account_moves:
                if move.has_reconciled_entries:
                    for move_line in move.line_ids:
                        if move_line.reconciled:
                            reconcile_ids = [m.id for m in move_line.full_reconcile_id]
                            credit_ids = [m.id for m in move_line.matched_credit_ids]
                            debit_ids = [m.id for m in move_line.matched_debit_ids]
                            if len(reconcile_ids) > 0:
                                search_lines = self.env['account.full.reconcile'].search([('id', 'in', reconcile_ids)])
                                reconcile_lines = [c.reconciled_line_ids for c in search_lines]
                            elif len(credit_ids) > 0:
                                search_lines = self.env['account.partial.reconcile'].search([('id', 'in', credit_ids)])
                                reconcile_lines = [c.credit_move_id for c in search_lines]
                            elif len(debit_ids) > 0:
                                search_lines = self.env['account.partial.reconcile'].search([('id', 'in', debit_ids)])
                                reconcile_lines = [c.debit_move_id for c in search_lines]
                            for lines in reconcile_lines:
                                log.append("--------------------------------------------------")
                                log.append("Asientos Contables desconciliados: %s"%(', ').join([l.move_id.name for l in lines]))
                                lines.remove_move_reconcile()


            #Deleting account moves for the product
            account_moves._context['force_delete'] = True
            account_moves.sudo().unlink()

            log.append("<br/>")

            #Searching move lines for the product sorted by force_date
            log.append("Las siguientes transferencias fueron revaloradas siguiendo el orden de su fecha forzada")
            pick_lines = self.env['stock.picking'].search([('product_id', '=', product.id)], order='force_date')
            for pick in pick_lines:
                log.append("--------------------------------------------------")
                log.append("Referencia: %s"%pick.name)
                log.append("Estado: %s"%pick.state)
                log.append("Fecha Forzada: %s"%pick.force_date)
                #Creating new valuation for each move line
                for move_line in pick.move_line_ids:
                    if move_line.product_id.id != product.id:
                        continue
                    if move_line.state != 'done':
                        continue
                    move = move_line.move_id
                    rounding = move.product_id.uom_id.rounding
                    diff = move_line.qty_done
                    if float_is_zero(diff, precision_rounding=rounding):
                        continue
                    if move._is_in():
                        log.append("Tipo Movimiento: Entrada")
                    elif move._is_out():
                        log.append("Tipo Movimiento: Salida")
                    log.append("Cantidad: %s"%diff)
                    log.append("Precio Unitario: %s"%move._get_price_unit())
                    move_line.sudo()._create_correction_svl(move, diff)

            product.message_post(body = ("<br/>").join(log))
        return True
