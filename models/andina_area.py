# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AndinaGerencia(models.Model):
	_name = "andina.gerencia"
	_description = "Gerencias donde pertencen las areas operativas"
	_order = 'name'

	name = fields.Char('Gerencia', required=True)
	
	_sql_constraints = [
		('name_uniq', 'unique(name)', 'La gerencia debe ser unico!'),
	]

class AndinaArea(models.Model):
	_name = "andina.area"
	_description = "Area Operativa (taller)"
	_order = 'name'
	
	name = fields.Char('Area Operativa', required=True)
	descripcion = fields.Char('Descripción')
	tipo = fields.Selection([('normal', 'Normal'), ('especial', 'Especial')], 'Tipo', default='normal', required=True)
	gerencia_id = fields.Many2one('andina.gerencia', 'Gerencia', required=True)

	_sql_constraints = [
		('name_uniq', 'unique(name)', 'El area operativa debe ser unico!'),
	]