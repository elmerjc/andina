import datetime
from openerp import tools, api
from openerp.osv import osv, orm, fields
from openerp.tools.translate import _

class report_consolidado_wizard(osv.osv_memory):
    _name = 'wizard.report.consolidado'
    _description = 'Impresion del consolidado del control de lavado industrial'
    _columns = {
        'date_inicio': fields.date('Desde', required=True),
        'date_fin': fields.date('Hasta', required=True),
        'titulo': fields.char('Titulo'),
        'precio_kilo': fields.float('Precio por Kilo', digits=(16,3)),
        'date_presentacion': fields.date('Fecha presentacion', required=True),
    }

    _defaults = {
        'date_inicio': False,
        'date_fin': False,
        'precio_kilo': 2.950,
    }

    @api.onchange('date_presentacion')
    def _check_change_date_presentacion(self):
        if self.date_presentacion:
            s = self.date_presentacion
            slist = s.split("-")
            sdate = datetime.date(int(slist[0]),int(slist[1]),int(slist[2]))
            self.titulo = sdate.strftime("LAVANDERIA ROPA DE TRABAJO %B %Y").upper()

    def print_report_consolidado(self,cr,uid,ids,context=None):
        report_data = self.browse(cr,uid,ids,context)
        if report_data.date_inicio > report_data.date_fin:
            raise orm.except_orm(_('Error!'),_('La fecha inicio %s no puede ser mayor a la fecha fin %s') % (report_data.date_inicio,report_data.date_fin))
        data = {
            'date_inicio':report_data.date_inicio,
            'date_fin': report_data.date_fin,
            'titulo': report_data.titulo,
            'precio_kilo': report_data.precio_kilo,
            'date_presentacion': report_data.date_presentacion,
            }
        return self.pool['report'].get_action(cr,uid,[],'andina_industrial.report_consolidado',data=data,context=context)