from odoo import fields, models

class tableFields(models.Model):
    _name = "estate.property.tag"
    _description = "modelo que define la etiqueta de la propiedad"

    name = fields.Char('Etiqueta Propiedad',required = True)
