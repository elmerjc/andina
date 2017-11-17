# -*- coding: utf-8 -*-
from openerp import models, fields, api

class prenda_multiple_wizard(models.TransientModel):
	_name = 'wizard.prenda.multiple'
	_description = 'Agregar multiples prendas'
	
	area_id = fields.Many2one('andina.area', string='Area Operativa')
	lavado_line = fields.One2many('wizard.prenda.multiple.line', 'lavado_id', string='Prendas',  readonly=False)

	@api.one
	def add_multiple(self):
		active_id = self._context['active_id']

		for line in self.lavado_line:
			prenda = self.env['wizard.prenda.multiple.line'].prenda_id_change(line.prenda_id.id)
			val = {
				'name': '',
				'area_id': self.area_id.id,
				'cantidad': line.cantidad,
				'lavado_id': active_id,
				'prenda_id': line.prenda_id.id,
				'peso': prenda['value'].get('peso'),
				'precio': prenda['value'].get('precio'),
			}
			self.env['andina.lavado.industrial.line'].create(val)

class andina_lavado_industrial_line(models.TransientModel):
	_name = 'wizard.prenda.multiple.line'
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

	name = fields.Char('Description', default='')
	lavado_id = fields.Many2one('andina.lavado.industrial', string='Control del lavado', ondelete='cascade')
	prenda_id = fields.Many2one('andina.prenda', string='Prenda', ondelete='set null', change_default=True)
	precio = fields.Float('Precio', digits=(16,3), store=True, required=True)
	peso = fields.Float('Peso', digits=(16,3),  store=True, required=True)
	peso_subtotal = fields.Float('Peso Subtotal', digits=(16,3), store=True, readonly=True, compute='_compute_peso')
	precio_subtotal = fields.Float('Precio Subtotal', digits=(16,3), store=True, readonly=True, compute='_compute_precio')
	cantidad = fields.Integer('Cantidad', required=True, default=1)
	persona_id = fields.Many2many('andina.persona', 'andina_lavado_industrial_persona_rel', 'lavado_line_id', 'persona_id', 'Trabajadores')

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