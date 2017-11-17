# -*- encoding: utf-8 -*-

from openerp.report import report_sxw
from openerp.osv import osv

class report_cantidades_wizard(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        if context is None:
            context = {}
        super(report_cantidades_wizard,self).__init__(cr,uid,name, context=context)
        self.localcontext.update({
            'get_data_cantidades':self._get_data_cantidades,
            'get_data_especiales':self._get_data_especiales,
            'get_sum_peso':self._get_sum_peso,
            'get_sum_cantidades':self._get_sum_cantidades,
            'get_sum_cantidades_especial':self._get_sum_cantidades_especial,
            'get_sum_precio_total':self._get_sum_precio_total,
            'get_sum_capuchon':self._get_sum_capuchon,
            'get_sum_casaca_corta':self._get_sum_casaca_corta,
            'get_sum_casaca_cuero':self._get_sum_casaca_cuero,
            'get_sum_casaca_lona':self._get_sum_casaca_lona,
            'get_sum_chaleco':self._get_sum_chaleco,
            'get_sum_escarpines':self._get_sum_escarpines,
            'get_sum_mameluco':self._get_sum_mameluco,
            'get_sum_mandiles_sbsp':self._get_sum_mandiles_sbsp,
            'get_sum_mandiles_chcp':self._get_sum_mandiles_chcp,
            'get_sum_mandiles_chsp':self._get_sum_mandiles_chsp,
            'get_sum_mandiles_lona':self._get_sum_mandiles_lona,
            'get_sum_pantalones_cuero':self._get_sum_pantalones_cuero,
            'get_sum_camisa_pantalon':self._get_sum_camisa_pantalon,
            'get_sum_pantalones_lona':self._get_sum_pantalones_lona,
            'get_sum_pantalones_impermeable':self._get_sum_pantalones_impermeable,
            'get_sum_guantes':self._get_sum_guantes,
            })
        self.context = context

    def _get_data_cantidades(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        where_gerencia = ""

        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)
            where_gerencia = " AND ar.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT
                  distinct (ali.date_recibido_control) as date_recibido,
                  MIN(ali.id) as id,
                  (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'CAPUCHON' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as capuchon,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'CASACA CORTA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as casaca_corta,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'CASACA CUERO (SOLDADOR)' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as casaca_cuero,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'CASACA DE LONA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as casaca_lona,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'CHALECO DE SEGURIDAD' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as chaleco,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'ESCARPINES' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as escarpines,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'MAMELUCO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mameluco,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'MANDILES CON BROCHES SIN PERCHERA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mandiles_sbsp,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'MANDILES CON HEBILLA Y PERCHERA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mandiles_chcp,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'MANDILES CON HEBILLA SIN PERCHERA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mandiles_chsp,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'MANDILES LONA CUERO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mandiles_lona,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'PANTALONES DE CUERO (SOLDADOR)' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as pantalones_cuero,
                     (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'CAMISA PANTALON' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as camisa_pantalon,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'PANTALON DE LONA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as pantalones_lona,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'CASACA Y PANT. IMPERMEABLE (ANTIACIDOS)' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as pantalones_impermeable,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND ap.name = 'GUANTES CUERO PANTUFLAS GORRO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as guantes,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as subtotal,
                    (SELECT 
                    SUM(li.peso_subtotal)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' %s AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as subtotal_kilos
                  FROM public.andina_lavado_industrial_line ali
                  INNER JOIN public.andina_lavado_industrial al ON ali.lavado_id = al.id
                  INNER JOIN public.andina_area ar ON ali.area_id = ar.id
                  WHERE ali.date_recibido_control >= '%s' AND ali.date_recibido_control <= '%s' %s
                  GROUP BY ali.date_recibido_control
                  ORDER BY ali.date_recibido_control asc
        """ % (
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            where_gerencia_id,
            wizard_data.date_inicio, wizard_data.date_fin, where_gerencia)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_data_especiales(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        query = """
            SELECT
            sum(vagones) as peso_vagones,
            sum(patio_simon) as peso_patio_simon,
            sum(automotriz_puerto) as peso_automotriz_puerto,
            sum(coquina) as peso_coquina,
            sum(subtotal) as peso_total
            FROM especial_lavado_industrial eli
            WHERE eli.date_recibido >= '%s' AND eli.date_recibido <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

    def _get_sum_cantidades_especial(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)
        query = """
            SELECT 
                SUM(li.cantidad)
            FROM public.andina_lavado_industrial_line li
            INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' AND aa.tipo = 'especial' AND CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_cantidades(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)
        
        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad) as sum_cantidades
            FROM public.andina_lavado_industrial_line li
            INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_peso(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.peso_subtotal) as sum_pesos
            FROM public.andina_lavado_industrial_line li
            INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_precio_total(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)
        query = """
            SELECT 
                SUM(pali.precio_total)
            FROM public.andina_lavado_industrial pali
            WHERE pali.state = 'done' AND CAST(pali.date_recibido AS DATE) >= '%s' AND CAST(pali.date_recibido AS DATE) <= '%s'
        """ % (wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_capuchon(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'CAPUCHON' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_casaca_corta(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'CASACA CORTA' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_casaca_cuero(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'CASACA CUERO (SOLDADOR)' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_casaca_lona(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'CASACA DE LONA' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_chaleco(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'CHALECO DE SEGURIDAD' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_escarpines(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'ESCARPINES' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_mameluco(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'MAMELUCO' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_mandiles_sbsp(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'MANDILES CON BROCHES SIN PERCHERA' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_mandiles_chcp(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'MANDILES CON HEBILLA Y PERCHERA' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_mandiles_chsp(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'MANDILES CON HEBILLA SIN PERCHERA' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_mandiles_lona(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'MANDILES LONA CUERO' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_pantalones_cuero(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'PANTALONES DE CUERO (SOLDADOR)' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_camisa_pantalon(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'CAMISA PANTALON' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_pantalones_lona(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'PANTALON DE LONA' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_pantalones_impermeable(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'CASACA Y PANT. IMPERMEABLE (ANTIACIDOS)' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

    def _get_sum_guantes(self):
        wizard_obj=self.pool.get('wizard.report.cantidades')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_gerencia_id = ""
        if wizard_data.gerencia_id.id:
            where_gerencia_id = " AND aa.gerencia_id = %s " % (wizard_data.gerencia_id.id)

        query = """
            SELECT 
                SUM(li.cantidad),
                SUM(li.peso_subtotal)
                FROM public.andina_lavado_industrial_line li
                INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
            WHERE pali.state = 'done' %s AND ap.name = 'GUANTES CUERO PANTUFLAS GORRO' AND  CAST(li.date_recibido_control AS DATE) >= '%s' AND CAST(li.date_recibido_control AS DATE) <= '%s'
        """ % (where_gerencia_id, wizard_data.date_inicio, wizard_data.date_fin)

        self.cr.execute(query)
        _res = self.cr.fetchone()
        return _res

class report_cantidades(osv.AbstractModel):
    _name="report.andina_industrial.report_cantidades"
    _inherit="report.abstract_report"
    _template="andina_industrial.report_cantidades"
    _wrapped_report_class=report_cantidades_wizard
    
    
