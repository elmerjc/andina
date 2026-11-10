# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AndinaGerencia(models.Model):
    _name = "andina.gerencia"
    _description = "Gerencias donde pertencen las areas operativas"
    _order = 'name'

    name = fields.Char('Gerencia', required=True)
    
    _name_uniq = models.Constraint('UNIQUE (name)', 'La gerencia debe ser unico!')
