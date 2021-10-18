from odoo import fields, models, api, exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

class tableFields(models.Model):
    _name = "estate.property.offer"
    _description = "modelo que define las etiqueta de las ofertas hacia propiedad"

    price = fields.Float('Precio',required = True)
    status = fields.Selection(
        string = 'Estatus de la oferta',
        selection = [('aceptada','Aceptada'), ('rechazada','Rechazada')],
        copy = False
    )
    partner_id = fields.Many2one("res.partner", string="Comprador", required = True)
    property_id = fields.Many2one("estate.property", string="Propiedad", required = True)
    vality = fields.Integer("Validez (días)", default = 7)
    date_deadline = fields.Date("Fecha vencimiento", compute= "_compute_date_deadline", inverse= "_inverse_date_deadline")

    @api.depends("vality")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (datetime.now() + relativedelta(days=record.vality))

    def _inverse_date_deadline(self):
        for record in self:
            record.vality = (record.date_deadline - datetime.now().date()).days

    def action_accept_offer(self):
        for record in self:
            if ("aceptada" not in record.mapped('property_id.offer_ids.status')):
                print(record.mapped('property_id.offer_ids.status'))
                record.status = "aceptada"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
            else:
                raise exceptions.UserError("No puede aceptar más de una oferta.")

    def action_reject_offer(self):
        for record in self:
            record.status = "rechazada"