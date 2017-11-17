
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_especial_lavado_industrial(osv.osv_memory):
    _name = 'wizard.especial.lavado.industrial'
    _description = 'especiale Especial del control de lavado industrial'
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
            'name': _('Reporte por areas especiales'),
            'view_type': 'form',
            'view_mode': 'tree,graph',
            'res_model': 'especial.lavado.industrial',
            'type': 'ir.actions.act_window',
            'context': ctx,
        }


class especial_lavado_industrial(osv.osv):
    _name = 'especial.lavado.industrial'
    _auto = False
    _order = 'date_recibido desc'

    _columns = {
        'id': fields.integer('ID'),
        'date_recibido' : fields.date('Fecha Recibido'),
        'vagones' : fields.float('VAGONES', digits=(16,3)),
        'patio_simon' : fields.float('PATIO SIMON', digits=(16,3)),
        'automotriz_puerto' : fields.float('AUTOMOTRIZ PUERTO', digits=(16,3)),
        'coquina' : fields.float('COQUINA', digits=(16,3)),
        'subtotal' : fields.float('SUBTOTAL', digits=(16,3)),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'especial_lavado_industrial')
        cr.execute("""
            CREATE OR REPLACE VIEW especial_lavado_industrial AS (
                SELECT
                    distinct (ali.date_recibido_control) as date_recibido,
                    MIN(ali.id) as id,
                    (SELECT 
                    SUM(li.peso_subtotal)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'especial' AND aa.name = 'VAGONES' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as vagones,
                    (SELECT 
                    SUM(li.peso_subtotal)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'especial' AND aa.name = 'PATIO SIMON' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as patio_simon,
                    (SELECT 
                    SUM(li.peso_subtotal)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'especial' AND aa.name = 'AUTOMOTRIZ PUERTO' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as automotriz_puerto,
                    (SELECT 
                    SUM(li.peso_subtotal)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'especial' AND aa.name = 'COQUINA' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as coquina,
                    (SELECT 
                    SUM(li.peso_subtotal)
                    FROM public.andina_lavado_industrial_line li
                    INNER JOIN public.andina_lavado_industrial pali ON li.lavado_id = pali.id
                    INNER JOIN public.andina_area aa ON li.area_id = aa.id
                    WHERE pali.state = 'done' AND aa.tipo = 'especial' AND CAST(li.date_recibido_control AS DATE) = CAST(ali.date_recibido_control AS DATE)
                    ) as subtotal
                FROM public.andina_lavado_industrial_line ali
                INNER JOIN public.andina_lavado_industrial al ON ali.lavado_id = al.id
                GROUP BY ali.date_recibido_control
                ORDER BY ali.date_recibido_control asc
            )""")
