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

class andina_prenda(osv.osv):
	_name = 'andina.prenda'
	_description = "Prenda"
	_order = "name"

	_columns = {
		'name': fields.char('Descripción', index=True),
		'detalle': fields.text('Detalle', index=True),
		'peso': fields.float('Peso', digits=(16, 3), store=True),
		'precio': fields.float('Costo', digits=(16, 3), store=True),
		'user_id' : fields.many2one('res.users', string='Responsable', track_visibility='onchange', readonly=True, default=lambda self: self.env.user),
		'active': fields.boolean('Activo', store=True, default=True),
	}

	_sql_constraints = [
		('name_uniq', 'unique(name,detalle)', 'La descripción debe ser unica!'),
	]