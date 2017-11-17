# -*- encoding: utf-8 -*-

from openerp.report import report_sxw
from openerp.osv import osv

class report_detalle_wizard(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        if context is None:
            context = {}
        super(report_detalle_wizard,self).__init__(cr,uid,name, context=context)
        self.localcontext.update({
            'get_data_detalle':self._get_data_detalle,
            'get_data_dates':self._get_data_dates,
            'get_data_persona':self._get_data_persona,
            })
        self.context = context

    def _get_data_persona(self, line_id):
        query = """
             SELECT 
                per.name as codigo
              FROM andina_lavado_industrial_persona_rel lap
              JOIN andina_persona per ON lap.persona_id = per.id
              WHERE lap.lavado_line_id = %s
              ORDER BY per.name
        """ % (line_id)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_data_detalle(self, date_recibido):
        wizard_obj=self.pool.get('wizard.report.detalle')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
             SELECT 
                alil.id as line_id,
                ali.date_recibido,
                ali.turno,
                ap.name AS prenda,
                sum(alil.cantidad) AS cantidad_total,
                sum(alil.peso_subtotal) AS kilos_total
               FROM andina_lavado_industrial_line alil
                 JOIN andina_lavado_industrial ali ON alil.lavado_id = ali.id
                 JOIN andina_prenda ap ON alil.prenda_id = ap.id
                 JOIN andina_area aa ON alil.area_id = aa.id
                 JOIN andina_gerencia ag ON aa.gerencia_id = ag.id
              WHERE ali.state = 'done' AND aa.id = %s AND ali.date_recibido = '%s'
              GROUP BY ali.date_recibido, ap.name, ali.turno, alil.id
              ORDER BY ali.date_recibido, ali.turno
        """ % (wizard_data.area_id.id, date_recibido)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_data_dates(self):
        wizard_obj=self.pool.get('wizard.report.detalle')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
              SELECT 
                ali.date_recibido
               FROM andina_lavado_industrial_line alil
                 JOIN andina_lavado_industrial ali ON alil.lavado_id = ali.id
                 JOIN andina_prenda ap ON alil.prenda_id = ap.id
                 JOIN andina_area aa ON alil.area_id = aa.id
              WHERE ali.state = 'done' AND aa.id = %s AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ali.date_recibido
              ORDER BY ali.date_recibido
        """ % (wizard_data.area_id.id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res


class report_detalle(osv.AbstractModel):
    _name="report.andina_industrial.report_detalle"
    _inherit="report.abstract_report"
    _template="andina_industrial.report_detalle"
    _wrapped_report_class=report_detalle_wizard
    
    
