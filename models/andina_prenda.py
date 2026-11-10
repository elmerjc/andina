# -*- coding: utf-8 -*-

from odoo import models, fields, api


class andina_prenda(models.Model):
    _name = 'andina.prenda'
    _description = "Prenda"
    _order = "name"

    name = fields.Char('Descripción')
    detalle = fields.Text('Detalle')
    peso = fields.Float(
        'Peso',
        digits=(16, 3)
    )
    precio = fields.Float(
        'Costo',
        digits=(16, 3)
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        readonly=True,
        default=lambda self: self.env.user)
    active = fields.Boolean(
        'Activo',
        default=True
    )

    _name_uniq = models.Constraint('UNIQUE (name, detalle)', 'La descripción debe ser unica!')
