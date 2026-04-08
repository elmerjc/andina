# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.addons.arc_andina.models import andina_constantes

import logging
_logger = logging.getLogger(__name__)

class AndinaLavadoIndustrial(models.Model):
    _name = 'andina.lavado.industrial'
    _description = "Control de lavado industrial"
    _order = "name desc, fecha desc"

    # def _get_default_precio_kilo(self):
    #     return self.env['andina.config.settings'].sudo()._get_precio_kilo()

    name = fields.Char('Referencia',
        index=True,
        default='')
    comentarios = fields.Text('Comentarios',
        readonly=True,
        copy=False)
    fecha = fields.Date('Fecha')
    fecha_inicio = fields.Date('Fecha Inicio',
        required=True,
        readonly=True, 
        states={'open': [('readonly', False)], 'done': [('readonly', False)]})
    fecha_fin = fields.Date('Fecha Fin',
        required=True,
        readonly=True,
        states={'open': [('readonly', False)], 'done': [('readonly', False)]})
    lavado_line = fields.One2many(
        'andina.lavado.industrial.line',
        'lavado_id',
        string='Prendas para el lavado',
        readonly=True,
        copy=True,
        states={'open': [('readonly', False)], 'done': [('readonly', False)]})
    precio_kilo = fields.Float('Precio x Kilo',
        digits=(16,3),
        # default=_get_default_precio_kilo,
        store=True,
        required=True)
    cobrar_por = fields.Selection(
        [('kilo', 'Kilo'), ('prenda', 'Prenda')],
        'Cobrar por',
        default='kilo',
        required=True,
        readonly=True,
        states={'open': [('readonly', False)], 'done': [('readonly', False)]})
    peso_total = fields.Float('Peso Total',
        digits=(16,3),
        readonly=True,
        store=True,
        compute='_compute_totales')
    precio_total = fields.Float('Precio Total',
        digits=(16,3),
        readonly=True,
        store=True,
        compute='_compute_totales')
    cantidad_total = fields.Integer('Cantidad de prendas',
        readonly=True,
        store=True,
        compute='_compute_totales')
    cantidad_turnoa = fields.Integer('Cantidad de prendas del Turno A',
        readonly=True,
        store=True,
        compute='_compute_totales')
    cantidad_turnob = fields.Integer('Cantidad de prendas del Turno B',
        readonly=True,
        store=True,
        compute='_compute_totales')
    cantidad_turnoc = fields.Integer('Cantidad de prendas del Turno C',
        readonly=True,
        store=True,
        compute='_compute_totales')
    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        track_visibility='onchange',
        readonly=True,
        default=lambda self: self.env.user)
    state = fields.Selection(
        [('open','Abierto'), ('confirm', 'En progreso'), ('done','Realizado'), ('cancel','Cancelado'), ('close','Cerrado')],
        string='Estado',
        readonly=True,
        default='open',
        track_visibility='onchange',
        copy=False)
    is_parada = fields.Boolean('Turno Parada', default=False)
    # turno = fields.Selection(
    #     [('REGULAR', 'REGULAR'), ('PARADA', 'PARADA')],
    #     'Turno',
    #     default='REGULAR',
    #     required=True,
    #     readonly=True,
    #     states={'open': [('readonly', False)], 'done': [('readonly', False)]})
    area_id = fields.Many2one(
        'andina.area',
        'Area Operativa',
        change_default=True)
    gerencia_id = fields.Many2one(
        'andina.gerencia',
        'Gerencia',
        related='area_id.gerencia_id',
        store=True,
        readonly=True)
    wizard_id = fields.Integer(
        string="Importación")
    wizard_name = fields.Char(
        string="Referencia")   

    @api.depends(
        'lavado_line.p1a', 'lavado_line.p2a', 'lavado_line.p3a', 'lavado_line.p4a', 'lavado_line.p5a', 'lavado_line.p6a', 'lavado_line.p7a', 'lavado_line.p8a', 'lavado_line.p9a', 'lavado_line.p10a', 'lavado_line.p11a', 'lavado_line.p12a', 'lavado_line.p13a', 'lavado_line.p14a', 'lavado_line.p15a', 'lavado_line.p16a',
        'lavado_line.p1b', 'lavado_line.p2b', 'lavado_line.p3b', 'lavado_line.p4b', 'lavado_line.p5b', 'lavado_line.p6b', 'lavado_line.p7b', 'lavado_line.p8b', 'lavado_line.p9b', 'lavado_line.p10b', 'lavado_line.p11b', 'lavado_line.p12b', 'lavado_line.p13b', 'lavado_line.p14b', 'lavado_line.p15b', 'lavado_line.p16b',
        'lavado_line.p1c', 'lavado_line.p2c', 'lavado_line.p3c', 'lavado_line.p4c', 'lavado_line.p5c', 'lavado_line.p6c', 'lavado_line.p7c', 'lavado_line.p8c', 'lavado_line.p9c', 'lavado_line.p10c', 'lavado_line.p11c', 'lavado_line.p12c', 'lavado_line.p13c', 'lavado_line.p14c', 'lavado_line.p15c', 'lavado_line.p16c',
        'cobrar_por',
        'precio_kilo')
    def _compute_totales(self):
        for control in self:
            cantidad_prendas = []
            cantidad_prendas_a = []
            cantidad_prendas_b = []
            cantidad_prendas_c = []
            p1a_total = sum(line.p1a for line in control.lavado_line)
            cantidad_prendas.append(p1a_total)
            cantidad_prendas_a.append(p1a_total)
            p1b_total = sum(line.p1b for line in control.lavado_line)
            cantidad_prendas.append(p1b_total)
            cantidad_prendas_b.append(p1b_total)
            p1c_total = sum(line.p1c for line in control.lavado_line)
            cantidad_prendas.append(p1c_total)
            cantidad_prendas_c.append(p1c_total)
            p2a_total = sum(line.p2a for line in control.lavado_line)
            cantidad_prendas.append(p2a_total)
            cantidad_prendas_a.append(p2a_total)
            p2b_total = sum(line.p2b for line in control.lavado_line)
            cantidad_prendas.append(p2b_total)
            cantidad_prendas_b.append(p2b_total)
            p2c_total = sum(line.p2c for line in control.lavado_line)
            cantidad_prendas.append(p2c_total)
            cantidad_prendas_c.append(p2c_total)
            p3a_total = sum(line.p3a for line in control.lavado_line)
            cantidad_prendas.append(p3a_total)
            cantidad_prendas_a.append(p3a_total)
            p3b_total = sum(line.p3b for line in control.lavado_line)
            cantidad_prendas.append(p3b_total)
            cantidad_prendas_b.append(p3b_total)
            p3c_total = sum(line.p3c for line in control.lavado_line)
            cantidad_prendas.append(p3c_total)
            cantidad_prendas_c.append(p3c_total)
            p4a_total = sum(line.p4a for line in control.lavado_line)
            cantidad_prendas.append(p4a_total)
            cantidad_prendas_a.append(p4a_total)
            p4b_total = sum(line.p4b for line in control.lavado_line)
            cantidad_prendas.append(p4b_total)
            cantidad_prendas_b.append(p4b_total)
            p4c_total = sum(line.p4c for line in control.lavado_line)
            cantidad_prendas.append(p4c_total)
            cantidad_prendas_c.append(p4c_total)
            p5a_total = sum(line.p5a for line in control.lavado_line)
            cantidad_prendas.append(p5a_total)
            cantidad_prendas_a.append(p5a_total)
            p5b_total = sum(line.p5b for line in control.lavado_line)
            cantidad_prendas.append(p5b_total)
            cantidad_prendas_b.append(p5b_total)
            p5c_total = sum(line.p5c for line in control.lavado_line)
            cantidad_prendas.append(p5c_total)
            cantidad_prendas_c.append(p5c_total)
            p6a_total = sum(line.p6a for line in control.lavado_line)
            cantidad_prendas.append(p6a_total)
            cantidad_prendas_a.append(p6a_total)
            p6b_total = sum(line.p6b for line in control.lavado_line)
            cantidad_prendas.append(p6b_total)
            cantidad_prendas_b.append(p6b_total)
            p6c_total = sum(line.p6c for line in control.lavado_line)
            cantidad_prendas.append(p6c_total)
            cantidad_prendas_c.append(p6c_total)
            p7a_total = sum(line.p7a for line in control.lavado_line)
            cantidad_prendas.append(p7a_total)
            cantidad_prendas_a.append(p7a_total)
            p7b_total = sum(line.p7b for line in control.lavado_line)
            cantidad_prendas.append(p7b_total)
            cantidad_prendas_b.append(p7b_total)
            p7c_total = sum(line.p7c for line in control.lavado_line)
            cantidad_prendas.append(p7c_total)
            cantidad_prendas_c.append(p7c_total)
            p8a_total = sum(line.p8a for line in control.lavado_line)
            cantidad_prendas.append(p8a_total)
            cantidad_prendas_a.append(p8a_total)
            p8b_total = sum(line.p8b for line in control.lavado_line)
            cantidad_prendas.append(p8b_total)
            cantidad_prendas_b.append(p8b_total)
            p8c_total = sum(line.p8c for line in control.lavado_line)
            cantidad_prendas.append(p8c_total)
            cantidad_prendas_c.append(p8c_total)
            p9a_total = sum(line.p9a for line in control.lavado_line)
            cantidad_prendas.append(p9a_total)
            cantidad_prendas_a.append(p9a_total)
            p9b_total = sum(line.p9b for line in control.lavado_line)
            cantidad_prendas.append(p9b_total)
            cantidad_prendas_b.append(p9b_total)
            p9c_total = sum(line.p9c for line in control.lavado_line)
            cantidad_prendas.append(p9c_total)
            cantidad_prendas_c.append(p9c_total)
            p10a_total = sum(line.p10a for line in control.lavado_line)
            cantidad_prendas.append(p10a_total)
            cantidad_prendas_a.append(p10a_total)
            p10b_total = sum(line.p10b for line in control.lavado_line)
            cantidad_prendas.append(p10b_total)
            cantidad_prendas_b.append(p10b_total)
            p10c_total = sum(line.p10c for line in control.lavado_line)
            cantidad_prendas.append(p10c_total)
            cantidad_prendas_c.append(p10c_total)
            p11a_total = sum(line.p11a for line in control.lavado_line)
            cantidad_prendas.append(p11a_total)
            cantidad_prendas_a.append(p11a_total)
            p11b_total = sum(line.p11b for line in control.lavado_line)
            cantidad_prendas.append(p11b_total)
            cantidad_prendas_b.append(p11b_total)
            p11c_total = sum(line.p11c for line in control.lavado_line)
            cantidad_prendas.append(p11c_total)
            cantidad_prendas_c.append(p11c_total)
            p12a_total = sum(line.p12a for line in control.lavado_line)
            cantidad_prendas.append(p12a_total)
            cantidad_prendas_a.append(p12a_total)
            p12b_total = sum(line.p12b for line in control.lavado_line)
            cantidad_prendas.append(p12b_total)
            cantidad_prendas_b.append(p12b_total)
            p12c_total = sum(line.p12c for line in control.lavado_line)
            cantidad_prendas.append(p12c_total)
            cantidad_prendas_c.append(p12c_total)
            p13a_total = sum(line.p13a for line in control.lavado_line)
            cantidad_prendas.append(p13a_total)
            cantidad_prendas_a.append(p13a_total)
            p13b_total = sum(line.p13b for line in control.lavado_line)
            cantidad_prendas.append(p13b_total)
            cantidad_prendas_b.append(p13b_total)
            p13c_total = sum(line.p13c for line in control.lavado_line)
            cantidad_prendas.append(p13c_total)
            cantidad_prendas_c.append(p13c_total)
            p14a_total = sum(line.p14a for line in control.lavado_line)
            cantidad_prendas.append(p14a_total)
            cantidad_prendas_a.append(p14a_total)
            p14b_total = sum(line.p14b for line in control.lavado_line)
            cantidad_prendas.append(p14b_total)
            cantidad_prendas_b.append(p14b_total)
            p14c_total = sum(line.p14c for line in control.lavado_line)
            cantidad_prendas.append(p14c_total)
            cantidad_prendas_c.append(p14c_total)
            p15a_total = sum(line.p15a for line in control.lavado_line)
            cantidad_prendas.append(p15a_total)
            cantidad_prendas_a.append(p15a_total)
            p15b_total = sum(line.p15b for line in control.lavado_line)
            cantidad_prendas.append(p15b_total)
            cantidad_prendas_b.append(p15b_total)
            p15c_total = sum(line.p15c for line in control.lavado_line)
            cantidad_prendas.append(p15c_total)
            cantidad_prendas_c.append(p15c_total)
            p16a_total = sum(line.p16a for line in control.lavado_line)
            cantidad_prendas.append(p16a_total)
            cantidad_prendas_a.append(p16a_total)
            p16b_total = sum(line.p16b for line in control.lavado_line)
            cantidad_prendas.append(p16b_total)
            cantidad_prendas_b.append(p16b_total)
            p16c_total = sum(line.p16c for line in control.lavado_line)
            cantidad_prendas.append(p16c_total)
            cantidad_prendas_c.append(p16c_total)
            
            control.cantidad_total = sum(p for p in cantidad_prendas)
            control.cantidad_turnoa = sum(p for p in cantidad_prendas_a)
            control.cantidad_turnob = sum(p for p in cantidad_prendas_b)
            control.cantidad_turnoc = sum(p for p in cantidad_prendas_c)
            control.peso_total = sum(line.peso_subtotal for line in control.lavado_line)
            if control.cobrar_por == 'kilo':
                control.precio_total = control.peso_total * control.precio_kilo
            else:
                control.precio_total = sum(line.precio_subtotal for line in control.lavado_line)

    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True

    def action_open(self):
        self.write({'state': 'done'})
        return True

    def action_close(self):
        self.write({'state': 'close'})
        return True

    def action_start(self):
        self.ensure_one()
        self._action_start()
        return self.action_open_control_lines()

    def _action_start(self):
        for control in self:
            if control.state != 'open':
                continue
            vals = {
                'state': 'confirm',
                'fecha': fields.Datetime.now()
            }
            self.env['andina.lavado.industrial.line'].create(control._get_control_lines_values())
            control.write(vals)

    def action_open_control_lines(self):
        self.ensure_one()
        action = {
            'name': 'Detalle del Control',
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('arc_andina.view_andina_lavado_industrial_line_tree').id, 'tree')],
            'view_mode': 'tree',
            'res_model': 'andina.lavado.industrial.line',
        }
        context = {
            'default_is_editable': True,
            'default_lavado_id': self.id,
        }
        # Define domains and context
        domain = [
            ('lavado_id', '=', self.id)
        ]

        action['context'] = context
        action['domain'] = domain
        return action

    def action_ver_detalle(self):
        self.ensure_one()
        domain = [('lavado_id', '=', self.id)]
        action = {
            'name': 'Detalle del Control',
            'type': 'ir.actions.act_window',
            'res_model': 'andina.lavado.industrial.line',
            # 'views': [(self.env.ref('arc_andina.view_andina_lavado_industrial_line_tree').id, 'tree')],
            'view_type': 'list',
            'view_mode': 'list',
            'domain': domain,
        }
        _logger.info('ACTION DETALLE : ===== %s' % action)
        return action

    def _get_control_lines_values(self):
        vals = []
        # tz = pytz.timezone('America/Lima')
        # fecha_inicio = fields.Datetime.from_string(self.fecha_inicio)
        # fecha_fin = fields.Datetime.from_string(self.fecha_fin)

        # fecha_inicio_tz = fields.Datetime.to_string(tz.localize(fecha_inicio, is_dst=None) - timedelta(hours=5))
        # fecha_fin_tz = fields.Datetime.to_string(tz.localize(fecha_fin, is_dst=None) - timedelta(hours=5))
        dias = (self.fecha_fin - self.fecha_inicio).days
        lista_fechas = [self.fecha_inicio + timedelta(days=x) for x in range(dias + 1)]

        for fecha in lista_fechas:
            rows = {}
            rows['fecha'] = fecha
            rows['lavado_id'] = self.id
            vals.append(rows)
        # _logger.info('CREAR DETALLE : VALS ===== %s' % vals)
        return vals

    #@api.multi
    #def ga_orden_print(self):
    #   return self.env.ref('andina_lavado.action_report_ga_orden').report_action(self)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('andina.lavado.industrial')
        vals['state'] = 'open'
        result = super(AndinaLavadoIndustrial, self).create(vals)
        return result

class AndinaLavadoIndustrialLine(models.Model):
    _name = 'andina.lavado.industrial.line'
    _description = "Prendas para el lavado"
    _order = "lavado_id, id"

    name = fields.Char('Description', default='')
    sequence = fields.Integer('Secuencia', default=10)
    lavado_id = fields.Many2one('andina.lavado.industrial', string='Control del lavado', ondelete='cascade')
    fecha = fields.Date('Fecha', required=True, readonly=True, states={'open': [('readonly', False)], 'done': [('readonly', False)]})
    p1a = fields.Integer('CAPUCHON-CHOMPA', default=0)
    p1b = fields.Integer('CAPUCHON-CHOMPA', default=0)
    p1c = fields.Integer('CAPUCHON-CHOMPA', default=0)
    p2a = fields.Integer('CASACA CORTA', default=0)
    p2b = fields.Integer('CASACA CORTA', default=0)
    p2c = fields.Integer('CASACA CORTA', default=0)
    p3a = fields.Integer('CASACA CUERO (SOLDADOR)', default=0)
    p3b = fields.Integer('CASACA CUERO (SOLDADOR)', default=0)
    p3c = fields.Integer('CASACA CUERO (SOLDADOR)', default=0)
    p4a = fields.Integer('CASACA DE LONA', default=0)
    p4b = fields.Integer('CASACA DE LONA', default=0)
    p4c = fields.Integer('CASACA DE LONA', default=0)
    p5a = fields.Integer('CHALECO DE SEGURIDAD', default=0)
    p5b = fields.Integer('CHALECO DE SEGURIDAD', default=0)
    p5c = fields.Integer('CHALECO DE SEGURIDAD', default=0)
    p6a = fields.Integer('ESCARPINES', default=0)
    p6b = fields.Integer('ESCARPINES', default=0)
    p6c = fields.Integer('ESCARPINES', default=0)
    p7a = fields.Integer('MAMELUCO', default=0)
    p7b = fields.Integer('MAMELUCO', default=0)
    p7c = fields.Integer('MAMELUCO', default=0)
    p8a = fields.Integer('MANDILES CON BROCHES SIN PERCHERA', default=0)
    p8b = fields.Integer('MANDILES CON BROCHES SIN PERCHERA', default=0)
    p8c = fields.Integer('MANDILES CON BROCHES SIN PERCHERA', default=0)
    p9a = fields.Integer('MANDILES CON HEBILLA Y PERCHERA', default=0)
    p9b = fields.Integer('MANDILES CON HEBILLA Y PERCHERA', default=0)
    p9c = fields.Integer('MANDILES CON HEBILLA Y PERCHERA', default=0)
    p10a = fields.Integer('MANDILES CON HEBILLA SIN PERCHERA', default=0)
    p10b = fields.Integer('MANDILES CON HEBILLA SIN PERCHERA', default=0)
    p10c = fields.Integer('MANDILES CON HEBILLA SIN PERCHERA', default=0)
    p11a = fields.Integer('MANDILES LONA CUERO', default=0)
    p11b = fields.Integer('MANDILES LONA CUERO', default=0)
    p11c = fields.Integer('MANDILES LONA CUERO', default=0)
    p12a = fields.Integer('PANTALONES DE CUERO (SOLDADOR)', default=0)
    p12b = fields.Integer('PANTALONES DE CUERO (SOLDADOR)', default=0)
    p12c = fields.Integer('PANTALONES DE CUERO (SOLDADOR)', default=0)
    p13a = fields.Integer('PANTALON DE LONA', default=0)
    p13b = fields.Integer('PANTALON DE LONA', default=0)
    p13c = fields.Integer('PANTALON DE LONA', default=0)
    p14a = fields.Integer('CASACA Y PANT. IMPERMEABLE (ANTIACIDOS)', default=0)
    p14b = fields.Integer('CASACA Y PANT. IMPERMEABLE (ANTIACIDOS)', default=0)
    p14c = fields.Integer('CASACA Y PANT. IMPERMEABLE (ANTIACIDOS)', default=0)
    p15a = fields.Integer('GUANTES CUERO PANTUFLAS GORRO', default=0)
    p15b = fields.Integer('GUANTES CUERO PANTUFLAS GORRO', default=0)
    p15c = fields.Integer('GUANTES CUERO PANTUFLAS GORRO', default=0)
    p16a = fields.Integer('CAMISA PANTALON', default=0)
    p16b = fields.Integer('CAMISA PANTALON', default=0)
    p16c = fields.Integer('CAMISA PANTALON', default=0)
    cantidad_subtotal = fields.Integer('Cantidad Subtotal',
        readonly=True,
        store=True,
        compute='_compute_subtotal')
    peso_subtotal = fields.Float('Peso Subtotal', 
        digits=(16,3),
        readonly=True,
        store=True,
        compute='_compute_subtotal')
    is_editable = fields.Boolean("Editable", default=True)
    state = fields.Selection('Estado', 
        related='lavado_id.state',
        store=True)
    name_control = fields.Char(
        related='lavado_id.name',
        string='Referencia',
        store=True,
        readonly=True)
    is_parada = fields.Boolean(
        related='lavado_id.is_parada',
        string='Turno Parada',
        store=True,
        readonly=True)
    area_id = fields.Many2one(
        'andina.area',
        'Area Operativa',
        related='lavado_id.area_id',
        store=True,
        readonly=True)
    gerencia_id = fields.Many2one(
        'andina.gerencia',
        'Gerencia',
        related='lavado_id.gerencia_id',
        store=True,
        readonly=True)

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
