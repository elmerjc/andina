# -*- encoding: utf-8 -*-

from openerp.report import report_sxw
from openerp.osv import osv

class report_ferrocarriles_wizard(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        if context is None:
            context = {}
        super(report_ferrocarriles_wizard,self).__init__(cr,uid,name, context=context)
        self.localcontext.update({
            'get_data_vagones':self._get_data_vagones,
            'get_sum_vagones':self._get_sum_vagones,
            'get_data_patio_simon':self._get_data_patio_simon,
            'get_sum_patio_simon':self._get_sum_patio_simon,
            'get_sum_totales':self._get_sum_totales,         
            })
        self.context = context

    def _get_data_vagones(self):
        wizard_obj=self.pool.get('wizard.report.ferrocarriles')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
             SELECT 
                ag.name AS gerencia,
                aa.name AS area_operativa,
                ap.name AS prenda,
                sum(alil.cantidad) AS cantidad_total,
                sum(alil.peso_subtotal) AS kilos_total
               FROM andina_lavado_industrial_line alil
                 JOIN andina_lavado_industrial ali ON alil.lavado_id = ali.id
                 JOIN andina_prenda ap ON alil.prenda_id = ap.id
                 JOIN andina_area aa ON alil.area_id = aa.id
                 JOIN andina_gerencia ag ON aa.gerencia_id = ag.id
              WHERE ali.state = 'done' AND aa.id = 14 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_vagones(self):
        wizard_obj=self.pool.get('wizard.report.ferrocarriles')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 14 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_patio_simon(self):
        wizard_obj=self.pool.get('wizard.report.ferrocarriles')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
             SELECT 
                ag.name AS gerencia,
                aa.name AS area_operativa,
                ap.name AS prenda,
                sum(alil.cantidad) AS cantidad_total,
                sum(alil.peso_subtotal) AS kilos_total
               FROM andina_lavado_industrial_line alil
                 JOIN andina_lavado_industrial ali ON alil.lavado_id = ali.id
                 JOIN andina_prenda ap ON alil.prenda_id = ap.id
                 JOIN andina_area aa ON alil.area_id = aa.id
                 JOIN andina_gerencia ag ON aa.gerencia_id = ag.id
              WHERE ali.state = 'done' AND aa.id = 16 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_patio_simon(self):
        wizard_obj=self.pool.get('wizard.report.ferrocarriles')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 16 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_totales(self):
        wizard_obj=self.pool.get('wizard.report.ferrocarriles')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)
        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            JOIN andina_gerencia ag ON aa.gerencia_id = ag.id
            WHERE li.state = 'done' AND ag.name = 'FERROCARRILES' AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

class report_ferrocarriles(osv.AbstractModel):
    _name="report.andina_industrial.report_ferrocarriles"
    _inherit="report.abstract_report"
    _template="andina_industrial.report_ferrocarriles"
    _wrapped_report_class=report_ferrocarriles_wizard
    
    
