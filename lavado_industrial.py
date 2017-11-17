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

class andina_lavado_industrial(osv.osv):
	_name = 'andina.lavado.industrial'
	_description = "Control del lavado industrial"
	_order = "date_recibido desc, turno desc"

	@api.one
	@api.depends('lavado_line', 'cobrar_por', 'precio_kilo')
	def _compute_totales(self):
		self.peso_total = sum(line.peso_subtotal for line in self.lavado_line)
		self.cantidad_total = sum(line.cantidad for line in self.lavado_line)
		if self.cobrar_por == 'kilo':
			self.precio_total = self.peso_total * self.precio_kilo
		else:
			self.precio_total = sum(line.precio_subtotal for line in self.lavado_line)

	_columns = {
		'name': fields.char('Referencia', index=True,  default=''),
		'comment': fields.text('Comentarios', store=True, readonly=True, copy=False),
		'date_recibido': fields.date('Fecha Recibido', required=True, index=True, readonly=True, states={'open': [('readonly', False)], 'done': [('readonly', False)]}),
		'date_entrega': fields.date('Fecha Entrega', index=True, readonly=True, states={'open': [('readonly', False)], 'done': [('readonly', False)]}),
		'lavado_line': fields.one2many('andina.lavado.industrial.line', 'lavado_id', string='Prendas para el lavado',  readonly=True, states={'open': [('readonly', False)], 'done': [('readonly', False)]}, copy=True),
		'precio_kilo': fields.float('Precio x Kilo', digits=(16,3), default=2.95, store=True, required=True, readonly=True, states={'open': [('readonly', False)], 'done': [('readonly', False)]}),
		'cobrar_por': fields.selection([('kilo', 'Kilo'), ('prenda', 'Prenda')], 'Cobrar por', default='kilo', required=True, readonly=True, states={'open': [('readonly', False)], 'done': [('readonly', False)]}),
		'peso_total': fields.float('Peso Total', digits=(16,3), store=True, readonly=True, compute='_compute_totales'),
		'precio_total': fields.float('Precio Total', digits=(16,3), store=True, readonly=True, compute='_compute_totales'),
		'cantidad_total': fields.integer('Cantidad de prendas', store=True, readonly=True, compute='_compute_totales'),
		'user_id' : fields.many2one('res.users', string='Responsable', track_visibility='onchange', readonly=True, default=lambda self: self.env.user),
		'state' : fields.selection([
			('open','Abierto'),
			('cancel','Cancelado'),
			('done','Realizado'),
			('close','Cerrado'),
			], string='Estado', index=True, readonly=True, default='open', track_visibility='onchange', copy=False),
		'turno': fields.selection([('A', 'A'), ('B', 'B'), ('C', 'C')], 'Turno', default='A', required=True, readonly=True, states={'open': [('readonly', False)], 'done': [('readonly', False)]}),
	}

	def action_done(self, cr, uid, ids, context=None):
		name = self.pool.get('ir.sequence').get(cr, uid, 'andina.lavado.industrial')
		self.write(cr, uid, ids, {'name': name, 'state': 'done'})
		return True

	def action_cancel(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state': 'cancel'})
		return True

	def action_open(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state': 'done'})
		return True

	def action_close(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state': 'close'})
		return True

class andina_lavado_industrial_line(osv.osv):
	_name = 'andina.lavado.industrial.line'
	_description = "Prendas para el lavado"
	_order = "lavado_id,id"

	@api.one
	@api.depends('peso', 'cantidad')
	def _compute_peso(self):
		self.peso_subtotal = self.peso * self.cantidad

	@api.one
	@api.depends('precio', 'cantidad')
	def _compute_precio(self):
		self.precio_subtotal = self.precio * self.cantidad

	_columns = {
		'name': fields.char('Description', default=''),
		'sequence': fields.integer('Secuencia', default=10),
		'lavado_id' : fields.many2one('andina.lavado.industrial', string='Control del lavado', ondelete='cascade'),
		'prenda_id': fields.many2one('andina.prenda', string='Prenda', ondelete='set null', change_default=True),
		'precio': fields.float('Precio', digits=(16,3), store=True, required=True),
		'peso': fields.float('Peso', digits=(16,3),  store=True, required=True),
		'peso_subtotal': fields.float('Peso Subtotal', digits=(16,3), store=True, readonly=True, compute='_compute_peso'),
		'precio_subtotal': fields.float('Precio Subtotal', digits=(16,3), store=True, readonly=True, compute='_compute_precio'),
		'cantidad': fields.integer('Cantidad', required=True, default=1),
		'persona_id' : fields.many2many('andina.persona', 'andina_lavado_industrial_persona_rel', 'lavado_line_id', 'persona_id', 'Trabajadores'),
		'area_id': fields.many2one('andina.area','Area Operativa', change_default=True),
		'name_control' : fields.char(related='lavado_id.name', string='Referencia', readonly=True),
		'date_recibido_control' : fields.date(related='lavado_id.date_recibido', string='Fecha Recibido', store=True, readonly=True),
		'date_entrega_control' : fields.date(related='lavado_id.date_entrega', string='Fecha Entrega', store=True, readonly=True),
		'area_id_control' : fields.integer('Area Operativa Related', store=True, readonly=True),
		'turno_control' : fields.related('lavado_id', 'turno', type='selection', selection=[('A', 'A'), ('B', 'B'), ('C', 'C')], store=True, readonly=True, string='Turno'),
	}

	def prenda_id_change(self, cr, uid, ids, prenda, context=None):
		context = context or {}
		prenda_obj = self.pool.get('andina.prenda')
		if not prenda:
			return {
				'value': {
					'peso': 0.000,
					'precio': 0.000,
				},
				'domain': {}
			}

		result = {}
		domain = {}
		prenda_obj = prenda_obj.browse(cr, uid, prenda, context=context)
		result['precio'] =  prenda_obj.precio
		result['peso'] =  prenda_obj.peso

		return {'value': result, 'domain': domain}

	@api.onchange('persona_id')
	def _count_persona(self):
		self.cantidad = len(self.persona_id)