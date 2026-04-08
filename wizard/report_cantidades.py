# -*- coding: utf-8 -*-

import time
import pytz
from datetime import datetime, date, timedelta

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.exceptions import UserError
from odoo.addons.arc_andina.models import andina_constantes

class AndinaReportCantidades(models.TransientModel):
    _name = 'andina.report.cantidades'
    _description = 'Reporte del detalle de factura del control de lavado industrial'

    # def _get_default_precio_kilo(self):
    #     return self.env['andina.config.settings'].sudo()._get_precio_kilo()

    def get_date_utc(self):
        if self.env.user.partner_id.tz:
            user_time_zone = pytz.timezone(self.env.user.partner_id.tz)
        else:
            user_time_zone = pytz.timezone('America/Lima')
        now = datetime.now(user_time_zone)
        return now.date()

    date_inicio = fields.Date('Desde', required=True, default=get_date_utc)
    date_fin = fields.Date('Hasta', required=True, default=get_date_utc)
    titulo = fields.Char('Titulo')
    precio_kilo = fields.Float('Precio por Kilo', digits=(16,3))
    date_presentacion = fields.Date('Fecha presentacion', required=True)
    gerencia_id = fields.Many2one('andina.gerencia', 'Gerencia')
    turno = fields.Selection([('REGULAR', 'REGULAR'), ('PARADA', 'PARADA')], 'Turno', default='REGULAR', required=True)

    @api.onchange('date_presentacion', 'gerencia_id', 'turno')
    def _check_change_date_presentacion(self):
        if self.date_presentacion:
            anio = self.date_presentacion.strftime("%Y")
            mes_number = int(self.date_presentacion.strftime("%m"))
            str_titulo = "DETALLE FACTURA LAVADO ROPA INDUSTRIAL " + str(self.month_name(mes_number)) + " " + str(anio)
            if self.gerencia_id:
                str_titulo = str_titulo + ' - ' + self.gerencia_id.name
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
        if self.date_inicio > self.date_fin:
            raise UserError('La fecha inicio %s no puede ser mayor a la fecha fin %s') % (self.date_inicio, self.date_fin)
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_inicio':self.date_inicio,
                'date_fin': self.date_fin,
                'titulo': self.titulo,
                'precio_kilo': self.precio_kilo,
                'date_presentacion': self.date_presentacion,
                'gerencia_id': self.gerencia_id.id,
                'turno': self.turno,
            },
        }
        return self.env.ref('arc_andina.report_cantidades_action').report_action(self, data=data)

class ReportCantidades(models.AbstractModel):
    _name = 'report.arc_andina.andina_report_cantidades_view'

    def _get_data_cantidades(self, fecha_inicio, fecha_fin, gerencia_id, turno):
        cr = self.env.cr
        where_gerencia_id = ""
        where_gerencia = ""
        where_turno = ""

        if turno:
            if turno == 'REGULAR':
                where_turno = " AND ali.is_parada = False "
            else:
                where_turno = " AND ali.is_parada = True "

        if gerencia_id:
            where_gerencia_id = " AND ali.gerencia_id = %s " % (gerencia_id)
            where_gerencia = " AND ali.gerencia_id = %s " % (gerencia_id)

        query = """
            SELECT
                distinct (ali.fecha) as fecha,
                MIN(ali.id) as id,
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
                SUM(ali.cantidad_subtotal) as subtotal,
                SUM(ali.peso_subtotal) as subtotal_kilos
            FROM public.andina_lavado_industrial_line ali 
            WHERE ali.state in ('confirm', 'done', 'close') 
            AND CAST(ali.fecha AS DATE) >= '%s' 
            AND CAST(ali.fecha AS DATE) <= '%s' %s %s 
            GROUP BY ali.fecha, ali.gerencia_id  
            ORDER BY ali.fecha asc
        """ % (fecha_inicio, fecha_fin, where_gerencia, where_turno)

        cr.execute(query)
        return cr.dictfetchall()

    def _get_data_totales(self, fecha_inicio, fecha_fin, gerencia_id, turno):
        cr = self.env.cr
        where_gerencia_id = ""
        where_gerencia = ""
        where_turno = ""

        if turno:
            if turno == 'REGULAR':
                where_turno = " AND ali.is_parada = False "
            else:
                where_turno = " AND ali.is_parada = True "

        if gerencia_id:
            where_gerencia_id = " AND ali.gerencia_id = %s " % (gerencia_id)
            where_gerencia = " AND ali.gerencia_id = %s " % (gerencia_id)

        query = """
            SELECT 
                MAX(ali.id) as id,
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
                SUM(ali.cantidad_subtotal) as subtotal,
                SUM(ali.peso_subtotal) as subtotal_kilos 
            FROM public.andina_lavado_industrial_line ali 
            WHERE ali.state in ('confirm', 'done', 'close') 
            AND CAST(ali.fecha AS DATE) >= '%s' 
            AND CAST(ali.fecha AS DATE) <= '%s' %s %s 
        """ % (fecha_inicio, fecha_fin, where_gerencia, where_turno)

        cr.execute(query)
        return cr.fetchone()

    def _get_data_pesos(self, fecha_inicio, fecha_fin, gerencia_id, turno):
        pesos = andina_constantes.PesoPrendas
        cr = self.env.cr
        where_gerencia_id = ""
        where_gerencia = ""
        where_turno = ""

        if turno:
            if turno == 'REGULAR':
                where_turno = " AND ali.is_parada = False "
            else:
                where_turno = " AND ali.is_parada = True "

        if gerencia_id:
            where_gerencia_id = " AND ali.gerencia_id = %s " % (gerencia_id)
            where_gerencia = " AND ali.gerencia_id = %s " % (gerencia_id)

        query = """
            SELECT 
                MAX(ali.id) as id,
                SUM(ali.p1a + ali.p1b + ali.p1c) * %s as p1,
                SUM(ali.p2a + ali.p2b + ali.p2c) * %s as p2,
                SUM(ali.p3a + ali.p3b + ali.p3c) * %s as p3,
                SUM(ali.p4a + ali.p4b + ali.p4c) * %s as p4,
                SUM(ali.p5a + ali.p5b + ali.p5c) * %s as p5,
                SUM(ali.p6a + ali.p6b + ali.p6c) * %s as p6,
                SUM(ali.p7a + ali.p7b + ali.p7c) * %s as p7,
                SUM(ali.p8a + ali.p8b + ali.p8c) * %s as p8,
                SUM(ali.p9a + ali.p9b + ali.p9c) * %s as p9,
                SUM(ali.p10a + ali.p10b + ali.p10c) * %s as p10,
                SUM(ali.p11a + ali.p11b + ali.p11c) * %s as p11,
                SUM(ali.p12a + ali.p12b + ali.p12c) * %s as p12,
                SUM(ali.p13a + ali.p13b + ali.p13c) * %s as p13,
                SUM(ali.p14a + ali.p14b + ali.p14c) * %s as p14,
                SUM(ali.p15a + ali.p15b + ali.p15c) * %s as p15,
                SUM(ali.p16a + ali.p16b + ali.p16c) * %s as p16,
                SUM(ali.cantidad_subtotal) as subtotal,
                SUM(ali.peso_subtotal) as subtotal_kilos 
            FROM public.andina_lavado_industrial_line ali 
            WHERE ali.state in ('confirm', 'done', 'close') 
            AND CAST(ali.fecha AS DATE) >= '%s' 
            AND CAST(ali.fecha AS DATE) <= '%s' %s %s 
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
            where_gerencia,
            where_turno
            )

        cr.execute(query)
        return cr.fetchone()

    def _get_sum_cantidades(self, fecha_inicio, fecha_fin, gerencia_id, turno):
        cr = self.env.cr
        where_gerencia_id = ""
        where_turno = ""

        if turno:
            if turno == 'REGULAR':
                where_turno = " AND ali.is_parada = False "
            else:
                where_turno = " AND ali.is_parada = True "

        if gerencia_id:
            where_gerencia_id = " AND ali.gerencia_id = %s " % (gerencia_id)

        query = """
            SELECT 
                SUM(ali.cantidad_subtotal) as sum_cantidades 
            FROM public.andina_lavado_industrial_line ali 
            WHERE ali.state in ('confirm', 'done', 'close') 
            AND CAST(ali.fecha AS DATE) >= '%s' 
            AND CAST(ali.fecha AS DATE) <= '%s' %s %s 
        """ % (fecha_inicio, fecha_fin, where_gerencia_id, where_turno)

        cr.execute(query)
        return cr.fetchone()

    def _get_sum_peso(self, fecha_inicio, fecha_fin, gerencia_id, turno):
        cr = self.env.cr
        where_gerencia_id = ""
        where_turno = ""

        if turno:
            if turno == 'REGULAR':
                where_turno = " AND ali.is_parada = False "
            else:
                where_turno = " AND ali.is_parada = True "

        if gerencia_id:
            where_gerencia_id = " AND ali.gerencia_id = %s " % (gerencia_id)

        query = """
            SELECT 
                SUM(ali.peso_subtotal) as sum_pesos 
            FROM public.andina_lavado_industrial_line ali 
            WHERE ali.state in ('confirm', 'done', 'close') 
            AND CAST(ali.fecha AS DATE) >= '%s' 
            AND CAST(ali.fecha AS DATE) <= '%s' %s %s 
        """ % (fecha_inicio, fecha_fin, where_gerencia_id, where_turno)

        cr.execute(query)
        return cr.fetchone()

    # def _get_sum_precio_total(self, fecha_inicio, fecha_fin, turno):
    #     cr = self.env.cr
    #     where_gerencia_id = ""
    #     where_turno = ""

    #     if turno:
    #         if turno == 'REGULAR':
    #             where_turno = " AND ali.is_parada = False "
    #         else:
    #             where_turno = " AND ali.is_parada = True "

    #     if gerencia_id:
    #         where_gerencia_id = " AND ali.gerencia_id = %s " % (gerencia_id)

    #     query = """
    #         SELECT 
    #             SUM(ali.peso_subtotal) 
    #         FROM public.andina_lavado_industrial_line ali 
    #         WHERE ali.state in ('confirm', 'done', 'close') 
    #         AND CAST(ali.fecha AS DATE) >= '%s' 
    #         AND CAST(ali.fecha AS DATE) <= '%s %s %s' 
    #     """ % (fecha_inicio, fecha_fin, where_turno_id, where_turno)

    #     cr.execute(query)
    #     return cr.fetchone()

    @api.model
    def _get_report_values(self, docids, data=None):
        # date_inicio = datetime.strptime(data['form']['date_inicio'], DATE_FORMAT)
        # date_fin = datetime.strptime(data['form']['date_fin'], DATE_FORMAT)
        date_inicio = data['form']['date_inicio']
        date_fin = data['form']['date_fin']
        titulo = data['form']['titulo']
        precio_kilo = data['form']['precio_kilo']
        gerencia_id = data['form']['gerencia_id']
        turno = data['form']['turno']

        month_number = time.strftime('%m',time.strptime(data['form']['date_presentacion'],'%Y-%m-%d'))
        month_name = time.strftime('%B',time.strptime(data['form']['date_presentacion'],'%Y-%m-%d'))
        month = self.env['andina.report.cantidades'].month_name(int(month_number))
        date_presentacion = time.strftime('%d %B %Y',time.strptime(data['form']['date_presentacion'],'%Y-%m-%d'))
        date_presentacion= date_presentacion.replace(str(month_name), str(month))

        docs = []

        data_cantidades = self._get_data_cantidades(date_inicio, date_fin, gerencia_id, turno)
        data_totales = self._get_data_totales(date_inicio, date_fin, gerencia_id, turno)
        data_pesos = self._get_data_pesos(date_inicio, date_fin, gerencia_id, turno)
        sum_peso = self._get_sum_peso(date_inicio, date_fin, gerencia_id, turno)
        sum_cantidades = self._get_sum_cantidades(date_inicio, date_fin, gerencia_id, turno)
        # sum_precio_total = self._get_sum_precio_total(date_inicio, date_fin, turno)
            
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'docs': docs,
            'titulo': titulo,
            'turno': turno,
            'precio_kilo': precio_kilo,
            'date_presentacion': date_presentacion,
            'data_cantidades' : data_cantidades,
            'data_totales' : data_totales,
            'data_pesos' : data_pesos,
            'sum_peso' : sum_peso,
            'sum_cantidades' : sum_cantidades,
            #'sum_precio_total' : sum_precio_total,
        }