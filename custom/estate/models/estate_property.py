#from datetime import datetime
#from typing_extensions import Required
#from xmlrpc.client import Boolean
from datetime import datetime
from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta
#from odoo.tools.float_utils import float_repr

class tableFields(models.Model):
    _name = "estate.property"
    _description = "modelo que define los campos de la tabla"

    name = fields.Char('Título',required = True)
    description = fields.Text('Descripción')
    postcode = fields.Char('Código Postal')
    date_availability = fields.Date('Disponible desde', copy = False, default = (datetime.now() + relativedelta(months=3)))
    expected_price = fields.Float('Precio esperado',required = True)
    selling_price = fields.Float('Precio de Venta', readonly = True, copy = False)
    bedrooms = fields.Integer('Dormitorios', default = 2)
    living_area = fields.Integer('Área vivienda (m²)')
    facades = fields.Integer('Fachadas')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Jardín')
    garden_area = fields.Integer('Área del Jardín (m²)')
    garden_orientation = fields.Selection(
        string = 'Orientación del Jardín',
        selection = [('Norte', 'norte'), ('Sur','sur'), ('Este', 'este'), ('Oeste', 'oeste')]
    )
    state = fields.Selection(
        string = 'Estado publicación',
        selection = [('nuevo','Nuevo'), ('cancelada','Cancelada'), ('vendida','Vendida'), ('oferta recibida','Oferta recibida')],
        default = 'nuevo',
        copy = False
    )
    property_type_id = fields.Many2one("estate.property.type", string="Tipo Propiedad", ondelete='set null')
    buyer_id = fields.Many2one("res.partner", string="Comprador", ondelete="set null", copy = False)
    seller_id = fields.Many2one("res.users", string="Vendedor", ondelete="set null", default = lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Etiqueta propiedad", ondelete='restrict')
    offer_ids = fields.One2many("estate.property.offer","property_id", string="Ofertas")
    total_area = fields.Float("Área total (m²)", compute = "_compute_area")
    best_price = fields.Float("Mejor Oferta", compute="_compute_best_offer")

    @api.depends("garden_area","living_area")
    def _compute_area(selft):
        for record in selft:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(selft):
        for record in selft:
            if(record.mapped('offer_ids.price')!=[]):
                record.best_price = max(record.mapped('offer_ids.price'))
            else:
                record.best_price = 0


    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden == 1):
            self.garden_area = 10
            self.garden_orientation = 'Norte'
        elif(self.garden == 0):
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold_property(self):
        for record in self:
            if (record.state != "cancelada"):
                record.state = "vendida"
            else:
                raise exceptions.UserError("No puede establecer como vendida una publicación que fué cancelada.")

    def action_cancel_property(self):
        for record in self:
            if (record.state != "vendida"):
                record.state = "cancelada"
            else:
                raise exceptions.UserError("No puede establecer como cancelda una publicación que ya fué vendida.")





