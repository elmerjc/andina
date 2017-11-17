# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 S&C (<http://arc.pe>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import api
from openerp.osv import osv, fields, expression
import openerp.addons.decimal_precision as dp

class andina_gerencia(osv.osv):
	_name = "andina.gerencia"
	_description = "Gerencias donde pertencen las areas operativas"
	_order = 'name'

	_columns = {
		'name': fields.char('Gerencia', required=True),
	}

	_sql_constraints = [
		('name_uniq', 'unique(name)', 'La gerencia debe ser unico!'),
	]

class andina_area(osv.osv):
	_name = "andina.area"
	_description = "Area Operativa (taller)"
	_order = 'name'
	
	_columns = {
		'name': fields.char('Area Operativa', required=True),
		'descripcion': fields.char('Descripción'),
		'tipo': fields.selection([('normal', 'Normal'), ('especial', 'Especial')], 'Tipo', default='normal', required=True),
		'gerencia_id': fields.many2one('andina.gerencia', 'Gerencia', required=True),
	}

	_sql_constraints = [
		('name_uniq', 'unique(name)', 'El area operativa debe ser unico!'),
	]