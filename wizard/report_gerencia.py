# -*- coding: utf-8 -*-

import time
import pytz
from datetime import datetime, date, timedelta

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.exceptions import UserError
from odoo.addons.arc_andina.models import andina_constantes

class AndinaReportGerencia(models.TransientModel):
    _name = 'andina.report.gerencia'
    _description = 'Reporte por Gerencia'
    
    # def _get_default_precio_kilo(self):
    #     return self.env['andina.config.settings'].sudo()._get_precio_kilo()

    def get_date_utc(self):
        if self.env.user.partner_id.tz:
            user_time_zone = pytz.timezone(self.env.user.partner_id.tz)
        else:
            user_time_zone = pytz.timezone('America/Lima')
        now = datetime.now(user_time_zone)
        return now.date()

    fecha_inicio = fields.Date('Desde', required=True, default=get_date_utc)
    fecha_fin = fields.Date('Hasta', required=True, default=get_date_utc)
    titulo = fields.Char('Titulo')
    precio_kilo = fields.Float('Precio por Kilo', digits=(16,3))
    date_presentacion = fields.Date('Fecha presentacion', required=True)
    gerencia_id = fields.Many2one('andina.gerencia', 'Gerencia')
    turno = fields.Selection([('REGULAR', 'REGULAR'), ('PARADA', 'PARADA')], 'Turno', default='REGULAR', required=True)

    @api.onchange('date_presentacion', 'turno')
    def _check_change_date_presentacion(self):
        if self.date_presentacion:
            anio = self.date_presentacion.strftime("%Y")
            mes_number = int(self.date_presentacion.strftime("%m"))
            str_titulo = "LAVANDERIA ROPA DE TRABAJO MANTENIMIENTO " + str(self.month_name(mes_number)) + " " + str(anio)
            if self.turno == 'PARADA':
                str_titulo = str_titulo + ' (' + self.turno + ')'
            self.titulo = (str_titulo).upper()

    def month_name (self, number):
        if number == 1:
            return "Enero"
        elif number == 2:
            return "Febrero"
        elif number == 3:
            return "Marzo"
        elif number == 4:
            return "Abril"
        elif number == 5:
            return "Mayo"
        elif number == 6:
            return "Junio"
        elif number == 7:
            return "Julio"
        elif number == 8:
            return "Agosto"
        elif number == 9:
            return "Septiembre"
        elif number == 10:
            return "Octubre"
        elif number == 11:
            return "Noviembre"
        elif number == 12:
            return "Diciembre"

    def print_report(self):
        if self.fecha_inicio > self.fecha_fin:
            raise UserError('La fecha inicio %s no puede ser mayor a la fecha fin %s') % (self.fecha_inicio,self.fecha_fin)

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'fecha_inicio': self.fecha_inicio,
                'fecha_fin': self.fecha_fin,
                'titulo': self.titulo,
                'precio_kilo': self.precio_kilo,
                'date_presentacion': self.date_presentacion,
                'gerencia_id': self.gerencia_id.id,
                'turno': self.turno,
            },
        }

        return self.env.ref('arc_andina.report_gerencia_action').report_action(self, data=data)

class ReportGerencia(models.AbstractModel):
    _name = 'report.arc_andina.andina_report_gerencia_view'

    def _get_data_area(self, fecha_inicio, fecha_fin, turno, area_id):
        cr = self.env.cr
        pesos = andina_constantes.PesoPrendas
        where_turno = ""
        where_area_id = ""

        if turno:
            if turno == 'REGULAR':
                where_turno = " AND ali.is_parada = False "
            else:
                where_turno = " AND ali.is_parada = True "

        if area_id:
            where_area_id = " AND ali.area_id = %s " % (area_id)

        query = """
            SELECT 
                aa.name AS area_operativa,
                SUM(ali.p1a + ali.p1b + ali.p1c) * %s as peso1,
                SUM(ali.p2a + ali.p2b + ali.p2c) * %s as peso2,
                SUM(ali.p3a + ali.p3b + ali.p3c) * %s as peso3,
                SUM(ali.p4a + ali.p4b + ali.p4c) * %s as peso4,
                SUM(ali.p5a + ali.p5b + ali.p5c) * %s as peso5,
                SUM(ali.p6a + ali.p6b + ali.p6c) * %s as peso6,
                SUM(ali.p7a + ali.p7b + ali.p7c) * %s as peso7,
                SUM(ali.p8a + ali.p8b + ali.p8c) * %s as peso8,
                SUM(ali.p9a + ali.p9b + ali.p9c) * %s as peso9,
                SUM(ali.p10a + ali.p10b + ali.p10c) * %s as peso10,
                SUM(ali.p11a + ali.p11b + ali.p11c) * %s as peso11,
                SUM(ali.p12a + ali.p12b + ali.p12c) * %s as peso12,
                SUM(ali.p13a + ali.p13b + ali.p13c) * %s as peso13,
                SUM(ali.p14a + ali.p14b + ali.p14c) * %s as peso14,
                SUM(ali.p15a + ali.p15b + ali.p15c) * %s as peso15,
                SUM(ali.p16a + ali.p16b + ali.p16c) * %s as peso16,
                SUM(ali.p1a + ali.p1b + ali.p1c) as p1,
                SUM(ali.p2a + ali.p2b + ali.p2c) as p2,
                SUM(ali.p3a + ali.p3b + ali.p3c) as p3,
                SUM(ali.p4a + ali.p4b + ali.p4c) as p4,
                SUM(ali.p5a + ali.p5b + ali.p5c) as p5,
                SUM(ali.p6a + ali.p6b + ali.p6c) as p6,
                SUM(ali.p7a + ali.p7b + ali.p7c) as p7,
                SUM(ali.p8a + ali.p8b + ali.p8c) as p8,
                SUM(ali.p9a + ali.p9b + ali.p9c) as p9,
                SUM(ali.p10a + ali.p10b + ali.p10c) as p10,
                SUM(ali.p11a + ali.p11b + ali.p11c) as p11,
                SUM(ali.p12a + ali.p12b + ali.p12c) as p12,
                SUM(ali.p13a + ali.p13b + ali.p13c) as p13,
                SUM(ali.p14a + ali.p14b + ali.p14c) as p14,
                SUM(ali.p15a + ali.p15b + ali.p15c) as p15,
                SUM(ali.p16a + ali.p16b + ali.p16c) as p16,
                SUM(ali.cantidad_subtotal) AS cantidad_total, 
                SUM(ali.peso_subtotal) AS kilos_total 
            FROM andina_lavado_industrial_line ali 
            JOIN andina_area aa ON ali.area_id = aa.id 
            WHERE ali.state in ('confirm', 'done', 'close') 
            AND ali.fecha >= '%s' 
            AND ali.fecha <= '%s' %s %s 
            GROUP BY aa.name 
            ORDER BY aa.name 
        """ % (
            pesos.p1.value,
            pesos.p2.value,
            pesos.p3.value,
            pesos.p4.value,
            pesos.p5.value,
            pesos.p6.value,
            pesos.p7.value,
            pesos.p8.value,
            pesos.p9.value,
            pesos.p10.value,
            pesos.p11.value,
            pesos.p12.value,
            pesos.p13.value,
            pesos.p14.value,
            pesos.p15.value,
            pesos.p16.value,
            fecha_inicio,
            fecha_fin,
            where_turno,
            where_area_id)

        cr.execute(query)
        _res = cr.dictfetchall()
        return _res

    def _get_sum_area(self, fecha_inicio, fecha_fin, turno, area_id):
        cr = self.env.cr

        where_turno = ""
        where_area_id = ""

        if turno:
            if turno == 'REGULAR':
                where_turno = " AND ali.is_parada = False "
            else:
                where_turno = " AND ali.is_parada = True "

        if area_id:
            where_area_id = " AND ali.area_id = %s " % (area_id)

        query = """
            SELECT 
                sum(ali.cantidad_subtotal),
                sum(ali.peso_subtotal) 
            FROM andina_lavado_industrial_line ali 
            WHERE ali.state in ('confirm', 'done', 'close') 
            AND ali.fecha >= '%s' 
            AND ali.fecha <= '%s' %s %s 
        """ % (fecha_inicio, fecha_fin, where_turno, where_area_id)

        cr.execute(query)
        _res = cr.fetchone()
        return _res

    def _get_sum_totales(self, fecha_inicio, fecha_fin, turno, gerencia_id):
        cr = self.env.cr

        where_turno = ""
        where_gerencia_id = ""

        if turno:
            if turno == 'REGULAR':
                where_turno = " AND ali.is_parada = False "
            else:
                where_turno = " AND ali.is_parada = True "

        if gerencia_id:
            where_gerencia_id = " AND ali.gerencia_id = %s " % (gerencia_id)

        query = """
            SELECT 
                sum(ali.cantidad_subtotal),
                sum(ali.peso_subtotal) 
            FROM andina_lavado_industrial_line ali 
            WHERE ali.state in ('confirm', 'done', 'close') 
            AND ali.fecha >= '%s' 
            AND ali.fecha <= '%s'  %s %s 
        """ % (fecha_inicio, fecha_fin, where_turno, where_gerencia_id)

        cr.execute(query)
        _res = cr.fetchone()
        return _res

    @api.model
    def _get_report_values(self, docids, data=None):
        fecha_inicio = data['form']['fecha_inicio']
        fecha_fin = data['form']['fecha_fin']
        titulo = data['form']['titulo']
        precio_kilo = data['form']['precio_kilo']
        turno = data['form']['turno']
        gerencia_id = data['form']['gerencia_id']

        month_number = time.strftime('%m',time.strptime(data['form']['date_presentacion'],'%Y-%m-%d'))
        month_name = time.strftime('%B',time.strptime(data['form']['date_presentacion'],'%Y-%m-%d'))
        month = self.env['andina.report.gerencia'].month_name(int(month_number))
        date_presentacion = time.strftime('%d %B %Y',time.strptime(data['form']['date_presentacion'],'%Y-%m-%d'))
        date_presentacion= date_presentacion.replace(str(month_name), str(month))
        areas = self.env['andina.area'].search([('gerencia_id', '=', gerencia_id)])
        docs = []
        sum_totales = self._get_sum_totales(fecha_inicio, fecha_fin, turno, gerencia_id)

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'docs': docs,
            'titulo': titulo,
            'precio_kilo': precio_kilo,
            'date_presentacion': date_presentacion,
            'areas': areas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'turno': turno,
            'get_data_area': self._get_data_area,
            'get_sum_area': self._get_sum_area,
            'sum_totales': sum_totales,
        }