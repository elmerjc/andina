# -*- coding: utf-8 -*-

from odoo import models, fields, api

class andina_prenda(models.Model):
    _name = 'andina.prenda'
    _description = "Prenda"
    _order = "name"

    name = fields.Char('Descripción')
    detalle = fields.Text('Detalle')
    peso = fields.Float('Peso', 
        digits=(16, 3))
    precio = fields.Float('Costo',
        digits=(16, 3))
    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        track_visibility='onchange',
        readonly=True,
        default=lambda self: self.env.user)
    active = fields.Boolean('Activo',
        default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name,detalle)', 'La descripción debe ser unica!'),
    ]