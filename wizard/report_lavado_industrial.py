
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_lavado_industrial(osv.osv_memory):
    _name = 'wizard.lavado.industrial'
    _description = 'Reporte del control de lavado industrial'
    _columns = {
        'date_inicio': fields.date('Desde', required=True),
        'date_fin': fields.date('Hasta', required=True),
    }

    _defaults = {
        'date_inicio': False,
        'date_fin': fields.datetime.now,
    }

    def open_table(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        ctx = context.copy()
        ctx['date_inicio'] = data['date_inicio']
        ctx['date_fin'] = data['date_fin']
        return {
            'domain': "[('date_recibido', '>=', '" + data['date_inicio'] + "'),('date_recibido', '<=', '" + data['date_fin'] + "')]",
            'name': _('Reporte de lavado industrial'),
            'view_type': 'form',
            'view_mode': 'tree,graph',
            'res_model': 'report.lavado.industrial',
            'type': 'ir.actions.act_window',
            'context': ctx,
        }


class report_lavado_industrial(osv.osv):
    _name = 'report.lavado.industrial'
    _auto = False
    _order = 'date_recibido asc'

    _columns = {
        'id': fields.integer('ID'),
        'date_recibido' : fields.date('Fecha Recibido'),
        'capuchon' : fields.integer('CAPUCHON'),
        'casaca_corta' : fields.integer('CASACA CORTA'),
        'casaca_cuero' : fields.integer('CASACA CUERO'),
        'casaca_lona' : fields.integer('CASACA DE LONA'),
        'chaleco' : fields.integer('CHALECO'),
        'escarpines' : fields.integer('ESCARPINES'),
        'mameluco' : fields.integer('MAMELUCO'),
        'mandiles_sbsp' : fields.integer('MANDILES CON BROCHES SIN PERCHERA'),
        'mandiles_chcp' : fields.integer('MANDILES CON HEBILLA Y PERCHERA'),
        'mandiles_chsp' : fields.integer('MANDILES CON HEBILLA SIN PERCHERA'),
        'mandiles_lona' : fields.integer('MANDILES LONA CUERO'),
        'pantalones_cuero' : fields.integer('PANTALONES DE CUERO'),
        'pantalones_lona' : fields.integer('PANTALON DE LONA'),
        'pantalones_impermeable' : fields.integer('CASACA Y PANT. IMPERMEABLE'),
        'guantes' : fields.integer('GUANTES CUERO PANTUFLAS'),
        'subtotal' : fields.integer('SUBTOTAL'),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_lavado_industrial')
        cr.execute("""
            CREATE OR REPLACE VIEW report_lavado_industrial AS (
                SELECT
                  distinct (ali.date_recibido_control) as date_recibido,
                  MIN(ali.id) as id,
                  (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'CAPUCHON' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as capuchon,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'CASACA CORTA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as casaca_corta,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'CASACA CUERO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as casaca_cuero,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'CASACA DE LONA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as casaca_lona,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'CHALECO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as chaleco,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'ESCARPINES' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as escarpines,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'MAMELUCO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mameluco,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'MANDILES CON BROCHES SIN PERCHERA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mandiles_sbsp,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'MANDILES CON HEBILLA Y PERCHERA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mandiles_chcp,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'MANDILES CON HEBILLA SIN PERCHERA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mandiles_chsp,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'MANDILES LONA CUERO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as mandiles_lona,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'PANTALONES DE CUERO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as pantalones_cuero,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'PANTALON DE LONA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as pantalones_lona,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'CASACA Y PANT. IMPERMEABLE' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as pantalones_impermeable,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_prenda ap ON li.prenda_id = ap.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND ap.name = 'GUANTES CUERO PANTUFLAS' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as guantes,
                    (SELECT 
                    SUM(li.cantidad)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as subtotal,
                    (SELECT 
                    SUM(li.peso_subtotal)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
            INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'normal' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as subtotal_kilos
                  FROM public.andina_lavado_industrial_line ali
                  INNER JOIN public.andina_lavado_industrial al ON ali.lavado_id = al.id
                  GROUP BY ali.date_recibido_control
                  ORDER BY ali.date_recibido_control asc
            )""")
