import datetime
from openerp import tools, api
from openerp.osv import osv, orm, fields
from openerp.tools.translate import _

class report_detalle_wizard(osv.osv_memory):
    _name = 'wizard.report.detalle'
    _description = 'Impresion del detalle del lavado por area operativa'
    _columns = {
        'date_inicio': fields.date('Desde', required=True),
        'date_fin': fields.date('Hasta', required=True),
        'titulo': fields.char('Titulo'),
        'date_presentacion': fields.date('Fecha presentacion', required=True),
        'gerencia_id': fields.many2one('andina.gerencia', 'Gerencia', required=True),
        'area_id': fields.many2one('andina.area', 'Area Operativa', required=True),
        'print_persona': fields.boolean('Imprimir codigo de trabajadores'),
    }

    _defaults = {
        'date_inicio': False,
        'date_fin': False,
    }

    @api.onchange('date_presentacion','area_id')
    def _check_change_date_presentacion(self):
        if self.date_presentacion:
            s = self.date_presentacion
            slist = s.split("-")
            sdate = datetime.date(int(slist[0]),int(slist[1]),int(slist[2]))
            anio = sdate.strftime("%Y")
            mes_number = int(sdate.strftime("%-m"))
            str_titulo = "DETALLE DEL LAVADO INDUSTRIAL " + str(self.month_name(mes_number)) + " " + str(anio)
            if self.area_id:
                str_titulo = str_titulo + ' - ' + self.area_id.name
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
            return "Deciembre"

    def print_report_detalle(self,cr,uid,ids,context=None):
        report_data = self.browse(cr,uid,ids,context)
        if report_data.date_inicio > report_data.date_fin:
            raise orm.except_orm(_('Error!'),_('La fecha inicio %s no puede ser mayor a la fecha fin %s') % (report_data.date_inicio,report_data.date_fin))
        data = {
            'date_inicio':report_data.date_inicio,
            'date_fin': report_data.date_fin,
            'titulo': report_data.titulo,
            'gerencia_id': report_data.gerencia_id.id,
            'area_id': report_data.area_id.id,
            'date_presentacion': report_data.date_presentacion,
            'print_persona': report_data.print_persona,
            }
        return self.pool['report'].get_action(cr,uid,[],'andina_industrial.report_detalle',data=data,context=context)