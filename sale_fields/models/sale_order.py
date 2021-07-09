# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Campos para cotización
    condiciones_entrega = fields.Selection(selection=[('inmediata', 'Entrega Inmediata'),('programa', 'En base a programa')])
    lugar_entrega = fields.Char('Lugar de Entrega')
    datos_fact = fields.Text('Datos Facturación')
    desc_col = fields.Char('Descuento / Columna')
    obs = fields.Text('Observaciones')
    tiempo_entrega = fields.Text('Tiempo de entrega')
    temperaturas = fields.Text('Temperaturas')
    template_id = fields.Many2one('data.template.sale','Plantilla de Cotización')
    tipo_cambio = fields.Char('Tipo de Cambio')

    #Campos para Licitaciones
    licitacion = fields.Char('No. de Licitación')
    organismo = fields.Char('Organismo')
    obra = fields.Text('Obra')


    #Campos de Contacto Cotización
    contact_name = fields.Char('Contacto', tracking=30)
    partner_name = fields.Char('Empresa', tracking=20, index=True)
    function = fields.Char('Puesto de Trabajo')
    title = fields.Many2one('res.partner.title', string='Titulo')
    email_from = fields.Char('Email', tracking=40, index=True, inverse='_inverse_email_from', readonly=False, store=True)
    phone = fields.Char('Teléfono', tracking=50, inverse='_inverse_phone', readonly=False, store=True)
    mobile = fields.Char('Móvil')
    phone_mobile_search = fields.Char('Phone/Mobile', store=False, search='_search_phone_mobile_search')
    phone_state = fields.Selection([
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect')], string='Phone Quality', store=True)
    email_state = fields.Selection([
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect')], string='Email Quality', store=True)
    website = fields.Char('Website', index=True, help="Website of the contact")
    # Address fields
    street = fields.Char('Calle')
    street2 = fields.Char('Street2')
    zip = fields.Char('CP', change_default=True)
    city = fields.Char('Ciudad')
    state_id = fields.Many2one("res.country.state", string='Estado', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='País')


    def _inverse_email_from(self):
        for lead in self:
            if lead.partner_id and lead.email_from != lead.partner_id.email:
                lead.partner_id.email = lead.email_from

    def _inverse_phone(self):
        for lead in self:
            if lead.partner_id and lead.phone != lead.partner_id.phone:
                lead.partner_id.phone = lead.phone
    


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_parte_relacionada = fields.Boolean('Partes Relacionadas')

class SaleOrder(models.Model):
    _inherit = 'res.partner.bank'

    show_crm = fields.Boolean('Mostrar en CRM', default=False)


