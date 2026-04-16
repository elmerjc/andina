# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api
from odoo.addons.andina.models import andina_constantes

_logger = logging.getLogger(__name__)


class AndinaLavadoIndustrialLine(models.Model):
    _name = 'andina.lavado.industrial.line'
    _description = "Prendas para el lavado"
    _order = "lavado_id, id"

    name = fields.Char(string='Description', default='')
    sequence = fields.Integer(string='Secuencia', default=10)
    lavado_id = fields.Many2one(
        'andina.lavado.industrial',
        string='Control del lavado',
        ondelete='cascade'
    )
    fecha = fields.Date(
        string='Fecha',
        required=True,
        readonly=True,
        states={'open': [('readonly', False)], 'done': [('readonly', False)]}
    )
    p1a = fields.Integer(string='CAPUCHON-CHOMPA', default=0)
    p1b = fields.Integer(string='CAPUCHON-CHOMPA', default=0)
    p1c = fields.Integer(string='CAPUCHON-CHOMPA', default=0)
    p2a = fields.Integer(string='CASACA CORTA', default=0)
    p2b = fields.Integer(string='CASACA CORTA', default=0)
    p2c = fields.Integer(string='CASACA CORTA', default=0)
    p3a = fields.Integer(string='CASACA CUERO (SOLDADOR)', default=0)
    p3b = fields.Integer(string='CASACA CUERO (SOLDADOR)', default=0)
    p3c = fields.Integer(string='CASACA CUERO (SOLDADOR)', default=0)
    p4a = fields.Integer(string='CASACA DE LONA', default=0)
    p4b = fields.Integer(string='CASACA DE LONA', default=0)
    p4c = fields.Integer(string='CASACA DE LONA', default=0)
    p5a = fields.Integer(string='CHALECO DE SEGURIDAD', default=0)
    p5b = fields.Integer(string='CHALECO DE SEGURIDAD', default=0)
    p5c = fields.Integer(string='CHALECO DE SEGURIDAD', default=0)
    p6a = fields.Integer(string='ESCARPINES', default=0)
    p6b = fields.Integer(string='ESCARPINES', default=0)
    p6c = fields.Integer(string='ESCARPINES', default=0)
    p7a = fields.Integer(string='MAMELUCO', default=0)
    p7b = fields.Integer(string='MAMELUCO', default=0)
    p7c = fields.Integer(string='MAMELUCO', default=0)
    p8a = fields.Integer(string='MANDILES CON BROCHES SIN PERCHERA', default=0)
    p8b = fields.Integer(string='MANDILES CON BROCHES SIN PERCHERA', default=0)
    p8c = fields.Integer(string='MANDILES CON BROCHES SIN PERCHERA', default=0)
    p9a = fields.Integer(string='MANDILES CON HEBILLA Y PERCHERA', default=0)
    p9b = fields.Integer(string='MANDILES CON HEBILLA Y PERCHERA', default=0)
    p9c = fields.Integer(string='MANDILES CON HEBILLA Y PERCHERA', default=0)
    p10a = fields.Integer(string='MANDILES CON HEBILLA SIN PERCHERA', default=0)
    p10b = fields.Integer(string='MANDILES CON HEBILLA SIN PERCHERA', default=0)
    p10c = fields.Integer(string='MANDILES CON HEBILLA SIN PERCHERA', default=0)
    p11a = fields.Integer(string='MANDILES LONA CUERO', default=0)
    p11b = fields.Integer(string='MANDILES LONA CUERO', default=0)
    p11c = fields.Integer(string='MANDILES LONA CUERO', default=0)
    p12a = fields.Integer(string='PANTALONES DE CUERO (SOLDADOR)', default=0)
    p12b = fields.Integer(string='PANTALONES DE CUERO (SOLDADOR)', default=0)
    p12c = fields.Integer(string='PANTALONES DE CUERO (SOLDADOR)', default=0)
    p13a = fields.Integer(string='PANTALON DE LONA', default=0)
    p13b = fields.Integer(string='PANTALON DE LONA', default=0)
    p13c = fields.Integer(string='PANTALON DE LONA', default=0)
    p14a = fields.Integer(string='CASACA Y PANT. IMPERMEABLE (ANTIACIDOS)', default=0)
    p14b = fields.Integer(string='CASACA Y PANT. IMPERMEABLE (ANTIACIDOS)', default=0)
    p14c = fields.Integer(string='CASACA Y PANT. IMPERMEABLE (ANTIACIDOS)', default=0)
    p15a = fields.Integer(string='GUANTES CUERO PANTUFLAS GORRO', default=0)
    p15b = fields.Integer(string='GUANTES CUERO PANTUFLAS GORRO', default=0)
    p15c = fields.Integer(string='GUANTES CUERO PANTUFLAS GORRO', default=0)
    p16a = fields.Integer(string='CAMISA PANTALON', default=0)
    p16b = fields.Integer(string='CAMISA PANTALON', default=0)
    p16c = fields.Integer(string='CAMISA PANTALON', default=0)
    cantidad_subtotal = fields.Integer(
        string='Cantidad Subtotal',
        readonly=True,
        store=True,
        compute='_compute_subtotal'
    )
    peso_subtotal = fields.Float(
        string='Peso Subtotal',
        digits=(16, 3),
        readonly=True,
        store=True,
        compute='_compute_subtotal'
    )
    is_editable = fields.Boolean("Editable", default=True)
    state = fields.Selection(
        string='Estado',
        related='lavado_id.state',
        store=True
    )
    name_control = fields.Char(
        related='lavado_id.name',
        string='Referencia',
        store=True,
        readonly=True
    )
    is_parada = fields.Boolean(
        related='lavado_id.is_parada',
        string='Turno Parada',
        store=True,
        readonly=True
    )
    area_id = fields.Many2one(
        'andina.area',
        string='Area Operativa',
        related='lavado_id.area_id',
        store=True,
        readonly=True
    )
    gerencia_id = fields.Many2one(
        'andina.gerencia',
        string='Gerencia',
        related='lavado_id.gerencia_id',
        store=True,
        readonly=True
    )

    @api.depends(
        'p1a', 'p2a', 'p3a', 'p4a', 'p5a', 'p6a', 'p7a', 'p8a', 'p9a', 'p10a', 'p11a', 'p12a', 'p13a', 'p14a', 'p15a', 'p16a',
        'p1b', 'p2b', 'p3b', 'p4b', 'p5b', 'p6b', 'p7b', 'p8b', 'p9b', 'p10b', 'p11b', 'p12b', 'p13b', 'p14b', 'p15b', 'p16b',
        'p1c', 'p2c', 'p3c', 'p4c', 'p5c', 'p6c', 'p7c', 'p8c', 'p9c', 'p10c', 'p11c', 'p12c', 'p13c', 'p14c', 'p15c', 'p16c',
    )
    def _compute_subtotal(self):
        pesos = andina_constantes.PesoPrendas
        for detalle in self:
            total_peso = 0.000
            total_cantidad = 0
            total_peso += detalle.p1a * pesos.p1.value
            total_cantidad += detalle.p1a
            total_peso += detalle.p1b * pesos.p1.value
            total_cantidad += detalle.p1b
            total_peso += detalle.p1c * pesos.p1.value
            total_cantidad += detalle.p1c
            total_peso += detalle.p2a * pesos.p2.value
            total_cantidad += detalle.p2a
            total_peso += detalle.p2b * pesos.p2.value
            total_cantidad += detalle.p2b
            total_peso += detalle.p2c * pesos.p2.value
            total_cantidad += detalle.p2c
            total_peso += detalle.p3a * pesos.p3.value
            total_cantidad += detalle.p3a
            total_peso += detalle.p3b * pesos.p3.value
            total_cantidad += detalle.p3b
            total_peso += detalle.p3c * pesos.p3.value
            total_cantidad += detalle.p3c
            total_peso += detalle.p4a * pesos.p4.value
            total_cantidad += detalle.p4a
            total_peso += detalle.p4b * pesos.p4.value
            total_cantidad += detalle.p4b
            total_peso += detalle.p4c * pesos.p4.value
            total_cantidad += detalle.p4c
            total_peso += detalle.p5a * pesos.p5.value
            total_cantidad += detalle.p5a
            total_peso += detalle.p5b * pesos.p5.value
            total_cantidad += detalle.p5b
            total_peso += detalle.p5c * pesos.p5.value
            total_cantidad += detalle.p5c
            total_peso += detalle.p6a * pesos.p6.value
            total_cantidad += detalle.p6a
            total_peso += detalle.p6b * pesos.p6.value
            total_cantidad += detalle.p6b
            total_peso += detalle.p6c * pesos.p6.value
            total_cantidad += detalle.p6c
            total_peso += detalle.p7a * pesos.p7.value
            total_cantidad += detalle.p7a
            total_peso += detalle.p7b * pesos.p7.value
            total_cantidad += detalle.p7b
            total_peso += detalle.p7c * pesos.p7.value
            total_cantidad += detalle.p7c
            total_peso += detalle.p8a * pesos.p8.value
            total_cantidad += detalle.p8a
            total_peso += detalle.p8b * pesos.p8.value
            total_cantidad += detalle.p8b
            total_peso += detalle.p8c * pesos.p8.value
            total_cantidad += detalle.p8c
            total_peso += detalle.p9a * pesos.p9.value
            total_cantidad += detalle.p9a
            total_peso += detalle.p9b * pesos.p9.value
            total_cantidad += detalle.p9b
            total_peso += detalle.p9c * pesos.p9.value
            total_cantidad += detalle.p9c
            total_peso += detalle.p10a * pesos.p10.value
            total_cantidad += detalle.p10a
            total_peso += detalle.p10b * pesos.p10.value
            total_cantidad += detalle.p10b
            total_peso += detalle.p10c * pesos.p10.value
            total_cantidad += detalle.p10c
            total_peso += detalle.p11a * pesos.p11.value
            total_cantidad += detalle.p11a
            total_peso += detalle.p11b * pesos.p11.value
            total_cantidad += detalle.p11b
            total_peso += detalle.p11c * pesos.p11.value
            total_cantidad += detalle.p11c
            total_peso += detalle.p12a * pesos.p12.value
            total_cantidad += detalle.p12a
            total_peso += detalle.p12b * pesos.p12.value
            total_cantidad += detalle.p12b
            total_peso += detalle.p12c * pesos.p12.value
            total_cantidad += detalle.p12c
            total_peso += detalle.p13a * pesos.p13.value
            total_cantidad += detalle.p13a
            total_peso += detalle.p13b * pesos.p13.value
            total_cantidad += detalle.p13b
            total_peso += detalle.p13c * pesos.p13.value
            total_cantidad += detalle.p13c
            total_peso += detalle.p14a * pesos.p14.value
            total_cantidad += detalle.p14a
            total_peso += detalle.p14b * pesos.p14.value
            total_cantidad += detalle.p14b
            total_peso += detalle.p14c * pesos.p14.value
            total_cantidad += detalle.p14c
            total_peso += detalle.p15a * pesos.p15.value
            total_cantidad += detalle.p15a
            total_peso += detalle.p15b * pesos.p15.value
            total_cantidad += detalle.p15b
            total_peso += detalle.p15c * pesos.p15.value
            total_cantidad += detalle.p15c
            total_peso += detalle.p16a * pesos.p16.value
            total_cantidad += detalle.p16a
            total_peso += detalle.p16b * pesos.p16.value
            total_cantidad += detalle.p16b
            total_peso += detalle.p16c * pesos.p16.value
            total_cantidad += detalle.p16c
            
            detalle.cantidad_subtotal = total_cantidad
            detalle.peso_subtotal = total_peso
