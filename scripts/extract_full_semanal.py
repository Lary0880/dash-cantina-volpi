import os, zipfile, xml.etree.ElementTree as ET, re, json

semanal_folder = r'C:\Users\NTI\Documents\SEMANAL'
vendas_json_path = r'C:\Users\NTI\Documents\VENDAS\scripts\vendas_metas_data.json'

SEMANAL_FILES = [
    ('Ondina', 'ONDINA', 'Ondina_2026_Semanal.xlsx', False),
    ('Pituba', 'PITUBA', 'Pituba_2026_Semanal.xlsx', False),
    ('Paralela', 'PARALELA', 'Paralela_2026_Semanal.xlsx', False),
    ('Paseo', 'PASEO', 'Paseo_2026_Semanal.xlsx', False),
    ('SSA', 'SSA', 'SSA_2026_Semanal.xlsx', False),
    ('SSA Norte', 'SSA NORTE', 'Norte_2026_Semanal.xlsx', False),
    ('Lauro', 'LAURO', 'Lauro _DK_2026 Semanal.xlsx', True),
    ('Brotas DK', 'BROTAS DK', 'DK_Brotas_2026_Semanal.xlsx', True),
]

NAME_NORMALIZATION = {
    'CMV - A&B + Emabalagens': 'CMV - A&B + Embalagens',
    'Alavacagem Delivery': 'Alavancagem Delivery',
    'Custo Beneficio': 'Custo Benefício',
    'Receita Rodizio': 'Receita Rodízio',
    'Qtde Triadvisor': 'Qtde Tripadvisor',
    'Desconto': 'Descontos',
    'Desligamento': 'Desligamentos',
    'Cliente Oculto Geral': 'Cliente Oculto',
    'ALAVANCAMENTO': 'Alavancamento (%)',
}

def normalize_month(sheet_name):
    s = sheet_name.lower()
    if any(w in s for w in ['plano', 'manuten', 'embalagen', 'trimestral']):
        return None
    y = '2025' if '2025' in s else ('2026' if '2026' in s else '')
    if not y: return None
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
    if 'nov' in s: return f'{y}-11'
    if 'dez' in s: return f'{y}-12'
    return None

def parse_num(v):
    if v is None: return None
    s = str(v).strip()
    if not s or s in ('-', ' - ', '#DIV/0!', '#VALUE!', '#REF!', 'N/A', '#N/A'):
        return None
    try:
        return round(float(s), 6)
    except:
        return None

def classify_indicator(cat, name):
    n = name.lower().strip()
    if '%' in n or n in ('cmv - compras (%)', 'alavancamento (%)', 'tempo kds'):
        return 'percent_dec'
    if cat == 'QUALIDADE' and any(k in n for k in ['cancelamento', 'chamados']):
        return 'percent_dec'
    if any(k in n for k in [
        'receita', 'ticket', 'cmv - a&b', 'total embalagens + a&b',
        'compras alimentos', 'embalagens/descart', 'material de limpeza',
        'manutenção variável', 'descontos', 'cancelamento', 'alavancagem'
    ]):
        return 'currency'
    if any(k in n for k in [
        'nps', 'nota ', 'estrutura física', 'restaurante ', 'cliente oculto',
        'custo benefício', 'qualidade do produto', 'sugestão de vendas', 'roi'
    ]):
        return 'score'
    return 'integer'

def is_lower_better(cat, name):
    n = name.lower().strip()
    if cat == 'CUSTOS':
        if 'roi' in n:
            return False
        return True
    if cat == 'QUALIDADE':
        if any(k in n for k in ['chamados', 'cancelamento', 'reentregas', 'tempo kds']):
            return True
    return False

def parse_semanal_workbook(fp, unit_name, unit_key, is_dk):
    months_out = {}
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
                if vals:
                    rows[r_idx] = vals
            
            sem_row = {}
            for r_i, rv in sorted(rows.items()):
                if 'semana' in str(rv.get('E', '')).lower():
                    sem_row = rv
                    break
            
            week_cols = [
                ('W1', 'E', 'F', 'G'),
                ('W2', 'I', 'J', 'K'),
                ('W3', 'P', 'Q', 'R'),
                ('W4', 'W', 'X', 'Y'),
                ('W5', 'AD', 'AE', 'AF'),
            ]
            
            week_headers = {}
            for w_code, mc, rc, vc in week_cols:
                lbl = sem_row.get(mc, '')
                week_headers[w_code] = lbl or w_code.replace('W', 'Semana ')
            
            categories = {
                'VENDAS': [],
                'QUALIDADE': [],
                'CUSTOS': []
            }
            
            curr_cat = None
            for r_i, rv in sorted(rows.items()):
                b_val = rv.get('B', '').upper().strip()
                c_raw = rv.get('C', '').strip()
                if b_val in ('VENDAS', 'QUALIDADE', 'CUSTOS', 'CUSTO'):
                    curr_cat = 'CUSTOS' if b_val == 'CUSTO' else b_val
                if not curr_cat or not c_raw:
                    continue
                if c_raw.upper() in ('DESCRIÇÃO', 'DESCRICAO', 'INDICADORES'):
                    continue
                raw_e = rv.get('E', '')
                if raw_e and parse_num(raw_e) is None and not raw_e.startswith('#'):
                    continue
                if curr_cat == 'CUSTOS' and c_raw in ('QTD Buffet', 'Ticket Médio', 'Receita do Buffet'):
                    continue
                
                c_val = NAME_NORMALIZATION.get(c_raw, c_raw)
                fmt_type = classify_indicator(curr_cat, c_val)
                low_better = is_lower_better(curr_cat, c_val)
                
                w_dict = {}
                valid_metas = []
                valid_reals = []
                for w_code, mc, rc, vc in week_cols:
                    m_val = parse_num(rv.get(mc))
                    r_val = parse_num(rv.get(rc))
                    v_val = parse_num(rv.get(vc))
                    w_dict[w_code] = {
                        'meta': m_val,
                        'real': r_val,
                        'var': v_val
                    }
                    if m_val is not None: valid_metas.append(m_val)
                    if r_val is not None and r_val != 0: valid_reals.append(r_val)
                
                acum_m = parse_num(rv.get('AG'))
                acum_r = parse_num(rv.get('AH'))
                acum_v = parse_num(rv.get('AI'))
                if acum_m is None and acum_r is None:
                    acum_m = parse_num(rv.get('Z'))
                    acum_r = parse_num(rv.get('AA'))
                    acum_v = parse_num(rv.get('AB'))
                
                # If Acumulado is missing/zero in sheet, compute fallback from weeks
                is_avg_metric = fmt_type in ('percent_dec', 'score') or 'ticket' in c_val.lower()
                if (acum_m is None or acum_m == 0) and valid_metas:
                    acum_m = round(sum(valid_metas)/len(valid_metas) if is_avg_metric else sum(valid_metas), 4)
                if (acum_r is None or acum_r == 0) and valid_reals:
                    acum_r = round(sum(valid_reals)/len(valid_reals) if is_avg_metric else sum(valid_reals), 4)
                
                categories[curr_cat].append({
                    'name': c_val,
                    'format': fmt_type,
                    'lower_is_better': low_better,
                    'is_avg': is_avg_metric,
                    'weeks': w_dict,
                    'acum': {
                        'meta': acum_m,
                        'real': acum_r,
                        'var': acum_v
                    }
                })
            
            months_out[m_key] = {
                'sheet_name': sh_name,
                'week_headers': week_headers,
                'categories': categories
            }
    return {
        'unit': unit_name,
        'unit_key': unit_key,
        'is_dk': is_dk,
        'months': months_out
    }

semanal_units = []
for u_name, u_key, fn, is_dk in SEMANAL_FILES:
    fp = os.path.join(semanal_folder, fn)
    if os.path.exists(fp):
        semanal_units.append(parse_semanal_workbook(fp, u_name, u_key, is_dk))

# Check which months have non-zero Realizado across units
month_real_counts = {}
for su in semanal_units:
    for mk, mdata in su['months'].items():
        cnt = 0
        for cat_list in mdata['categories'].values():
            for item in cat_list:
                if item['acum']['real'] and item['acum']['real'] > 0:
                    cnt += 1
        month_real_counts[mk] = month_real_counts.get(mk, 0) + cnt

print("Realizado counts by month across all 7 units:")
for mk, cnt in sorted(month_real_counts.items()):
    print(f"  {mk}: {cnt} filled indicators")

with open(vendas_json_path, 'r', encoding='utf-8') as f:
    combined = json.load(f)

combined['semanal_units'] = semanal_units

with open(vendas_json_path, 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False)

print("Successfully saved updated vendas_metas_data.json!")

