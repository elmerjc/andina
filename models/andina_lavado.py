# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.addons.andina.models import andina_constantes

import logging
_logger = logging.getLogger(__name__)


class AndinaLavadoIndustrial(models.Model):
    _name = 'andina.lavado.industrial'
    _description = "Control de lavado industrial"
    _order = "name desc, fecha desc"

    # def _get_default_precio_kilo(self):
    #     return self.env['andina.config.settings'].sudo()._get_precio_kilo()

    name = fields.Char(
        'Referencia',
        index=True,
        default=''
    )
    comentarios = fields.Text(
        'Comentarios',
        readonly=True,
        copy=False
    )
    fecha = fields.Date('Fecha')
    fecha_inicio = fields.Date(
        'Fecha Inicio',
        required=True,
        readonly=True,
        states={'open': [('readonly', False)], 'done': [('readonly', False)]}
    )
    fecha_fin = fields.Date(
        'Fecha Fin',
        required=True,
        readonly=True,
        states={'open': [('readonly', False)], 'done': [('readonly', False)]}
    )
    lavado_line = fields.One2many(
        'andina.lavado.industrial.line',
        'lavado_id',
        string='Prendas para el lavado',
        readonly=True,
        copy=True,
        states={'open': [('readonly', False)], 'done': [('readonly', False)]}
    )
    precio_kilo = fields.Float(
        'Precio x Kilo',
        digits=(16, 3),
        # default=_get_default_precio_kilo,
        store=True,
        required=True
    )
    cobrar_por = fields.Selection(
        [('kilo', 'Kilo'), ('prenda', 'Prenda')],
        'Cobrar por',
        default='kilo',
        required=True,
        readonly=True,
        states={'open': [('readonly', False)], 'done': [('readonly', False)]})
    peso_total = fields.Float(
        'Peso Total',
        digits=(16, 3),
        readonly=True,
        store=True,
        compute='_compute_totales'
    )
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

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('andina.lavado.industrial')
        vals['state'] = 'open'
        result = super(AndinaLavadoIndustrial, self).create(vals)
        return result
