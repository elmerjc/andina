
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_consolidado_lavado_industrial(osv.osv_memory):
    _name = 'wizard.consolidado.lavado.industrial'
    _description = 'Consolidado del control de lavado industrial'
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
        ctx['search_default_group_by_area_operativa'] = True
        ctx['search_default_group_by_prenda'] = True
        return {
            'domain': "['&',('date_recibido', '>=', '" + data['date_inicio'] + "'),('date_recibido', '<=', '" + data['date_fin'] + "')]",
            'name': _('Consolidado de lavado industrial'),
            'view_type': 'form',
            'view_mode': 'tree,graph',
            'res_model': 'consolidado.lavado.industrial',
            'type': 'ir.actions.act_window',
            'context': ctx,
        }


class consolidado_lavado_industrial(osv.osv):
    _name = 'consolidado.lavado.industrial'
    _auto = False
    _order = 'gerencia desc'

    _columns = {
        'id': fields.integer('ID'),
        'date_recibido' : fields.date('Fecha recibido'),
        'gerencia' : fields.char('Gerencia'),
        'area_operativa' : fields.char('Area operativa'),
        'prenda' : fields.char('Prendas'),
        'cantidad_total' : fields.integer('Cantidad'),
        'kilos_total' : fields.float('Kilos', digits=(16,3)),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'consolidado_lavado_industrial')
        cr.execute("""
            CREATE OR REPLACE VIEW consolidado_lavado_industrial AS (
                SELECT 
                    1 as id,
                    ali.date_recibido,
                    ag.name AS gerencia,
                    aa.name AS area_operativa,
                    ap.name AS prenda,
                    sum(alil.cantidad) as cantidad_total,
                    sum(alil.peso_subtotal) as kilos_total
                FROM andina_lavado_industrial_line alil
                INNER JOIN andina_lavado_industrial ali ON alil.lavado_id = ali.id
                INNER JOIN andina_prenda ap ON alil.prenda_id = ap.id
                INNER JOIN andina_area aa ON alil.area_id = aa.id
                INNER JOIN andina_gerencia ag ON aa.gerencia_id = ag.id
                WHERE ali.state = 'done' 
                GROUP BY ali.date_recibido, ag.name, aa.name, ap.name
                ORDER BY ag.name, aa.name
            )""")
