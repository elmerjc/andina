# -*- encoding: utf-8 -*-

from openerp.report import report_sxw
from openerp.osv import osv

class report_consolidado_wizard(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        if context is None:
            context = {}
        super(report_consolidado_wizard,self).__init__(cr,uid,name, context=context)
        self.localcontext.update({
            'get_data_automotriz_puerto':self._get_data_automotriz_puerto,
            'get_sum_automotriz_puerto':self._get_sum_automotriz_puerto,
            'get_data_casa_cambio':self._get_data_casa_cambio,
            'get_sum_casa_cambio':self._get_sum_casa_cambio,
            'get_data_layza':self._get_data_layza,
            'get_sum_layza':self._get_sum_layza,
            'get_data_albaniles':self._get_data_albaniles,
            'get_sum_albaniles':self._get_sum_albaniles,
            'get_data_acidos':self._get_data_acidos,
            'get_sum_acidos':self._get_sum_acidos,
            'get_data_patio_simon':self._get_data_patio_simon,
            'get_sum_patio_simon':self._get_sum_patio_simon,
            'get_data_anodos':self._get_data_anodos,
            'get_sum_anodos':self._get_sum_anodos,
            'get_data_premin':self._get_data_premin,
            'get_sum_premin':self._get_sum_premin,
            'get_data_carranza':self._get_data_carranza,
            'get_sum_carranza':self._get_sum_carranza,
            'get_data_mecanica_instrumental':self._get_data_mecanica_instrumental,
            'get_sum_mecanica_instrumental':self._get_sum_mecanica_instrumental,
            'get_data_electrico_construccion':self._get_data_electrico_construccion,
            'get_sum_electrico_construccion':self._get_sum_electrico_construccion,
            'get_data_equipo_pesado':self._get_data_equipo_pesado,
            'get_sum_equipo_pesado':self._get_sum_equipo_pesado,
            'get_data_kamag':self._get_data_kamag,
            'get_sum_kamag':self._get_sum_kamag,  
            'get_data_taller_mecanica':self._get_data_taller_mecanica,
            'get_sum_taller_mecanica':self._get_sum_taller_mecanica,  
            'get_data_vagones':self._get_data_vagones,
            'get_sum_vagones':self._get_sum_vagones,  
            'get_sum_totales':self._get_sum_totales,         
            })
        self.context = context

    def _get_data_automotriz_puerto(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 15 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_automotriz_puerto(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 15 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_casa_cambio(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 1 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_casa_cambio(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 1 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_layza(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 8 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_layza(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 8 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_albaniles(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 10 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_albaniles(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 10 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_acidos(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 5 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_acidos(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 5 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_patio_simon(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
        wizard_obj=self.pool.get('wizard.report.consolidado')
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

    def _get_data_anodos(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 2 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_anodos(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 2 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_premin(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 9 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_premin(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 9 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_carranza(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 7 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_carranza(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 7 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_mecanica_instrumental(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 3 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_mecanica_instrumental(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 3 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_electrico_construccion(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 13 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_electrico_construccion(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 13 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_equipo_pesado(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 11 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_equipo_pesado(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 11 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_kamag(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 6 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_kamag(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 6 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_taller_mecanica(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
              WHERE ali.state = 'done' AND aa.id = 12 AND ali.date_recibido >= '%s' AND ali.date_recibido <= '%s'
              GROUP BY ag.name, aa.name, ap.name
              ORDER BY ag.name, aa.name
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_taller_mecanica(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND aa.id = 12 AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_data_vagones(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
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
        wizard_obj=self.pool.get('wizard.report.consolidado')
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

    def _get_sum_totales(self):
        wizard_obj=self.pool.get('wizard.report.consolidado')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)
        query = """
            SELECT 
                sum(lil.cantidad),
                sum(lil.peso_subtotal)
            FROM andina_lavado_industrial_line lil
            JOIN andina_lavado_industrial li ON lil.lavado_id = li.id
            JOIN andina_area aa ON lil.area_id = aa.id
            WHERE li.state = 'done' AND li.date_recibido >= '%s' AND li.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

class report_consolidado(osv.AbstractModel):
    _name="report.andina_industrial.report_consolidado"
    _inherit="report.abstract_report"
    _template="andina_industrial.report_consolidado"
    _wrapped_report_class=report_consolidado_wizard
    
    
