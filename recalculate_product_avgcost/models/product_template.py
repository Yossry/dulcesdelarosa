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
            #Action applies only for average cost method
            if product.cost_method not in ('average'):
                product.message_post(body = ('El método de costo %s para el producto no aplica a esta acción'%product.cost_method))
                continue

            #Deleting all valuation lines for the product (it should delete also account moves in cascade)
            log.append("VALORACIONES")
            log.append("Las siguientes líneas de valoración y contabilidad fueron eliminadas")
            valuation_lines = self.env['stock.valuation.layer'].search([('product_id', '=', product.id)])
            account_ids = []
            for valuation in valuation_lines:
                if (valuation.account_move_id): account_ids.append(valuation.account_move_id.id)
                log.append("""Referencia Valoración Inventario:%s, Referencia Contabilidad:%s"""
                %(valuation.display_name, valuation.account_move_id.name))
            valuation_lines.sudo().unlink()
            account_lines = self.env['account.move'].search([('id', 'in', account_ids)])
            account_lines._context['force_delete'] = True
            account_lines.sudo().unlink()

            log.append("<br/>")

            #Searching move lines for the product sorted by force_date
            log.append("TRANSFERENCIAS")
            log.append("Las siguientes transferencias fueron revaloradas siguiendo el orden de su fecha forzada")
            pick_lines = self.env['stock.picking'].search([('product_id', '=', product.id)], order='force_date')
            for pick in pick_lines:
                log.append("""ID:%s, Referencia:%s, Estado:%s, Fecha Forzada:%s, Movimientos:%s"""
                %(pick.id, pick.name, pick.state, pick.force_date, [p.reference for p in pick.move_line_ids]))
                #Creating new valuation for each move line
                for move_line in pick.move_line_ids:
                    if move_line.state != 'done':
                        continue
                    move = move_line.move_id
                    rounding = move.product_id.uom_id.rounding
                    diff = move_line.qty_done
                    if float_is_zero(diff, precision_rounding=rounding):
                        continue
                    if move._is_in():
                        log.append('Movimiento de Entrada')
                    elif move._is_out():
                        log.append('Movimiento de Salida')
                    log.append('Cantidad %s'%diff)
                    log.append('Precio Unitario %s'%move._get_price_unit())
                    move_line.sudo()._create_correction_svl(move, diff)

            product.message_post(body = ('<br/>').join(log))
        return True
