import os, zipfile, xml.etree.ElementTree as ET, re, json

vendas_folder = r'C:\Users\NTI\Documents\VENDAS'
semanal_folder = r'C:\Users\NTI\Documents\SEMANAL'

MONTH_ORDER = [
    ('2025-11', 'Nov/2025'),
    ('2025-12', 'Dez/2025'),
    ('2026-01', 'Jan/2026'),
    ('2026-02', 'Fev/2026'),
    ('2026-03', 'Mar/2026'),
    ('2026-04', 'Abr/2026'),
    ('2026-05', 'Mai/2026'),
    ('2026-06', 'Jun/2026'),
    ('2026-07', 'Jul/2026'),
    ('2026-08', 'Ago/2026'),
    ('2026-09', 'Set/2026'),
    ('2026-10', 'Out/2026'),
]

# Default calendar week ranges per month when not specified in SEMANAL
DEFAULT_MONTH_WEEKS = {
    '2025-11': [(1,2), (3,9), (10,16), (17,23), (24,30)],
    '2025-12': [(1,7), (8,14), (15,21), (22,28), (29,31)],
    '2026-01': [(1,4), (5,11), (12,18), (19,25), (26,31)],
    '2026-02': [(1,8), (9,15), (16,22), (23,28)],
    '2026-03': [(1,8), (9,15), (16,22), (23,29), (30,31)],
    '2026-04': [(1,5), (6,12), (13,19), (20,26), (27,30)],
    '2026-05': [(1,3), (4,10), (11,17), (18,24), (25,31)],
    '2026-06': [(1,7), (8,14), (15,21), (22,28), (29,30)],
    '2026-07': [(1,5), (6,12), (13,19), (20,26), (27,31)],
    '2026-08': [(1,2), (3,9), (10,16), (17,23), (24,31)],
    '2026-09': [(1,6), (7,13), (14,20), (21,27), (28,30)],
    '2026-10': [(1,4), (5,11), (12,18), (19,25), (26,31)],
    '2026-11': [(1,1), (2,8), (9,15), (16,22), (23,30)],
    '2026-12': [(1,6), (7,13), (14,20), (21,27), (28,31)],
}

SEMANAL_FILE_MAP = {
    'DK_Brotas_2026_Semanal.xlsx': 'BROTAS DK',
    'Lauro _DK_2026 Semanal.xlsx': 'LAURO',
    'Norte_2026_Semanal.xlsx': 'SSA NORTE',
    'Ondina_2026_Semanal.xlsx': 'ONDINA',
    'Paralela_2026_Semanal.xlsx': 'PARALELA',
    'Paseo_2026_Semanal.xlsx': 'PASEO',
    'Pituba_2026_Semanal.xlsx': 'PITUBA',
    'SSA_2026_Semanal.xlsx': 'SSA',
}

PRETTY_NAMES = {
    'BROTAS DK': 'Brotas DK',
    'LAURO': 'Lauro',
    'ONDINA': 'Ondina',
    'PARALELA': 'Paralela',
    'PASEO': 'Paseo',
    'PITUBA': 'Pituba',
    'SSA NORTE': 'SSA Norte',
    'SSA': 'SSA'
}

def normalize_month(sheet_name):
    s = sheet_name.lower()
    if any(w in s for w in ['plano', 'manuten', 'embalagen', 'trimestral']):
        return None
    y = '2025' if '2025' in s else ('2026' if '2026' in s else '')
    if not y: return None
    if 'nov' in s: return f'{y}-11'
    if 'dez' in s: return f'{y}-12'
    if 'jan' in s: return f'{y}-01'
    if 'fev' in s: return f'{y}-02'
    if 'mar' in s: return f'{y}-03'
    if 'abr' in s: return f'{y}-04'
    if 'mai' in s: return f'{y}-05'
    if 'jun' in s: return f'{y}-06'
    if 'jul' in s: return f'{y}-07'
    if 'ago' in s: return f'{y}-08'
    if 'set' in s: return f'{y}-09'
    if 'out' in s: return f'{y}-10'
    return None

def to_float(v):
    if v is None: return 0.0
    try:
        s = str(v).strip()
        if not s: return 0.0
        return round(float(s), 2)
    except:
        return 0.0

def parse_week_range(label, default_ranges, idx):
    fallback = default_ranges[idx] if idx < len(default_ranges) else (29, 31)
    if not label:
        return fallback
    nums = [int(x) for x in re.findall(r'\d+', label)]
    if len(nums) >= 2:
        return (nums[0], nums[1])
    elif len(nums) == 1:
        return (nums[0], nums[0])
    return fallback

def parse_semanal_file(fp, unit_key):
    months_meta = {}
    with zipfile.ZipFile(fp, 'r') as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            root = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                strings.append(''.join(node.text or '' for node in si.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')))
        wb_root = ET.fromstring(z.read('xl/workbook.xml'))
        rels_root = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rels = {r.attrib['Id']: r.attrib['Target'] for r in rels_root}
        for sh in wb_root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
            sh_name = sh.attrib.get('name', '')
            m_key = normalize_month(sh_name)
            if not m_key: continue
            rid = sh.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            target = 'xl/' + rels[rid].lstrip('/')
            if target not in z.namelist(): target = rels[rid].lstrip('/')
            ws_root = ET.fromstring(z.read(target))
            rows = {}
            for row in ws_root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
                r_idx = int(row.attrib.get('r'))
                if r_idx > 25: continue
                vals = {}
                for c in row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                    col = re.sub(r'\d+', '', c.attrib.get('r'))
                    t = c.attrib.get('t')
                    v_node = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                    is_node = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}is')
                    val = None
                    if v_node is not None and v_node.text is not None:
                        val = strings[int(v_node.text)] if t == 's' else v_node.text
                    elif is_node is not None:
                        val = ''.join(n.text or '' for n in is_node.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'))
                    if val is not None:
                        vals[col] = val.strip()
                if vals: rows[r_idx] = vals
            
            sem_row = {}
            for r_i, rv in rows.items():
                if 'semana' in str(rv.get('E', '')).lower():
                    sem_row = rv
                    break
            
            default_ranges = DEFAULT_MONTH_WEEKS.get(m_key, [(1,7),(8,14),(15,21),(22,28),(29,31)])
            week_cols = [('E', 'F'), ('I', 'J'), ('P', 'Q'), ('W', 'X'), ('AD', 'AE')]
            
            row_total = {}
            row_salao = {}
            row_deliv = {}
            row_zapy = {}
            for r_i, rv in sorted(rows.items()):
                desc = rv.get('C', '').lower().strip()
                if desc == 'receita total':
                    row_total = rv
                elif 'receita sal' in desc or 'receita delivery volpi' in desc:
                    row_salao = rv
                elif desc in ('receita delivery', 'receita delivery bella parme'):
                    if not row_deliv:
                        row_deliv = rv
                elif 'receita zapy' in desc or 'receita delivery zapy' in desc:
                    row_zapy = rv
            
            weeks_data = []
            sum_mt, sum_ms, sum_md, sum_mz = 0.0, 0.0, 0.0, 0.0
            for idx, (mc, rc) in enumerate(week_cols):
                lbl = sem_row.get(mc, '')
                if not lbl and idx >= len(default_ranges):
                    # e.g. Feb has 4 weeks
                    weeks_data.append({
                        'week': f'W{idx+1}',
                        'label': f'Semana {idx+1}',
                        'min_day': 29,
                        'max_day': 31,
                        'meta_cantina': 0.0,
                        'meta_total': 0.0,
                        'meta_deliv': 0.0,
                        'meta_zapy': 0.0
                    })
                    continue
                dmin, dmax = parse_week_range(lbl, default_ranges, idx)
                mt = to_float(row_total.get(mc))
                ms = to_float(row_salao.get(mc))
                md = to_float(row_deliv.get(mc))
                mz = to_float(row_zapy.get(mc))
                sum_mt += mt
                sum_ms += ms
                sum_md += md
                sum_mz += mz
                weeks_data.append({
                    'week': f'W{idx+1}',
                    'label': lbl or f'Semana {idx+1} ({dmin}–{dmax})',
                    'min_day': dmin,
                    'max_day': dmax,
                    'meta_cantina': round(ms, 2),
                    'meta_total': round(mt, 2),
                    'meta_deliv': round(md, 2),
                    'meta_zapy': round(mz, 2)
                })
            
            tot_mt = round(sum_mt, 2) or to_float(row_total.get('AG')) or to_float(row_total.get('Z'))
            tot_ms = round(sum_ms, 2) or to_float(row_salao.get('AG')) or to_float(row_salao.get('Z'))
            tot_md = round(sum_md, 2) or to_float(row_deliv.get('AG')) or to_float(row_deliv.get('Z'))
            tot_mz = round(sum_mz, 2) or to_float(row_zapy.get('AG')) or to_float(row_zapy.get('Z'))
            
            months_meta[m_key] = {
                'meta_cantina': tot_ms,
                'meta_total': tot_mt,
                'meta_deliv': tot_md,
                'meta_zapy': tot_mz,
                'weeks': weeks_data
            }
    return months_meta

all_semanal = {}
for fn, u_key in SEMANAL_FILE_MAP.items():
    fp = os.path.join(semanal_folder, fn)
    if os.path.exists(fp):
        all_semanal[u_key] = parse_semanal_file(fp, u_key)

# Complement LAURO from SSA NORTE Semanal (Jun W3-W5 and Jul-Dec) where Lauro's delivery metas are stored
if 'LAURO' in all_semanal and 'SSA NORTE' in all_semanal:
    lauro_sem = all_semanal['LAURO']
    norte_sem = all_semanal['SSA NORTE']
    for m_key, n_m in norte_sem.items():
        if m_key == '2026-06' and '2026-06' in lauro_sem:
            # Fill W3, W4, W5 of June for Lauro from Norte's delivery
            l_m = lauro_sem['2026-06']
            for idx in range(2, 5):
                nw = n_m['weeks'][idx]
                l_m['weeks'][idx]['meta_cantina'] = nw['meta_deliv']
                l_m['weeks'][idx]['meta_total'] = round(nw['meta_deliv'] + nw['meta_zapy'], 2)
                l_m['weeks'][idx]['label'] = nw['label']
                l_m['weeks'][idx]['min_day'] = nw['min_day']
                l_m['weeks'][idx]['max_day'] = nw['max_day']
            l_m['meta_cantina'] = round(sum(w['meta_cantina'] for w in l_m['weeks']), 2)
            l_m['meta_total'] = round(sum(w['meta_total'] for w in l_m['weeks']), 2)
        elif m_key >= '2026-07' and m_key not in lauro_sem:
            w_list = []
            for nw in n_m['weeks']:
                mc = nw['meta_deliv']
                mt = round(nw['meta_deliv'] + nw['meta_zapy'], 2)
                w_list.append({
                    'week': nw['week'],
                    'label': nw['label'],
                    'min_day': nw['min_day'],
                    'max_day': nw['max_day'],
                    'meta_cantina': mc,
                    'meta_total': mt,
                    'meta_deliv': nw['meta_zapy'],
                    'meta_zapy': nw['meta_zapy']
                })
            lauro_sem[m_key] = {
                'meta_cantina': round(sum(w['meta_cantina'] for w in w_list), 2),
                'meta_total': round(sum(w['meta_total'] for w in w_list), 2),
                'meta_deliv': round(sum(w['meta_deliv'] for w in w_list), 2),
                'meta_zapy': round(sum(w['meta_zapy'] for w in w_list), 2),
                'weeks': w_list
            }

def parse_vendas_file(filepath, filename):
    unit_key = filename.replace('.xlsx', '').replace(' (1)', '').replace(' ATUALIZADA', '').replace('-VENDAS', '').replace(' VENDAS', '').strip().upper()
    is_dk = unit_key in ('BROTAS DK', 'LAURO')
    unit_semanal = all_semanal.get(unit_key, {})
    
    with zipfile.ZipFile(filepath, 'r') as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            root = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                strings.append(''.join(node.text or '' for node in si.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')))
        wb_root = ET.fromstring(z.read('xl/workbook.xml'))
        rels_root = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rels = {r.attrib['Id']: r.attrib['Target'] for r in rels_root}
        
        months_data = {}
        for sh in wb_root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
            if sh.attrib.get('state', 'visible') != 'visible':
                continue
            sh_name = sh.attrib.get('name', '')
            m_key = normalize_month(sh_name)
            if not m_key:
                continue
            rid = sh.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            target = 'xl/' + rels[rid].lstrip('/')
            if target not in z.namelist():
                target = rels[rid].lstrip('/')
            ws_root = ET.fromstring(z.read(target))
            rows = {}
            for row in ws_root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
                r_idx = int(row.attrib.get('r'))
                vals = {}
                for c in row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                    ref = c.attrib.get('r')
                    col = re.sub(r'\d+', '', ref)
                    t = c.attrib.get('t')
                    v_node = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                    is_node = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}is')
                    val = None
                    if v_node is not None and v_node.text is not None:
                        val = strings[int(v_node.text)] if t == 's' else v_node.text
                    elif is_node is not None:
                        val = ''.join(n.text or '' for n in is_node.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'))
                    if val is not None:
                        vals[col] = val.strip()
                if vals:
                    rows[r_idx] = vals
            
            r1_title = rows.get(1, {}).get('A', '').strip()
            h3 = {k: v.replace('\n', ' ').strip() for k, v in rows.get(3, {}).items()}
            
            is_template_copy = False
            if unit_key == 'BROTAS DK' and 'LAURO' in r1_title.upper():
                is_template_copy = True
            if unit_key == 'SSA NORTE' and r1_title.upper().endswith('- SSA'):
                is_template_copy = True
            
            # Identify extra delivery columns for DKs (BP Dia, BP Noite, Zapy Noite)
            dk_dia_cols = []
            dk_noite_cols = []
            if is_dk:
                for col_k, col_title in h3.items():
                    if col_k in ('D', 'F'): continue
                    up = col_title.upper()
                    if 'VENDA' in up and 'TOTAL' not in up and 'DIFEREN' not in up and 'PROMO' not in up:
                        if 'DIA' in up:
                            dk_dia_cols.append(col_k)
                        elif 'NOITE' in up:
                            dk_noite_cols.append(col_k)
            
            daily = []
            sum_qtd_dia = 0.0
            sum_venda_dia = 0.0
            sum_qtd_noite = 0.0
            sum_venda_noite = 0.0
            sum_deliv_dia = 0.0
            sum_deliv_noite = 0.0
            
            for r in range(4, 35):
                rv = rows.get(r, {})
                day_num = rv.get('A', '')
                day_name = rv.get('B', '')
                if not day_num or not day_num.isdigit():
                    continue
                q_dia = to_float(rv.get('C'))
                v_dia = to_float(rv.get('D'))
                q_noite = to_float(rv.get('E'))
                v_noite = to_float(rv.get('F'))
                
                if not is_dk:
                    deliv_dia = to_float(rv.get('H'))
                    deliv_noite = to_float(rv.get('J'))
                else:
                    deliv_dia = round(sum(to_float(rv.get(c)) for c in dk_dia_cols), 2)
                    deliv_noite = round(sum(to_float(rv.get(c)) for c in dk_noite_cols), 2)
                
                sum_qtd_dia += q_dia
                sum_venda_dia += v_dia
                sum_qtd_noite += q_noite
                sum_venda_noite += v_noite
                sum_deliv_dia += deliv_dia
                sum_deliv_noite += deliv_noite
                
                daily.append({
                    'dia': int(day_num),
                    'dia_semana': day_name,
                    'qtd_dia': q_dia,
                    'venda_dia': v_dia,
                    'qtd_noite': q_noite,
                    'venda_noite': v_noite,
                    'deliv_dia': deliv_dia,
                    'deliv_noite': deliv_noite
                })
            
            # Match Semanal Meta for this month
            sem_m = unit_semanal.get(m_key) if not is_template_copy else None
            default_ranges = DEFAULT_MONTH_WEEKS.get(m_key, [(1,7),(8,14),(15,21),(22,28),(29,31)])
            
            if sem_m:
                meta_cantina = sem_m['meta_cantina']
                # For SSA NORTE, since SSA NORTE VENDAS only has Salão (Lauro has the Delivery),
                # keep meta_total_own = meta_cantina, and also store meta_total_semanal
                meta_total = sem_m['meta_cantina'] if unit_key == 'SSA NORTE' else sem_m['meta_total']
                meta_total_full = sem_m['meta_total']
                weeks_meta = []
                for w in sem_m['weeks']:
                    weeks_meta.append({
                        'week': w['week'],
                        'label': w['label'],
                        'min_day': w['min_day'],
                        'max_day': w['max_day'],
                        'meta_cantina': w['meta_cantina'],
                        'meta_total': w['meta_cantina'] if unit_key == 'SSA NORTE' else w['meta_total'],
                        'meta_total_full': w['meta_total']
                    })
            else:
                meta_cantina = 0.0
                meta_total = 0.0
                meta_total_full = 0.0
                weeks_meta = []
                for idx in range(5):
                    if idx < len(default_ranges):
                        dmin, dmax = default_ranges[idx]
                        lbl = f'Semana {idx+1} ({dmin}–{dmax})'
                    else:
                        dmin, dmax = 29, 31
                        lbl = f'Semana {idx+1}'
                    weeks_meta.append({
                        'week': f'W{idx+1}',
                        'label': lbl,
                        'min_day': dmin,
                        'max_day': dmax,
                        'meta_cantina': 0.0,
                        'meta_total': 0.0,
                        'meta_total_full': 0.0
                    })
            
            months_data[m_key] = {
                'sheet_name': sh_name,
                'r1_title': r1_title,
                'is_template_copy': is_template_copy,
                'qtd_dia': round(sum_qtd_dia, 2),
                'venda_dia': round(sum_venda_dia, 2),
                'qtd_noite': round(sum_qtd_noite, 2),
                'venda_noite': round(sum_venda_noite, 2),
                'deliv_dia': round(sum_deliv_dia, 2),
                'deliv_noite': round(sum_deliv_noite, 2),
                'meta_cantina': round(meta_cantina, 2),
                'meta_total': round(meta_total, 2),
                'meta_total_full': round(meta_total_full, 2),
                'weeks_meta': weeks_meta,
                'daily': daily
            }
            
        sem_nov26 = unit_semanal.get('2026-11')
        is_ref_oct = False
        if not sem_nov26 and unit_semanal.get('2026-10'):
            sem_nov26 = unit_semanal.get('2026-10')
            is_ref_oct = True
        
        if sem_nov26:
            nov2026_meta = {
                'meta_cantina': round(sem_nov26['meta_cantina'], 2),
                'meta_total': round(sem_nov26['meta_cantina'] if unit_key == 'SSA NORTE' else sem_nov26['meta_total'], 2),
                'meta_total_full': round(sem_nov26['meta_total'], 2),
                'meta_deliv': round(sem_nov26.get('meta_deliv', 0.0) + sem_nov26.get('meta_zapy', 0.0), 2),
                'is_ref_oct': is_ref_oct,
                'weeks': sem_nov26.get('weeks', [])
            }
        else:
            nov2026_meta = {
                'meta_cantina': 0.0,
                'meta_total': 0.0,
                'meta_total_full': 0.0,
                'meta_deliv': 0.0,
                'is_ref_oct': False,
                'weeks': []
            }

        return {
            'unit': PRETTY_NAMES.get(unit_key, unit_key.title()),
            'unit_key': unit_key,
            'is_dk': is_dk,
            'has_semanal': unit_key in all_semanal,
            'nov2026_meta': nov2026_meta,
            'months': months_data
        }

all_units = []
for f in sorted(os.listdir(vendas_folder)):
    if f.endswith('.xlsx') and not f.startswith('~$'):
        all_units.append(parse_vendas_file(os.path.join(vendas_folder, f), f))

out_path = r'C:\Users\NTI\Documents\VENDAS\scripts\vendas_metas_data.json'
with open(out_path, 'w', encoding='utf-8') as out:
    json.dump({'month_order': MONTH_ORDER, 'default_month_weeks': DEFAULT_MONTH_WEEKS, 'units': all_units}, out, ensure_ascii=False)

print("Saved vendas_metas_data.json successfully!")
for u in all_units:
    v_sal = sum(m['venda_dia'] + m['venda_noite'] for m in u['months'].values() if not m['is_template_copy'])
    m_sal = sum(m['meta_cantina'] for m in u['months'].values() if not m['is_template_copy'])
    v_tot = sum(m['venda_dia'] + m['venda_noite'] + m['deliv_dia'] + m['deliv_noite'] for m in u['months'].values() if not m['is_template_copy'])
    m_tot = sum(m['meta_total'] for m in u['months'].values() if not m['is_template_copy'])
    print(f"{u['unit']:12s} | Cantina: Real={v_sal:12,.2f} Meta={m_sal:12,.2f} | Total: Real={v_tot:12,.2f} Meta={m_tot:12,.2f}")

