# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 S&C (arc.pe).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name' : 'Lavado Industrial',
    'version' : '1.0',
    'category': 'Uncategorized',
    'author' : 'ARC',
    'website': "http://www.arc.pe",
    'summary' : 'Gestiona el lavado industrial',
    'description' : 'Gestiona el lavado industrial',
    'depends' : [
                'base',
                'report',
                ],
    'data' : [
            'security/andina_security.xml',
            'security/ir.model.access.csv',
            'lavado_industrial_sequence.xml',
            'lavado_industrial_view.xml',
            'lavado_industrial_line_view.xml',
            'persona_view.xml',
            'prenda_view.xml',
            'prenda_data.xml',
            'area_view.xml',
            'wizard/report_lavado_industrial_view.xml',
            'wizard/consolidado_lavado_industrial_view.xml',
            'wizard/especial_lavado_industrial_view.xml',
            'wizard/report_cantidades_wizard_view.xml',
            'wizard/report_consolidado_wizard_view.xml',
            'wizard/report_mantenimiento_wizard_view.xml',
            'wizard/report_operaciones_wizard_view.xml',
            'wizard/report_ferrocarriles_wizard_view.xml',
            'wizard/report_detalle_wizard_view.xml',
            'wizard/prenda_multiple_wizard_view.xml',
            'lavado_industrial_report.xml',
            'views/andina_layouts.xml',
            'views/report_controlindustrial.xml',
            'views/report_cantidades.xml',
            'views/report_consolidado.xml',
            'views/report_mantenimiento.xml',
            'views/report_operaciones.xml',
            'views/report_ferrocarriles.xml',
            'views/report_detalle.xml',
            'views/css_view.xml',
            ],
    'installable' : True,
    'aplication' : True,
}
