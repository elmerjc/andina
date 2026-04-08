# -*- coding: utf-8 -*-
{
    'name': 'Control de Lavado Industrial',
    'version': '13.0',
    'category': 'website',
    'sequence': 1,
    'description': 'Control de Lavado Industrial',
    'author' : 'arc',
    'website': 'www.arc.pe',
    'depends': [
        'base'
    ],
    'data': [
        'security/andina_security.xml',
        'security/ir.model.access.csv',
        'data/data_area.xml',
        'views/andina_menu.xml',
        'views/andina_sequence.xml',
        'views/andina_area_view.xml',
        # 'views/andina_prenda_view.xml',
        'views/andina_lavado_view.xml',
        'views/andina_assets.xml',
        'views/andina_layouts.xml',
        'report/andina_report.xml',
        'report/andina_report_cantidades.xml',
        'report/andina_report_consolidado.xml',
        'report/andina_report_gerencia.xml',
        'report/andina_report_area.xml',
        'wizard/report_cantidades_view.xml',
        'wizard/report_consolidado_view.xml',
        'wizard/report_gerencia_view.xml',
        'wizard/report_area_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
