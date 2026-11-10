# -*- coding: utf-8 -*-
"""Migración de datos: Odoo 13 (módulo ``arc_andina``) -> Odoo 19 (módulo ``andina``).

Copia gerencias, áreas operativas, controles de lavado industrial (cabecera + detalle
por fecha) y el correlativo de la secuencia ``andina.lavado.industrial``.
La base de Odoo 13 solo se LEE (conexión de solo lectura); todo se escribe con el ORM
de Odoo 19, por lo que los campos calculados (subtotales, totales, gerencia, estado de
las líneas) se recalculan y luego se comparan contra los valores guardados en Odoo 13.

Pasos
-----
1. Restaurar el backup de Odoo 13 como otra base en el MISMO PostgreSQL (ej. ``andina13``).
2. Instalar el módulo en la base destino (ej. ``msim``):
       odoo -d msim -i andina --stop-after-init
3. Crear en la base destino los usuarios que eran "Responsable" en Odoo 13 (se enlazan por
   ``login``; los que no existan quedan sin responsable y se listan en el reporte).
4. SIMULACIÓN (ejecuta todo, imprime el reporte y hace rollback):
       docker exec -i -e ANDINA_OLD_DB=andina13 odoo-19 sh -c 'odoo shell -d msim \\
           --db_host="$HOST" --db_user="$USER" --db_password="$PASSWORD" --no-http' \\
           < scripts/migrate_from_odoo13.py
5. MIGRACIÓN REAL: el mismo comando agregando ``-e ANDINA_COMMIT=1``.

Variables de entorno
--------------------
ANDINA_OLD_DB   (obligatoria) nombre de la base Odoo 13 restaurada.
ANDINA_OLD_DSN  (opcional) DSN/URI de PostgreSQL si la base Odoo 13 está en otro servidor.
ANDINA_COMMIT   (opcional) "1" para guardar; si no, simulación.
ANDINA_BATCH    (opcional) líneas por lote de creación (por defecto 1000).

Reglas
------
* Se puede ejecutar varias veces: un control cuyo ``name`` ya existe en destino se omite.
* Gerencias y áreas se enlazan por nombre. Si el área ya existe (datos semilla del módulo),
  se alinea con Odoo 13 (tipo, descripción, gerencia) y se informa de cada diferencia.
* No se migran: pertenencia a grupos de los usuarios, adjuntos ni mensajes (el módulo no usa
  chatter) ni ``andina.prenda`` (el modelo no está cargado en ninguna de las dos versiones).
"""
import os
import re
from decimal import Decimal

import psycopg2
import psycopg2.extras

from odoo import SUPERUSER_ID
from odoo.models import BaseModel
from odoo.sql_db import connection_info_for

OLD_DB = os.environ.get('ANDINA_OLD_DB')
OLD_DSN = os.environ.get('ANDINA_OLD_DSN')
COMMIT = os.environ.get('ANDINA_COMMIT') == '1'
BATCH = int(os.environ.get('ANDINA_BATCH') or 1000)

SEQUENCE_CODE = 'andina.lavado.industrial'
PRENDAS = [f'p{n}{turno}' for n in range(1, 17) for turno in 'abc']
LAVADO_FIELDS = [
    'comentarios', 'fecha', 'fecha_inicio', 'fecha_fin', 'precio_kilo', 'cobrar_por',
    'is_parada', 'wizard_id', 'wizard_name',
]
LINE_FIELDS = ['name', 'sequence', 'fecha', 'is_editable'] + PRENDAS
# (campo del control en Odoo 19, columna guardada en Odoo 13); se compara tras recalcular
LAVADO_TOTALS = [
    'cantidad_total', 'cantidad_turnoa', 'cantidad_turnob', 'cantidad_turnoc',
    'peso_total', 'precio_total',
]
FLOAT_TOLERANCE = 0.0011  # los importes tienen 3 decimales (1 milésima de redondeo)
AUDIT_FIELDS = ['create_uid', 'create_date', 'write_uid', 'write_date']

errors = []    # detienen la migración real
warnings = []  # se informan pero no detienen


def say(msg=''):
    print(msg, flush=True)


def clean(value):
    """psycopg2 devuelve Decimal para las columnas numeric; el ORM espera float."""
    return float(value) if isinstance(value, Decimal) else value


def open_old_db():
    if OLD_DSN:
        conn = psycopg2.connect(OLD_DSN)
    else:
        _name, info = connection_info_for(OLD_DB)
        conn = psycopg2.connect(**info)
    conn.set_session(readonly=True, autocommit=True)
    return conn


def fetch(old, sql, params=None):
    with old.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        return [{k: clean(v) for k, v in row.items()} for row in cur.fetchall()]


def table_exists(old, table):
    return bool(fetch(old, "SELECT 1 FROM information_schema.tables WHERE table_name = %s", [table]))


def vals_from(row, fields):
    """Valores a copiar; los NULL de Odoo 13 se omiten para que apliquen los defaults de Odoo 19."""
    return {f: row[f] for f in fields if row.get(f) is not None}


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


# ---------------------------------------------------------------------------
# 0. Verificaciones previas
# ---------------------------------------------------------------------------
if not OLD_DB and not OLD_DSN:
    raise RuntimeError('Defina ANDINA_OLD_DB con el nombre de la base Odoo 13 restaurada.')
if OLD_DB == env.cr.dbname:
    raise RuntimeError('ANDINA_OLD_DB no puede ser la misma base destino (%s).' % env.cr.dbname)
if not env['ir.module.module'].search_count([('name', '=', 'andina'), ('state', '=', 'installed')]):
    raise RuntimeError("El módulo 'andina' no está instalado en la base destino %s." % env.cr.dbname)

say('Modo: %s | origen: %s | destino: %s' % (
    'MIGRACIÓN REAL (commit)' if COMMIT else 'SIMULACIÓN (rollback)', OLD_DB or 'DSN', env.cr.dbname))
old = open_old_db()
for table in ('andina_gerencia', 'andina_area', 'andina_lavado_industrial', 'andina_lavado_industrial_line',
              'res_users'):
    if not table_exists(old, table):
        raise RuntimeError('La base de origen no tiene la tabla %s: ¿es la base Odoo 13 correcta?' % table)

Gerencia = env['andina.gerencia']
Area = env['andina.area']
Lavado = env['andina.lavado.industrial'].with_context(tracking_disable=True)
Line = env['andina.lavado.industrial.line'].with_context(tracking_disable=True)

old_gerencias = fetch(old, 'SELECT * FROM andina_gerencia ORDER BY id')
old_areas = fetch(old, 'SELECT * FROM andina_area ORDER BY id')
old_lavados = fetch(old, 'SELECT * FROM andina_lavado_industrial ORDER BY id')
old_lines = fetch(old, 'SELECT * FROM andina_lavado_industrial_line ORDER BY lavado_id, id')
old_logins = {r['id']: r['login'] for r in fetch(old, 'SELECT id, login FROM res_users')}

allowed_states = {key for key, _label in Lavado._fields['state'].selection}
allowed_cobrar = {key for key, _label in Lavado._fields['cobrar_por'].selection}
bad_states = {r['state'] for r in old_lavados} - allowed_states - {None}
bad_cobrar = {r['cobrar_por'] for r in old_lavados} - allowed_cobrar - {None}
if bad_states or bad_cobrar:
    raise RuntimeError('Valores no soportados en Odoo 19: state=%s cobrar_por=%s' % (bad_states, bad_cobrar))
lines_by_lavado = {}
for line in old_lines:
    lines_by_lavado.setdefault(line['lavado_id'], []).append(line)
# 'precio_subtotal' no existe en la línea: Odoo 19 no puede calcular el total de un control "por prenda" con líneas
prenda_con_lineas = [r['name'] for r in old_lavados if r['cobrar_por'] == 'prenda' and lines_by_lavado.get(r['id'])]
if prenda_con_lineas:
    raise RuntimeError("Controles con cobrar_por='prenda' y detalle (el módulo no puede calcularlos): %s"
                       % prenda_con_lineas[:10])

# ---------------------------------------------------------------------------
# 1. Usuarios: se enlazan por login
# ---------------------------------------------------------------------------
used_uids = {r[f] for r in old_lavados + old_lines + old_gerencias + old_areas
             for f in ('user_id', 'create_uid', 'write_uid') if r.get(f)}
new_users = {u.login: u.id for u in env['res.users'].with_context(active_test=False).search(
    [('login', 'in', [old_logins[uid] for uid in used_uids if uid in old_logins])])}
user_map = {uid: new_users.get(old_logins.get(uid)) for uid in used_uids}
missing_logins = sorted({old_logins.get(uid, '#%s' % uid) for uid, new in user_map.items() if not new})


def new_uid(old_uid):
    return user_map.get(old_uid) or False


# ---------------------------------------------------------------------------
# 2. Gerencias y áreas operativas (por nombre)
# ---------------------------------------------------------------------------
gerencia_by_name = {g.name: g for g in Gerencia.search([])}
gerencia_map, created_gerencias = {}, 0
for row in old_gerencias:
    rec = gerencia_by_name.get(row['name'])
    if not rec:
        rec = Gerencia.create({'name': row['name']})
        gerencia_by_name[rec.name] = rec
        created_gerencias += 1
    gerencia_map[row['id']] = rec

area_by_name = {a.name: a for a in Area.search([])}
area_map, created_areas, aligned_areas = {}, 0, 0
for row in old_areas:
    vals = {'name': row['name'], 'tipo': row['tipo'], 'gerencia_id': gerencia_map[row['gerencia_id']].id}
    if row.get('descripcion'):
        vals['descripcion'] = row['descripcion']
    rec = area_by_name.get(row['name'])
    if not rec:
        rec = Area.create(vals)
        area_by_name[rec.name] = rec
        created_areas += 1
    else:
        current = {'name': rec.name, 'tipo': rec.tipo, 'gerencia_id': rec.gerencia_id.id}
        if 'descripcion' in vals:
            current['descripcion'] = rec.descripcion
        diff = {k: v for k, v in vals.items() if current[k] != v}
        if diff:
            warnings.append('Área %r ya existía con otros datos; se alineó con Odoo 13: %s' % (rec.name, diff))
            rec.write(diff)
            aligned_areas += 1
    area_map[row['id']] = rec

# ---------------------------------------------------------------------------
# 3. Controles (cabecera). Se omite el create() del modelo porque este reemplaza
#    ``name`` por un nuevo correlativo y fuerza state='open' (correcto para altas
#    nuevas, incorrecto al migrar). El resto del ORM (computes, constraints) se mantiene.
# ---------------------------------------------------------------------------
existing_names = set(Lavado.search([('name', '!=', False)]).mapped('name'))
pending = [r for r in old_lavados if not r['name'] or r['name'] not in existing_names]
skipped_lavados = len(old_lavados) - len(pending)
lavado_map = {}  # id Odoo 13 -> id Odoo 19
sin_area = sum(1 for r in pending if r['area_id'] and r['area_id'] not in area_map)
for batch in chunks(pending, BATCH):
    vals_list = []
    for row in batch:
        vals = vals_from(row, LAVADO_FIELDS)
        vals.update(
            name=row['name'] or '',
            state=row['state'] or 'open',
            area_id=area_map[row['area_id']].id if row['area_id'] in area_map else False,
            user_id=new_uid(row['user_id']),
        )
        vals_list.append(vals)
    for row, rec in zip(batch, BaseModel.create(Lavado, vals_list)):
        lavado_map[row['id']] = rec.id
if sin_area:
    warnings.append('%s controles apuntaban a un área inexistente: quedaron sin área.' % sin_area)

# ---------------------------------------------------------------------------
# 4. Detalle por fecha. Los controles se agrupan para que cada cabecera se
#    recalcule una sola vez por lote.
# ---------------------------------------------------------------------------
old_lavado_ids = {r['id'] for r in old_lavados}
huerfanas = [ln for ln in old_lines if ln['lavado_id'] not in old_lavado_ids]
if huerfanas:
    warnings.append('%s líneas sin control (lavado_id vacío o inexistente) NO se migraron.' % len(huerfanas))
line_vals, line_old_rows = [], []
audit_lines = {}  # id nuevo -> fila Odoo 13, para restaurar las fechas de auditoría


def flush_lines():
    global line_vals, line_old_rows
    if line_vals:
        recs = Line.create(line_vals)
        audit_lines.update({rec.id: old_row for rec, old_row in zip(recs, line_old_rows)})
        env.flush_all()
        env.invalidate_all()
        line_vals, line_old_rows = [], []


for row in pending:
    for ln in lines_by_lavado.get(row['id'], []):
        vals = vals_from(ln, LINE_FIELDS)
        vals['lavado_id'] = lavado_map[row['id']]
        line_vals.append(vals)
        line_old_rows.append(ln)
    if len(line_vals) >= BATCH:
        flush_lines()
flush_lines()
env.flush_all()

# ---------------------------------------------------------------------------
# 5. Fechas y usuarios de auditoría (create/write) tal como estaban en Odoo 13
# ---------------------------------------------------------------------------
def restore_audit(table, rows_by_new_id):
    ids = list(rows_by_new_id)
    if not ids:
        return
    cols = list(zip(*[
        (i, new_uid(r.get('create_uid')) or SUPERUSER_ID, r.get('create_date'),
         new_uid(r.get('write_uid')) or SUPERUSER_ID, r.get('write_date'))
        for i, r in rows_by_new_id.items()]))
    env.cr.execute("""
        UPDATE %s t SET create_uid = v.cu, create_date = COALESCE(v.cd, t.create_date),
                        write_uid = v.wu, write_date = COALESCE(v.wd, t.write_date)
          FROM unnest(%%s::int[], %%s::int[], %%s::timestamp[], %%s::int[], %%s::timestamp[])
               AS v(id, cu, cd, wu, wd)
         WHERE t.id = v.id""" % table, [list(c) for c in cols])
    env.invalidate_all()


restore_audit('andina_lavado_industrial', {lavado_map[r['id']]: r for r in pending})
restore_audit('andina_lavado_industrial_line', audit_lines)

# ---------------------------------------------------------------------------
# 6. Conciliación contra los valores guardados en Odoo 13
# ---------------------------------------------------------------------------
env.flush_all()
mismatches = []
old_by_id = {r['id']: r for r in old_lavados}
for new_batch in chunks(sorted(lavado_map.items()), 500):
    recs = Lavado.browse([new for _old, new in new_batch])
    for (old_id, _new), rec in zip(new_batch, recs):
        row = old_by_id[old_id]
        for fname in LAVADO_TOTALS:
            expected, got = row.get(fname), rec[fname]
            if expected is not None and abs(float(expected) - float(got)) > FLOAT_TOLERANCE:
                mismatches.append((rec.name, fname, expected, got))

env.cr.execute("""
    SELECT count(*), COALESCE(sum(cantidad_subtotal), 0), COALESCE(sum(peso_subtotal), 0)
      FROM andina_lavado_industrial_line WHERE lavado_id = ANY(%s)""", [list(lavado_map.values())])
new_count, new_cant, new_peso = env.cr.fetchone()
old_migrated = [ln for r in pending for ln in lines_by_lavado.get(r['id'], [])]
old_cant = sum(ln.get('cantidad_subtotal') or 0 for ln in old_migrated)
old_peso = sum(float(ln.get('peso_subtotal') or 0) for ln in old_migrated)

if len(lavado_map) != len(pending):
    errors.append('Controles creados %s != esperados %s' % (len(lavado_map), len(pending)))
if new_count != len(old_migrated):
    errors.append('Líneas creadas %s != esperadas %s' % (new_count, len(old_migrated)))
if new_cant != old_cant:
    warnings.append('Piezas en líneas: Odoo 13=%s Odoo 19=%s' % (old_cant, new_cant))
if abs(float(new_peso) - old_peso) > FLOAT_TOLERANCE * max(1, len(old_migrated)):
    warnings.append('Kilos en líneas: Odoo 13=%.3f Odoo 19=%.3f' % (old_peso, float(new_peso)))
if mismatches:
    warnings.append('%s totales de cabecera difieren de lo guardado en Odoo 13 (se conserva el recalculado).'
                    % len(mismatches))

# ---------------------------------------------------------------------------
# 7. Secuencia: el próximo número debe continuar el de Odoo 13
# ---------------------------------------------------------------------------
def old_next_number():
    seq = fetch(old, "SELECT * FROM ir_sequence WHERE code = %s ORDER BY id LIMIT 1", [SEQUENCE_CODE])
    if not seq:
        return None, None
    seq = seq[0]
    if seq.get('implementation') == 'no_gap':
        return seq, seq['number_next']
    pg_seq = 'ir_sequence_%03d' % seq['id']
    if not fetch(old, "SELECT 1 FROM pg_class WHERE relkind = 'S' AND relname = %s", [pg_seq]):
        return seq, seq['number_next']
    last = fetch(old, 'SELECT last_value, is_called FROM "%s"' % pg_seq)[0]
    return seq, last['last_value'] + (seq['number_increment'] if last['is_called'] else 0)


old_seq, next_number = old_next_number()
new_seq = env['ir.sequence'].search([('code', '=', SEQUENCE_CODE)], limit=1)
highest_used = max((int(m.group(1)) for n in Lavado.search([]).mapped('name') if n
                    for m in [re.search(r'(\d+)$', n)] if m), default=0)
if not new_seq:
    errors.append('No existe la secuencia %s en destino.' % SEQUENCE_CODE)
elif next_number is None:
    next_number = highest_used + 1
    warnings.append('Sin secuencia en Odoo 13: el próximo número será %s.' % next_number)
else:
    if (old_seq['prefix'], old_seq['padding']) != (new_seq.prefix, new_seq.padding):
        warnings.append('Prefijo/relleno distinto: Odoo 13=%r/%s Odoo 19=%r/%s' % (
            old_seq['prefix'], old_seq['padding'], new_seq.prefix, new_seq.padding))
    if next_number <= highest_used:
        warnings.append('La secuencia de Odoo 13 (%s) estaba por detrás del mayor número usado (%s): se ajusta.'
                        % (next_number, highest_used))
        next_number = highest_used + 1

# ---------------------------------------------------------------------------
# 8. Reporte y cierre
# ---------------------------------------------------------------------------
say('\n=== RESUMEN ===')
say('Gerencias : origen %-5s creadas %s' % (len(old_gerencias), created_gerencias))
say('Áreas     : origen %-5s creadas %s, alineadas %s' % (len(old_areas), created_areas, aligned_areas))
say('Controles : origen %-5s migrados %s, omitidos por ya existir %s' % (
    len(old_lavados), len(lavado_map), skipped_lavados))
say('Detalle   : migradas %s líneas (piezas %s, kilos %.3f)' % (new_count, new_cant, float(new_peso)))
say('Secuencia : próximo número en Odoo 13 = %s' % next_number)
if missing_logins:
    say('Usuarios sin equivalente en destino (quedan sin responsable): %s' % ', '.join(missing_logins))
for w in warnings:
    say('AVISO  : %s' % w)
for name, fname, expected, got in mismatches[:20]:
    say('  difiere %s.%s: Odoo 13=%s Odoo 19=%s' % (name, fname, expected, got))
for e in errors:
    say('ERROR  : %s' % e)

if errors:
    raise RuntimeError('Migración abortada (rollback): %s' % '; '.join(errors))
if COMMIT:
    new_seq.number_next_actual = next_number
    env.cr.commit()
    say('\nOK: cambios guardados. Próximo control: %s' % new_seq.get_next_char(next_number))
else:
    env.cr.rollback()
    say('\nSimulación terminada SIN guardar. Agregue ANDINA_COMMIT=1 para migrar de verdad.')
old.close()
