from odoo import fields, models

class tableFields(models.Model):
    _name = "estate.property.type"
    _description = "modelo que define el tipo de propiedad"

    name = fields.Char('Tipo Propiedad',required = True)


