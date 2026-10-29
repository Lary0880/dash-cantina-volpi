import json, os

json_path = r'C:\Users\NTI\Documents\VENDAS\scripts\vendas_metas_data.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data_js = json.dumps(data, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cantina Volpi — Painel de Vendas & Metas Semanais</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@600;700;800&family=Mulish:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    /* ==========================================================================
       CANTINA VOLPI — DESIGN SYSTEM OFICIAL (tokens.css + bundle.css)
       Verde Pantone 350 C (#254C25) · Vermelho Pantone 200 C (#C92535) · Paper (#FBF7EF)
       ========================================================================== */
    :root {{
      --green-50: #eef4ee;
      --green-100: #dce8dc;
      --green-200: #bcd5bc;
      --green-300: #88b388;
      --green-400: #5c945c;
      --green-500: #3c763c;
      --green-600: #2f5e2f;
      --green-700: #254c25;
      --green-800: #1d451d;
      --green-900: #173817;
      --green-950: #102810;

      --red-50: #fdeff1;
      --red-100: #fbdfe2;
      --red-200: #f6c8cd;
      --red-300: #f0a0a8;
      --red-400: #ea7782;
      --red-500: #e2515f;
      --red-600: #d83a49;
      --red-700: #c92535;
      --red-800: #a51b29;
      --red-900: #84141f;
      --red-950: #5e0f17;

      --gold-100: #faecca;
      --gold-300: #f0c878;
      --gold-500: #e0a233;
      --gold-700: #976816;
      --gold-800: #8a5f13;

      --white: #ffffff;
      --paper: #fbf7ef;
      --ink-50: #f6f1e7;
      --ink-100: #ece5d7;
      --ink-200: #ddd5c6;
      --ink-300: #c2b9a9;
      --ink-400: #9d9384;
      --ink-500: #7c7263;
      --ink-600: #5d5446;
      --ink-700: #423b30;
      --ink-800: #2d2820;
      --ink-900: #1f1b16;
      --ink-950: #161310;
      --black: #100d0a;

      --color-primary: var(--green-700);
      --color-primary-hover: var(--green-800);
      --color-primary-active: var(--green-900);
      --color-primary-soft: var(--green-50);
      --color-on-primary: var(--white);

      --color-accent: var(--red-700);
      --color-accent-hover: var(--red-800);
      --color-accent-active: var(--red-900);
      --color-accent-soft: var(--red-50);
      --color-on-accent: var(--white);

      --surface-page: var(--paper);
      --surface-card: var(--white);
      --surface-raised: var(--white);
      --surface-sunken: var(--ink-50);
      --surface-inverse: var(--green-700);
      --surface-inverse-deep: var(--green-900);
      --surface-accent: var(--red-700);

      --text-heading: var(--ink-900);
      --text-body: var(--ink-800);
      --text-muted: var(--ink-500);
      --text-subtle: var(--ink-400);
      --text-on-green: #f3f8f3;

      --border-subtle: var(--ink-100);
      --border-default: var(--ink-200);
      --border-strong: var(--ink-300);
      --border-on-green: rgba(255,255,255,0.18);

      --shadow-xs: 0 1px 2px rgba(31,27,22,0.06);
      --shadow-sm: 0 1px 3px rgba(31,27,22,0.10), 0 1px 2px rgba(31,27,22,0.06);
      --shadow-md: 0 6px 16px rgba(31,27,22,0.08), 0 2px 4px rgba(31,27,22,0.05);
      --shadow-lg: 0 14px 32px rgba(31,27,22,0.12), 0 4px 8px rgba(31,27,22,0.06);
      --shadow-green: 0 12px 28px rgba(37,76,37,0.22);
      --focus-ring: 0 0 0 3px rgba(37,76,37,0.28);

      --radius-xs: 4px;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --radius-xl: 26px;
      --radius-pill: 999px;

      --font-display: "Hanken Grotesk", system-ui, sans-serif;
      --font-text: "Mulish", system-ui, sans-serif;
      --font-mono: "IBM Plex Mono", ui-monospace, monospace;
      --tricolore: linear-gradient(90deg, #254c25 0 33.333%, #ffffff 33.333% 66.666%, #c92535 66.666% 100%);

      /* Aliases de compatibilidade do Dashboard */
      --bg: var(--surface-page);
      --bg-card: var(--surface-card);
      --bg-dark: var(--ink-50);
      --bg-hover: #f3ede0;
      --border: var(--ink-200);
      --text: var(--ink-900);
      --vendas-color: var(--green-700);
      --vendas-bg: var(--green-50);
      --qual-color: #2f6db0;
      --qual-bg: #e7f0f9;
      --custo-color: var(--red-700);
      --custo-bg: var(--red-50);
      --meta-color: var(--gold-700);
      --meta-bg: var(--gold-100);
      --dia-color: var(--gold-700);
      --dia-bg: var(--gold-100);
      --noite-color: var(--green-700);
      --noite-bg: var(--green-50);
      --success: var(--green-600);
      --warning: var(--gold-700);
      --danger: var(--red-700);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font-text);
      background-color: var(--surface-page);
      color: var(--text-body);
      line-height: 1.5;
      padding-bottom: 64px;
      -webkit-font-smoothing: antialiased;
    }}

    /* Cabeçalho Oficial Cantina Volpi (Verde #254C25 + Fio Tricolore) */
    header {{
      background: var(--green-700);
      color: var(--white);
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: var(--shadow-green);
    }}
    .header-inner {{
      max-width: 1600px;
      margin: 0 auto;
      padding: 16px 28px 12px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 22px;
    }}
    .brand-logo {{
      height: 64px;
      width: auto;
      object-fit: contain;
      flex: none;
      filter: drop-shadow(0 2px 6px rgba(16,13,10,0.22));
    }}
    .brand-text {{
      border-left: 2px solid rgba(255, 255, 255, 0.22);
      padding-left: 20px;
    }}
    .brand-eyebrow {{
      font-family: var(--font-text);
      font-weight: 800;
      font-size: 0.72rem;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: var(--gold-300);
      margin-bottom: 4px;
    }}
    .brand h1 {{
      font-family: var(--font-display);
      font-size: 1.48rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--white);
      line-height: 1.1;
    }}
    .brand p {{
      font-family: var(--font-text);
      font-size: 0.84rem;
      font-weight: 500;
      color: var(--green-200);
      margin-top: 3px;
    }}

    /* Navegação Principal (CategoryTabs estilo pill Cantina Volpi) */
    .category-nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .cat-tab {{
      background: rgba(255, 255, 255, 0.10);
      color: var(--text-on-green);
      border: 2px solid rgba(255, 255, 255, 0.22);
      border-radius: var(--radius-pill);
      height: 42px;
      padding: 0 20px;
      font-size: 0.86rem;
      font-weight: 700;
      font-family: var(--font-text);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      white-space: nowrap;
      transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .cat-tab:hover {{
      background: rgba(255, 255, 255, 0.20);
      border-color: var(--gold-300);
      color: var(--white);
    }}
    .cat-tab.active-VENDAS,
    .cat-tab.active-QUALIDADE,
    .cat-tab.active-TURNOS {{
      background: var(--white);
      color: var(--green-700);
      border-color: var(--white);
      box-shadow: var(--shadow-sm);
      font-weight: 800;
    }}
    .cat-tab.active-CUSTOS {{
      background: var(--red-700);
      color: var(--white);
      border-color: var(--white);
      box-shadow: var(--shadow-sm);
      font-weight: 800;
    }}
    .cv-tricolore-bar {{
      height: 7px;
      background: var(--tricolore);
      width: 100%;
    }}

    /* Container & Barra de Filtros */
    .container {{
      max-width: 1600px;
      margin: 24px auto 0;
      padding: 0 28px;
    }}
    .filter-bar {{
      background: var(--surface-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-md);
      padding: 16px 22px;
      margin-bottom: 20px;
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      align-items: flex-end;
      justify-content: space-between;
    }}
    .filter-group-wrap {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      align-items: flex-end;
    }}
    .control-group {{
      display: flex;
      flex-direction: column;
      gap: 5px;
    }}
    .control-group label {{
      font-family: var(--font-text);
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--ink-600);
      font-weight: 800;
    }}
    select {{
      background: var(--white);
      color: var(--ink-900);
      border: 2px solid var(--border-default);
      border-radius: var(--radius-md);
      height: 42px;
      padding: 0 14px;
      font-size: 0.86rem;
      font-family: var(--font-text);
      font-weight: 700;
      cursor: pointer;
      min-width: 175px;
      transition: border-color 120ms, box-shadow 120ms;
    }}
    select:hover {{ border-color: var(--green-300); }}
    select:focus {{ outline: none; border-color: var(--green-700); box-shadow: var(--focus-ring); }}

    /* Pílulas de Indicadores e Lojas (.cv-tab style) */
    .indicator-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 18px;
    }}
    .ind-pill {{
      background: var(--white);
      border: 2px solid var(--border-default);
      color: var(--ink-800);
      padding: 7px 16px;
      border-radius: var(--radius-pill);
      font-family: var(--font-text);
      font-size: 0.80rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 120ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .ind-pill:hover {{
      border-color: var(--green-300);
      background: var(--green-50);
      color: var(--green-800);
    }}
    .ind-pill.active {{
      background: var(--green-700);
      color: var(--white);
      border-color: var(--green-700);
      box-shadow: var(--shadow-sm);
    }}

    /* KPI Cards (Cantina Volpi Card) */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 20px;
    }}
    @media (max-width: 1100px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 600px) {{ .kpi-grid {{ grid-template-columns: 1fr; }} }}
    .kpi-card {{
      background: var(--surface-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-md);
      padding: 18px 22px;
      position: relative;
      overflow: hidden;
      transition: box-shadow 200ms, transform 200ms;
    }}
    .kpi-card:hover {{
      box-shadow: var(--shadow-lg);
      transform: translateY(-2px);
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 4px;
      background: var(--green-700);
    }}
    .kpi-card.c-meta::before {{ background: var(--gold-700); }}
    .kpi-card.c-real::before {{ background: var(--green-700); }}
    .kpi-card.c-status::before {{ background: var(--red-700); }}
    .kpi-card.c-cat::before {{ background: var(--green-600); }}
    .kpi-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      gap: 8px;
    }}
    .kpi-title {{
      font-family: var(--font-text);
      font-size: 0.74rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--ink-600);
    }}
    .kpi-badge {{
      font-family: var(--font-text);
      font-size: 0.69rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 4px 10px;
      border-radius: var(--radius-pill);
      background: var(--ink-50);
      color: var(--ink-700);
      border: 1px solid var(--ink-200);
    }}
    .kpi-value {{
      font-family: var(--font-display);
      font-size: 1.62rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--ink-900);
      margin: 4px 0;
    }}
    .kpi-sub {{
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Gráficos e Cards */
    .charts-row {{
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 18px;
      margin-bottom: 22px;
    }}
    @media (max-width: 1050px) {{ .charts-row {{ grid-template-columns: 1fr; }} }}
    .chart-card {{
      background: var(--surface-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-md);
      padding: 20px 24px;
    }}
    .chart-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .chart-card-title {{
      font-family: var(--font-display);
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.015em;
      color: var(--ink-900);
    }}
    .chart-card-subtitle {{
      font-size: 0.78rem;
      font-weight: 500;
      color: var(--text-muted);
      margin-top: 2px;
    }}
    .chart-container {{
      position: relative;
      height: 265px;
      width: 100%;
    }}

    /* Botões de Alternância de Visão */
    .view-switch {{
      display: flex;
      gap: 4px;
      background: var(--ink-50);
      padding: 4px;
      border-radius: var(--radius-pill);
      border: 2px solid var(--border-default);
    }}
    .view-btn {{
      background: transparent;
      color: var(--ink-700);
      border: none;
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      font-family: var(--font-text);
      transition: all 120ms;
    }}
    .view-btn.active {{
      background: var(--green-700);
      color: var(--white);
      box-shadow: var(--shadow-xs);
    }}

    /* Tabelas no Padrão Oficial Cantina Volpi (Cabeçalho Verde #254C25, Linhas Claras) */
    .matrix-card {{
      background: var(--surface-card);
      border: 1.5px solid var(--ink-200);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-md);
      overflow: hidden;
      margin-bottom: 26px;
    }}
    .matrix-header {{
      padding: 16px 22px;
      background: var(--ink-50);
      border-bottom: 1.5px solid var(--ink-200);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .table-responsive {{
      width: 100%;
      overflow-x: auto;
    }}
    table.semanal-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.80rem;
    }}
    table.semanal-table th, table.semanal-table td {{
      padding: 10px 12px;
      text-align: right;
      border-bottom: 1px solid var(--ink-100);
      white-space: nowrap;
      color: var(--ink-800);
    }}
    table.semanal-table th:first-child, table.semanal-table td:first-child {{
      text-align: left;
      position: sticky;
      left: 0;
      background: var(--white);
      z-index: 2;
      border-right: 1.5px solid var(--ink-200);
    }}
    table.semanal-table thead th {{
      background: var(--green-700);
      color: var(--white);
      font-family: var(--font-display);
      font-weight: 800;
      font-size: 0.73rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      border-bottom: none;
    }}
    table.semanal-table thead th:first-child {{
      background: var(--green-800);
      color: var(--white);
    }}
    .th-group {{
      text-align: center !important;
      border-left: 1px solid rgba(255, 255, 255, 0.20);
      background: var(--green-800) !important;
      color: var(--gold-300) !important;
    }}
    table.semanal-table tr.clickable-row {{
      cursor: pointer;
      transition: background 120ms;
    }}
    table.semanal-table tr.clickable-row:hover td {{
      background: var(--paper);
    }}
    table.semanal-table tr.selected-row td {{
      background: var(--green-50);
    }}
    table.semanal-table tr.selected-row td:first-child {{
      background: var(--green-100);
      border-left: 4px solid var(--green-700);
    }}
    .col-sep {{
      border-left: 1px solid var(--ink-100);
    }}
    .val-meta {{ color: var(--ink-500); font-weight: 700; }}
    .val-real {{ font-family: var(--font-display); color: var(--green-700); font-weight: 800; }}

    /* Badges / Status Pills (Semáforo Oficial Cantina Volpi) */
    .status-pill {{
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      border-radius: var(--radius-pill);
      font-family: var(--font-text);
      font-size: 0.71rem;
      font-weight: 800;
      letter-spacing: 0.03em;
      border: 1px solid transparent;
    }}
    .st-ok {{ background: var(--green-50); color: var(--green-700); border-color: var(--green-200); }}
    .st-warn {{ background: var(--gold-100); color: var(--gold-800); border-color: var(--gold-300); }}
    .st-bad {{ background: var(--red-50); color: var(--red-800); border-color: var(--red-200); }}
    .st-none {{ background: var(--ink-50); color: var(--ink-600); border-color: var(--ink-200); }}

    /* Cards por Unidade */
    .unit-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
      gap: 18px;
    }}
    @media (max-width: 560px) {{ .unit-cards-grid {{ grid-template-columns: 1fr; }} }}
    .unit-cat-card {{
      background: var(--surface-card);
      border: 1.5px solid var(--ink-200);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-md);
      overflow: hidden;
    }}
    .unit-cat-header {{
      padding: 14px 20px;
      background: var(--ink-50);
      border-bottom: 1.5px solid var(--ink-200);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .unit-cat-header h3 {{
      font-family: var(--font-display);
      font-size: 1.02rem;
      font-weight: 800;
      color: var(--green-700);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* Estilos da Aba Vendas Dia & Noite */
    .kpi-grid-5 {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 20px;
    }}
    @media (max-width: 1200px) {{ .kpi-grid-5 {{ grid-template-columns: repeat(3, 1fr); }} }}
    @media (max-width: 700px) {{ .kpi-grid-5 {{ grid-template-columns: 1fr; }} }}
    .overview-grid-turnos {{
      display: grid;
      grid-template-columns: 2.2fr 1fr;
      gap: 18px;
      margin-bottom: 20px;
    }}
    .comp-grid-turnos {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-bottom: 24px;
    }}
    @media (max-width: 1100px) {{
      .overview-grid-turnos, .comp-grid-turnos {{ grid-template-columns: 1fr; }}
    }}
    .table-scroll-turnos {{
      max-height: 250px;
      overflow-y: auto;
      border: 1.5px solid var(--ink-200);
      border-radius: var(--radius-md);
      margin-top: 14px;
      background: var(--white);
    }}

    /* Divisor de Seção Oficial Cantina Volpi (Ponto Vermelho + Caps Verde + Linha Creme) */
    .section-divider-turnos {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 28px 0 16px;
      padding-bottom: 10px;
      border-bottom: 2px solid var(--ink-200);
      flex-wrap: wrap;
      gap: 10px;
    }}
    .section-divider-turnos h2 {{
      font-family: var(--font-display);
      color: var(--green-700);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .section-divider-turnos h2::before {{
      content: '';
      display: inline-block;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--red-700);
      flex: none;
    }}

    .units-grid-turnos {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
      gap: 18px;
    }}
    @media (max-width: 600px) {{ .units-grid-turnos {{ grid-template-columns: 1fr; }} }}
    .unit-card-turno {{
      background: var(--surface-card);
      border: 1.5px solid var(--ink-200);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-md);
      padding: 18px 22px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .unit-metrics-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
    }}
    @media (max-width: 560px) {{ .unit-metrics-3 {{ grid-template-columns: 1fr; }} }}
    .um-box {{
      background: var(--paper);
      border: 1px solid var(--ink-200);
      border-radius: var(--radius-md);
      padding: 10px 12px;
    }}
    .um-box .lbl {{
      font-size: 0.69rem;
      text-transform: uppercase;
      color: var(--ink-600);
      font-weight: 800;
      display: flex;
      justify-content: space-between;
    }}
    .um-box .val {{
      font-family: var(--font-display);
      font-size: 1.06rem;
      font-weight: 800;
      margin-top: 3px;
    }}
    .um-box .sub {{
      font-size: 0.71rem;
      color: var(--text-muted);
      margin-top: 2px;
      font-weight: 600;
    }}
    .split-bar-wrap {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .split-bar-labels {{
      display: flex;
      justify-content: space-between;
      font-size: 0.74rem;
      font-weight: 800;
    }}
    .split-bar-track {{
      height: 9px;
      background: var(--ink-100);
      border-radius: var(--radius-pill);
      overflow: hidden;
      display: flex;
    }}
    .split-fill-dia {{ background: var(--gold-500); height: 100%; }}
    .split-fill-noite {{ background: var(--green-700); height: 100%; }}
    .checkbox-pill {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: var(--white);
      border: 2px solid var(--border-default);
      color: var(--ink-800);
      height: 42px;
      padding: 0 14px;
      border-radius: var(--radius-md);
      font-size: 0.80rem;
      font-weight: 700;
      cursor: pointer;
      user-select: none;
    }}
    .hidden {{ display: none !important; }}
  </style>
</head>
<body>

  <header>
    <div class="header-inner">
      <div class="brand">
        <img class="brand-logo" src="data:image/png;base64,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" alt="Cantina Volpi — Desde 1992" />
        <div class="brand-text">
          <div class="brand-eyebrow">DESDE 1992 · GESTÃO COMERCIAL & OPERACIONAL</div>
          <h1>Painel de Vendas & Metas Semanais</h1>
          <p>Acompanhamento Oficial das 8 Unidades: <strong>Vendas</strong> · <strong>Qualidade</strong> · <strong>Custos</strong> · <strong>Turnos Dia & Noite</strong></p>
        </div>
      </div>

      <!-- Navegação Principal por Categoria (Pills Cantina Volpi) -->
      <nav class="category-nav">
        <button class="cat-tab active-VENDAS" id="tabBtn_VENDAS" onclick="switchMainCategory('VENDAS')">
          💰 Metas Venda
        </button>
        <button class="cat-tab" id="tabBtn_QUALIDADE" onclick="switchMainCategory('QUALIDADE')">
          ⭐ Metas Qualidade
        </button>
        <button class="cat-tab" id="tabBtn_CUSTOS" onclick="switchMainCategory('CUSTOS')">
          📉 Metas Custo
        </button>
        <button class="cat-tab" id="tabBtn_TURNOS" onclick="switchMainCategory('TURNOS')">
          ☀️🌙 Vendas Dia & Noite
        </button>
      </nav>
    </div>
    <div class="cv-tricolore-bar"></div>
  </header>

  <!-- ===================================================================== -->
  <!-- PAINEL 1: METAS SEMANAIS POR CATEGORIA (VENDAS | QUALIDADE | CUSTOS)  -->
  <!-- ===================================================================== -->
  <main class="container" id="semanalSection">
    <div class="filter-bar">
      <div class="filter-group-wrap">
        <div class="control-group">
          <label for="semMonthFilter">🗓️ Mês (Planilha Semanal)</label>
          <select id="semMonthFilter" onchange="renderSemanalView()">
            <option value="YEAR_2026">📊 Acumulado 2026 (Jan–Out)</option>
            <option value="2026-12">Dezembro 2026 (Projeção/Meta)</option>
            <option value="2026-11">Novembro 2026 (Projeção/Meta)</option>
            <option value="2026-10" selected>Outubro 2026</option>
            <option value="2026-09">Setembro 2026</option>
            <option value="2026-08">Agosto 2026</option>
            <option value="2026-07">Julho 2026</option>
            <option value="2026-06">Junho 2026</option>
            <option value="2026-05">Maio 2026</option>
            <option value="2026-04">Abril 2026</option>
            <option value="2026-03">Março 2026</option>
            <option value="2026-02">Fevereiro 2026</option>
            <option value="2026-01">Janeiro 2026</option>
          </select>
        </div>

        <div class="control-group">
          <label for="semWeekFilter">📌 Recorte Semanal</label>
          <select id="semWeekFilter" onchange="renderSemanalView()">
            <option value="ACUM" selected>📊 Acumulado do Mês</option>
            <option value="W1">Semana 1</option>
            <option value="W2">Semana 2</option>
            <option value="W3">Semana 3</option>
            <option value="W4">Semana 4</option>
            <option value="W5">Semana 5</option>
          </select>
        </div>

        <div class="control-group">
          <label for="semUnitFilter">🏢 Unidade</label>
          <select id="semUnitFilter" onchange="onGlobalUnitChange(this.value)">
            <option value="ALL" selected>Todas as Unidades (8)</option>
          </select>
        </div>

        <div class="control-group">
          <label for="semIndicatorSelect">🎯 Indicador em Destaque nos Gráficos</label>
          <select id="semIndicatorSelect" onchange="onIndicatorSelectChange()"></select>
        </div>
      </div>

      <div class="view-switch">
        <button class="view-btn active" id="btnViewMatrix" onclick="setSemanalSubView('MATRIX')">📋 Planilha Semanal (Sem 1–5)</button>
        <button class="view-btn" id="btnViewUnits" onclick="setSemanalSubView('UNITS')">🏢 Vendas & Metas por Loja</button>
      </div>
    </div>

    <!-- Pílulas Rápidas de Indicadores da Categoria -->
    <div class="indicator-pills" id="indicatorPillsContainer"></div>

    <!-- 4 KPI Cards do Indicador e Categoria -->
    <section class="kpi-grid">
      <div class="kpi-card c-meta">
        <div class="kpi-header">
          <span class="kpi-title" id="semKpiMetaTitle">🎯 Meta do Indicador</span>
          <span class="kpi-badge" id="semKpiCatBadge">VENDAS</span>
        </div>
        <div class="kpi-value" id="semKpiMetaVal" style="color:#254c25;">-</div>
        <div class="kpi-sub"><span id="semKpiMetaSub">Meta estipulada na planilha</span></div>
      </div>

      <div class="kpi-card c-real">
        <div class="kpi-header">
          <span class="kpi-title" id="semKpiRealTitle">📊 Realizado</span>
          <span class="kpi-badge" id="semKpiWeekBadge">Acumulado</span>
        </div>
        <div class="kpi-value" id="semKpiRealVal" style="color:#254c25;">-</div>
        <div class="kpi-sub"><span id="semKpiRealSub">Resultado apurado no período</span></div>
      </div>

      <div class="kpi-card c-status">
        <div class="kpi-header">
          <span class="kpi-title">📈 Atingimento / Desempenho</span>
          <span class="kpi-badge" id="semKpiStatusRule">Maior = Melhor</span>
        </div>
        <div class="kpi-value" id="semKpiStatusVal">-</div>
        <div class="kpi-sub"><span id="semKpiStatusDiff">-</span></div>
      </div>

      <div class="kpi-card c-cat">
        <div class="kpi-header">
          <span class="kpi-title" id="semKpiSummaryTitle">🏆 Metas Batidas na Categoria</span>
          <span class="kpi-badge" id="semKpiSummaryPct">0%</span>
        </div>
        <div class="kpi-value" id="semKpiSummaryVal">0 / 0</div>
        <div class="kpi-sub"><span id="semKpiSummarySub">Indicadores dentro da meta</span></div>
      </div>
    </section>

    <!-- 2 Gráficos Limpos do Indicador Selecionado -->
    <section class="charts-row">
      <div class="chart-card">
        <div class="chart-card-header">
          <div>
            <div class="chart-card-title" id="semChartUnitsTitle">🏢 Comparativo por Unidade: Meta vs Realizado</div>
            <div class="chart-card-subtitle" id="semChartUnitsSub">Desempenho de cada unidade para o indicador selecionado</div>
          </div>
        </div>
        <div class="chart-container">
          <canvas id="semUnitsChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-card-header">
          <div>
            <div class="chart-card-title" id="semChartWeeksTitle">🗓️ Evolução Semana 1 a Semana 5: Meta vs Realizado</div>
            <div class="chart-card-subtitle" id="semChartWeeksSub">Acompanhamento semanal na mesma metodologia da planilha</div>
          </div>
        </div>
        <div class="chart-container">
          <canvas id="semWeeksChart"></canvas>
        </div>
      </div>
    </section>

    <!-- Visão 1: Matriz Completa Semanal (Semana 1 a 5 + Acumulado) -->
    <section class="matrix-card" id="semMatrixContainer">
      <div class="matrix-header">
        <div>
          <div class="chart-card-title" id="semMatrixTitle">📋 Tabela de Metas Semanais — Categoria VENDAS</div>
          <div class="chart-card-subtitle">Clique em qualquer linha da tabela para visualizar o indicador nos gráficos acima</div>
        </div>
        <div style="font-size: 0.75rem; color: var(--text-muted);">
          <span style="color:#976816; font-weight:700;">● Meta</span> &nbsp;|&nbsp;
          <span style="color:#1f1b16; font-weight:700;">● Realizado</span> &nbsp;|&nbsp;
          <span class="status-pill st-ok">≥ 100% Meta Batida</span>
        </div>
      </div>
      <div class="table-responsive">
        <table class="semanal-table">
          <thead>
            <tr>
              <th rowspan="2" style="min-width:210px;">Indicador (Descrição)</th>
              <th colspan="2" class="th-group" id="thW1">Semana 1</th>
              <th colspan="2" class="th-group" id="thW2">Semana 2</th>
              <th colspan="2" class="th-group" id="thW3">Semana 3</th>
              <th colspan="2" class="th-group" id="thW4">Semana 4</th>
              <th colspan="2" class="th-group" id="thW5">Semana 5</th>
              <th colspan="3" class="th-group" style="background:#1e1b4b !important; color:#254c25 !important;">Acumulado do Período</th>
            </tr>
            <tr>
              <th class="col-sep">Meta</th><th>Real</th>
              <th class="col-sep">Meta</th><th>Real</th>
              <th class="col-sep">Meta</th><th>Real</th>
              <th class="col-sep">Meta</th><th>Real</th>
              <th class="col-sep">Meta</th><th>Real</th>
              <th class="col-sep">Meta</th><th>Real</th><th>% / Status</th>
            </tr>
          </thead>
          <tbody id="semMatrixBody"></tbody>
        </table>
      </div>
    </section>

    <!-- Visão 2: Cards por Unidade (Todos os indicadores da categoria para cada loja) -->
    <section class="unit-cards-grid hidden" id="semUnitsGridContainer"></section>

    <!-- Seção de Projeção Novembro 2026 vs Novembro 2025 por Loja (Aba Metas Venda) -->
    <section class="matrix-card" id="semNovProjectionCard" style="margin-top: 20px; border-color: #254c25;">
      <div class="matrix-header" style="background: #eef4ee; border-bottom: 2px solid #bcd5bc;">
        <div>
          <div class="chart-card-title" id="semNovTitle">🔮 Comparativo Direto: Quanto Vendeu em Novembro/2025 vs Projeção para Novembro/2026</div>
          <div class="chart-card-subtitle" id="semNovSubtitle">Selecione uma loja abaixo (ex: 📍 Ondina) para ver de forma simples quanto ela vendeu em Nov/2025 e quanto projeta vender em Nov/2026</div>
        </div>
        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
          <select id="semNovModeSelect" onchange="renderNovProjectionAll()" style="min-width:210px;">
            <option value="cantina_plus_delivery" selected>🍝+🛵 Cantina + Delivery (Total)</option>
            <option value="cantina_only">🍝 Apenas Cantina (Salão Dia & Noite)</option>
          </select>
          <select id="semNovProjBasisSelect" onchange="onNovBasisChange(this.value)" style="min-width:265px;">
            <option value="META" selected>🎯 Base: Meta Planejada p/ Novembro/2026</option>
            <option value="RITMO">📈 Base: Ritmo Atual da Loja (Últimos 90 dias)</option>
            <option value="MEDIA26">📊 Base: Média Mensal da Loja em 2026</option>
          </select>
        </div>
      </div>
      <div style="padding: 16px 18px;">
        <div class="indicator-pills" id="semNovStorePills" style="margin-bottom: 14px;"></div>
        <div id="semNovSummaryBanner" style="margin-bottom: 16px;"></div>
        <div class="kpi-grid" id="semNovKpiGrid" style="margin-bottom: 16px;"></div>
        <div class="chart-container" style="height: 280px; margin-bottom: 16px;">
          <canvas id="semNovProjChart"></canvas>
        </div>
        <div class="table-responsive">
          <table class="semanal-table">
            <thead id="semNovProjTableHead"></thead>
            <tbody id="semNovProjTableBody"></tbody>
          </table>
        </div>
      </div>
    </section>
  </main>

  <!-- ===================================================================== -->
  <!-- PAINEL 2: VENDAS POR TURNO (DIA & NOITE) — COMPLETO COMO ERA ANTES     -->
  <!-- ===================================================================== -->
  <main class="container hidden" id="turnosSection">
    <div class="filter-bar">
      <div class="filter-group-wrap">
        <div class="control-group">
          <label for="turnoMonthFilter">🗓️ Mês / Período</label>
          <select id="turnoMonthFilter" onchange="renderTurnosView()">
            <option value="ALL" selected>📅 Todos os Meses (Nov/25 – Out/26)</option>
            <option value="YEAR_2026">📆 Ano 2026 (Jan – Out/26)</option>
            <option value="YEAR_2025">📆 Ano 2025 (Nov – Dez/25)</option>
          </select>
        </div>

        <div class="control-group">
          <label for="turnoUnitFilter">🏢 Unidade</label>
          <select id="turnoUnitFilter" onchange="onGlobalUnitChange(this.value)">
            <option value="ALL" selected>Todas as Unidades (8)</option>
          </select>
        </div>

        <div class="control-group">
          <label for="turnoModeFilter">🍝 Modalidade</label>
          <select id="turnoModeFilter" onchange="renderTurnosView()">
            <option value="cantina_only">🍝 Apenas Cantina (Dia & Noite)</option>
            <option value="cantina_plus_delivery">🍝+🛵 Cantina + Delivery (Total)</option>
          </select>
        </div>

        <label class="checkbox-pill" title="Oculta abas antigas de modelo em Brotas DK e SSA Norte.">
          <input type="checkbox" id="turnoIgnoreTemplate" checked onchange="renderTurnosView()" />
          <span>Ignorar meses-modelo</span>
        </label>
      </div>
    </div>

    <!-- 5 KPI Cards Completos -->
    <section class="kpi-grid-5">
      <div class="kpi-card" style="border-top: 3px solid var(--dia-color);">
        <div class="kpi-header">
          <span class="kpi-title">☀️ Venda Dia</span>
          <span class="kpi-badge" id="tKpiDiaPct" style="color:var(--dia-color);">0%</span>
        </div>
        <div class="kpi-value" id="tKpiDiaVal" style="color:var(--dia-color);">R$ 0,00</div>
        <div class="kpi-sub"><span id="tKpiDiaSub">0 clientes/pedidos dia</span></div>
      </div>

      <div class="kpi-card" style="border-top: 3px solid var(--noite-color);">
        <div class="kpi-header">
          <span class="kpi-title">🌙 Venda Noite</span>
          <span class="kpi-badge" id="tKpiNoitePct" style="color:var(--noite-color);">0%</span>
        </div>
        <div class="kpi-value" id="tKpiNoiteVal" style="color:var(--noite-color);">R$ 0,00</div>
        <div class="kpi-sub"><span id="tKpiNoiteSub">0 clientes/pedidos noite</span></div>
      </div>

      <div class="kpi-card" style="border-top: 3px solid var(--vendas-color);">
        <div class="kpi-header">
          <span class="kpi-title">💰 Total Acumulado (Dia + Noite)</span>
          <span class="kpi-badge" id="tKpiTotalBadge">Cantina</span>
        </div>
        <div class="kpi-value" id="tKpiTotalVal" style="color:var(--vendas-color);">R$ 0,00</div>
        <div class="kpi-sub"><span id="tKpiTotalSub">Soma das unidades</span></div>
      </div>

      <div class="kpi-card" style="border-top: 4px solid #254c25;">
        <div class="kpi-header">
          <span class="kpi-title">📅 Melhor Mês do Período</span>
          <span class="kpi-badge" id="tKpiBestMonthBadge">Mês</span>
        </div>
        <div class="kpi-value" id="tKpiBestMonthVal" style="color:#254c25;">R$ 0,00</div>
        <div class="kpi-sub"><span id="tKpiBestMonthSub">-</span></div>
      </div>

      <div class="kpi-card" style="border-top: 4px solid #976816;">
        <div class="kpi-header">
          <span class="kpi-title">🗓️ Melhor Semana / Dia Sem.</span>
          <span class="kpi-badge" id="tKpiBestWeekBadge">Destaque</span>
        </div>
        <div class="kpi-value" id="tKpiBestWeekVal" style="color:#976816;">R$ 0,00</div>
        <div class="kpi-sub"><span id="tKpiBestWeekSub">-</span></div>
      </div>
    </section>

    <!-- Visão Geral: Barras por Unidade + Rosca Proporção Dia vs Noite -->
    <section class="overview-grid-turnos">
      <div class="chart-card">
        <div class="chart-card-header">
          <div>
            <div class="chart-card-title">🏢 Comparativo Geral por Unidade (Venda Dia vs Venda Noite)</div>
            <div class="chart-card-subtitle">Faturamento acumulado de cada unidade separado por turno</div>
          </div>
        </div>
        <div class="chart-container">
          <canvas id="turnoUnitsChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-card-header">
          <div>
            <div class="chart-card-title">⚖️ Participação Dia vs Noite</div>
            <div class="chart-card-subtitle">Proporção consolidada no período selecionado</div>
          </div>
        </div>
        <div class="chart-container">
          <canvas id="turnoDonutChart"></canvas>
        </div>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- SEÇÃO 1 (SEPARADA): DETALHAMENTO DE VENDAS POR LOJA (TURNOS DIA&NOITE)-->
    <!-- ===================================================================== -->
    <div class="section-divider-turnos" style="margin-top: 10px;">
      <h2 style="font-size:1.08rem;font-weight:800;">🏢 Detalhamento de Vendas por Loja (Turnos Dia & Noite)</h2>
      <span style="font-size: 0.76rem; color: var(--text-muted);">Faturamento de Dia e Noite por unidade no período/mês selecionado acima</span>
    </div>
    <section class="units-grid-turnos" id="turnoStoreCardsContainer" style="margin-bottom: 24px;"></section>

    <!-- ===================================================================== -->
    <!-- SEÇÃO 2 (SEPARADA): PROJEÇÃO NOVEMBRO/2026 vs NOVEMBRO/2025 DA LOJA   -->
    <!-- ===================================================================== -->
    <div class="section-divider-turnos">
      <div>
        <h2 style="font-size:1.12rem;font-weight:800;" id="turnoNovTitle">🔮 Comparativo Direto: Quanto Vendeu em Novembro/2025 vs Projeção para Novembro/2026</h2>
        <span style="font-size: 0.78rem; color: var(--text-muted);" id="turnoNovSubtitle">Selecione uma loja abaixo (ex: 📍 Ondina) para ver de forma simples quanto ela vendeu em Nov/2025 e quanto projeta vender em Nov/2026</span>
      </div>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
        <label style="font-size:0.72rem;color:var(--text-muted);font-weight:700;text-transform:uppercase;">Como calcular a projeção de Nov/26:</label>
        <select id="turnoNovProjBasisSelect" onchange="onNovBasisChange(this.value)" style="min-width:265px;">
          <option value="META" selected>🎯 Base: Meta Planejada p/ Novembro/2026</option>
          <option value="RITMO">📈 Base: Ritmo Atual da Loja (Últimos 90 dias)</option>
          <option value="MEDIA26">📊 Base: Média Mensal da Loja em 2026</option>
        </select>
      </div>
    </div>

    <section class="matrix-card" style="border-color: #254c25; margin-bottom: 24px;">
      <div style="padding: 16px 18px;">
        <div class="indicator-pills" id="turnoNovStorePills" style="margin-bottom: 14px;"></div>
        <div id="turnoNovSummaryBanner" style="margin-bottom: 16px;"></div>
        <div class="kpi-grid" id="turnoNovKpiGrid" style="margin-bottom: 16px;"></div>
        <div class="chart-container" style="height: 280px; margin-bottom: 16px;">
          <canvas id="turnoNovProjChart"></canvas>
        </div>
        <div class="table-responsive">
          <table class="semanal-table">
            <thead id="turnoNovProjTableHead"></thead>
            <tbody id="turnoNovProjTableBody"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- Comparação Mensal e Semanal Completa com Tabelas -->
    <section class="comp-grid-turnos">
      <!-- Card Comparação Mensal -->
      <div class="chart-card">
        <div class="chart-card-header">
          <div>
            <div class="chart-card-title">📊 Comparação Mensal (Mês a Mês — Dia vs Noite)</div>
            <div class="chart-card-subtitle">Evolução histórica mensal e variação percentual</div>
          </div>
        </div>
        <div class="chart-container">
          <canvas id="turnoMonthlyChart"></canvas>
        </div>
        <div class="table-scroll-turnos">
          <table class="semanal-table">
            <thead>
              <tr>
                <th>Mês</th>
                <th>☀️ Venda Dia</th>
                <th>🌙 Venda Noite</th>
                <th>💰 Total Mês</th>
                <th>% Dia</th>
                <th>% Noite</th>
                <th>Var. Mês Ant.</th>
              </tr>
            </thead>
            <tbody id="turnoMonthlyTableBody"></tbody>
          </table>
        </div>
      </div>

      <!-- Card Comparação Semanal -->
      <div class="chart-card">
        <div class="chart-card-header">
          <div>
            <div class="chart-card-title">🗓️ Comparação Semanal (Semanas do Mês & Dias da Semana)</div>
            <div class="chart-card-subtitle" id="turnoWeeklySubtitle">Desempenho por Semana do Mês (Semana 1 a 5)</div>
          </div>
          <div class="view-switch">
            <button class="view-btn active" id="btnTurnoWOM" onclick="setTurnoWeeklyType('WOM')">Semanas 1–5</button>
            <button class="view-btn" id="btnTurnoDOW" onclick="setTurnoWeeklyType('DOW')">Seg–Dom</button>
          </div>
        </div>
        <div class="chart-container">
          <canvas id="turnoWeeklyChart"></canvas>
        </div>
        <div class="table-scroll-turnos">
          <table class="semanal-table">
            <thead>
              <tr>
                <th id="turnoWeeklyColHeader">Semana do Mês</th>
                <th>☀️ Venda Dia</th>
                <th>🌙 Venda Noite</th>
                <th>💰 Total</th>
                <th>% Dia</th>
                <th>% Noite</th>
              </tr>
            </thead>
            <tbody id="turnoWeeklyTableBody"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- Vendas por Semana com Datas (De 1 a 7, De 8 a 14, etc.) -->
    <div class="section-divider-turnos">
      <h2 style="font-size:1.1rem;font-weight:800;">🗓️ Vendas por Semana e Datas (Dias 1 a 7 • 8 a 14 • 15 a 21 • 22 a 28 • 29 a 31)</h2>
      <span style="font-size: 0.78rem; color: var(--text-muted);" id="turnoWeekDatesSubtitle">Resumo vendido em cada intervalo de datas conforme unidade e período selecionados no topo</span>
    </div>

    <section class="kpi-grid-5" id="turnoWeekDateCardsContainer"></section>

    <section class="chart-card" style="margin-top: 14px;">
      <div class="chart-card-header">
        <div>
          <div class="chart-card-title">📅 Detalhamento de Vendas por Intervalo de Datas e Dia do Mês (1 a 31)</div>
          <div class="chart-card-subtitle">Faturamento diário e acumulado por faixa de datas (De 1 a 7, De 8 a 14, De 15 a 21, De 22 a 28 e De 29 a 31)</div>
        </div>
      </div>
      <div class="chart-container" style="height: 230px;">
        <canvas id="turnoDailyDatesChart"></canvas>
      </div>
      <div class="table-scroll-turnos" style="max-height: 290px;">
        <table class="semanal-table">
          <thead>
            <tr>
              <th>Intervalo / Data</th>
              <th>Faixa da Semana</th>
              <th>☀️ Venda Dia</th>
              <th>🌙 Venda Noite</th>
              <th>💰 Total Vendido</th>
              <th>% Dia</th>
              <th>% Noite</th>
            </tr>
          </thead>
          <tbody id="turnoDailyDatesTableBody"></tbody>
        </table>
      </div>
    </section>
  </main>

  <script>
    const RAW_DATA = {data_js};

    // State
    let activeCategory = 'VENDAS'; // 'VENDAS' | 'QUALIDADE' | 'CUSTOS' | 'TURNOS'
    let semanalSubView = 'MATRIX'; // 'MATRIX' | 'UNITS'
    let selectedIndicatorByCat = {{
      'VENDAS': 'Receita Total',
      'QUALIDADE': 'NPS - Falaê',
      'CUSTOS': 'CMV - Compras (%)'
    }};

    let semUnitsChartInst = null;
    let semWeeksChartInst = null;
    let turnoUnitsChartInst = null;
    let turnoWeeklyChartInst = null;
    let turnoMonthlyChartInst = null;

    // Populate Unit Selectors
    const semUnitFilter = document.getElementById('semUnitFilter');
    RAW_DATA.semanal_units.forEach(su => {{
      const opt = document.createElement('option');
      opt.value = su.unit;
      opt.textContent = '📍 ' + su.unit;
      semUnitFilter.appendChild(opt);
    }});

    const turnoMonthFilter = document.getElementById('turnoMonthFilter');
    RAW_DATA.month_order.forEach(([k, lbl]) => {{
      const opt = document.createElement('option');
      opt.value = k;
      opt.textContent = '🗓️ ' + lbl;
      turnoMonthFilter.appendChild(opt);
    }});

    const turnoUnitFilter = document.getElementById('turnoUnitFilter');
    RAW_DATA.units.forEach(u => {{
      const opt = document.createElement('option');
      opt.value = u.unit;
      opt.textContent = '📍 ' + u.unit;
      turnoUnitFilter.appendChild(opt);
    }});

    // Formatting Helpers
    function formatVal(val, fmtType, compact = false) {{
      if (val === null || val === undefined || Number.isNaN(val)) return '-';
      const num = Number(val);
      if (fmtType === 'currency') {{
        if (compact && Math.abs(num) >= 1000000) {{
          return 'R$ ' + (num / 1000000).toFixed(2).replace('.', ',') + 'M';
        }}
        if (compact && Math.abs(num) >= 1000) {{
          return 'R$ ' + (num / 1000).toFixed(1).replace('.', ',') + 'k';
        }}
        return num.toLocaleString('pt-BR', {{ style: 'currency', currency: 'BRL' }});
      }}
      if (fmtType === 'percent_dec') {{
        // In Excel, 0.30 = 30%, 0.0125 = 1.25%. If > 1.5, already in percent points
        const pct = Math.abs(num) <= 1.5 ? num * 100 : num;
        return pct.toFixed(2).replace('.', ',').replace(/,00$/, ',0') + '%';
      }}
      if (fmtType === 'score') {{
        return num.toLocaleString('pt-BR', {{ minimumFractionDigits: 1, maximumFractionDigits: 2 }});
      }}
      return Math.round(num).toLocaleString('pt-BR');
    }}

    function normalizeChartVal(val, fmtType) {{
      if (val === null || val === undefined) return 0;
      const num = Number(val);
      if (fmtType === 'percent_dec') {{
        return Math.abs(num) <= 1.5 ? +(num * 100).toFixed(2) : +num.toFixed(2);
      }}
      return +num.toFixed(2);
    }}

    // Evaluate Meta vs Realizado
    function evaluateMeta(meta, real, lowerIsBetter) {{
      if (meta === null || meta === undefined || real === null || real === undefined) {{
        return {{ hasMeta: false, pct: null, hit: null, cls: 'st-none', label: '-' }};
      }}
      const m = Number(meta);
      const r = Number(real);
      if (m === 0 && r === 0) {{
        return {{ hasMeta: false, pct: null, hit: null, cls: 'st-none', label: '-' }};
      }}
      if (lowerIsBetter) {{
        if (m === 0) {{
          const hit = r <= 0;
          return {{ hasMeta: true, pct: hit ? 100 : 0, hit, cls: hit ? 'st-ok' : 'st-bad', label: hit ? '✅ Na Meta (0)' : `⚠️ Acima (+${{r}})` }};
        }}
        const ratio = (r / m) * 100;
        const hit = r <= m * 1.001;
        const warn = r <= m * 1.10;
        const cls = hit ? 'st-ok' : (warn ? 'st-warn' : 'st-bad');
        const label = hit ? `✅ ${{ratio.toFixed(0)}}% do teto` : `⚠️ ${{ratio.toFixed(0)}}% do teto`;
        return {{ hasMeta: true, pct: ratio, hit, cls, label }};
      }} else {{
        if (m <= 0) {{
          return {{ hasMeta: false, pct: null, hit: null, cls: 'st-none', label: '-' }};
        }}
        const ratio = (r / m) * 100;
        const hit = ratio >= 99.9;
        const warn = ratio >= 88.0;
        const cls = hit ? 'st-ok' : (warn ? 'st-warn' : 'st-bad');
        const label = `${{hit ? '✅' : (warn ? '⚡' : '🔻')}} ${{ratio.toFixed(1).replace('.', ',')}}%`;
        return {{ hasMeta: true, pct: ratio, hit, cls, label }};
      }}
    }}

    function switchMainCategory(cat) {{
      activeCategory = cat;
      ['VENDAS', 'QUALIDADE', 'CUSTOS', 'TURNOS'].forEach(c => {{
        const btn = document.getElementById('tabBtn_' + c);
        btn.className = 'cat-tab' + (c === cat ? ' active-' + c : '');
      }});
      const semSec = document.getElementById('semanalSection');
      const turSec = document.getElementById('turnosSection');
      if (cat === 'TURNOS') {{
        semSec.classList.add('hidden');
        turSec.classList.remove('hidden');
        renderTurnosView();
      }} else {{
        turSec.classList.add('hidden');
        semSec.classList.remove('hidden');
        renderSemanalView();
      }}
    }}

    function setSemanalSubView(v) {{
      semanalSubView = v;
      document.getElementById('btnViewMatrix').classList.toggle('active', v === 'MATRIX');
      document.getElementById('btnViewUnits').classList.toggle('active', v === 'UNITS');
      document.getElementById('semMatrixContainer').classList.toggle('hidden', v !== 'MATRIX');
      document.getElementById('semUnitsGridContainer').classList.toggle('hidden', v !== 'UNITS');
    }}

    function onIndicatorSelectChange() {{
      const sel = document.getElementById('semIndicatorSelect');
      if (sel.value) {{
        selectedIndicatorByCat[activeCategory] = sel.value;
        renderSemanalView();
      }}
    }}

    function selectIndicator(indName) {{
      selectedIndicatorByCat[activeCategory] = indName;
      renderSemanalView();
    }}

    // Aggregate an indicator across selected units and selected month(s)
    function getAggregatedCategoryData(cat, mFilter, uFilter) {{
      const units = RAW_DATA.semanal_units.filter(u => uFilter === 'ALL' || u.unit === uFilter);
      const monthsList = mFilter === 'YEAR_2026'
        ? ['2026-01','2026-02','2026-03','2026-04','2026-05','2026-06','2026-07','2026-08','2026-09','2026-10']
        : [mFilter];

      const indMap = new Map();
      let weekHeaders = {{ W1: 'Semana 1', W2: 'Semana 2', W3: 'Semana 3', W4: 'Semana 4', W5: 'Semana 5' }};

      units.forEach(u => {{
        monthsList.forEach(mk => {{
          const mObj = u.months[mk];
          if (!mObj) return;
          if (mFilter !== 'YEAR_2026' && mObj.week_headers) {{
            weekHeaders = mObj.week_headers;
          }}
          const items = (mObj.categories && mObj.categories[cat]) || [];
          items.forEach(item => {{
            if (!indMap.has(item.name)) {{
              indMap.set(item.name, {{
                name: item.name,
                format: item.format,
                lower_is_better: item.lower_is_better,
                is_avg: item.is_avg,
                weeks: {{
                  W1: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                  W2: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                  W3: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                  W4: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                  W5: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }}
                }},
                acum: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                byUnit: {{}}
              }});
            }}
            const entry = indMap.get(item.name);
            if (!entry.byUnit[u.unit]) {{
              entry.byUnit[u.unit] = {{
                W1: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                W2: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                W3: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                W4: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                W5: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }},
                ACUM: {{ mSum: 0, mCnt: 0, rSum: 0, rCnt: 0 }}
              }};
            }}
            const uSlot = entry.byUnit[u.unit];

            ['W1','W2','W3','W4','W5'].forEach(wk => {{
              const wObj = item.weeks[wk];
              if (!wObj) return;
              if (wObj.meta !== null && wObj.meta !== undefined) {{
                entry.weeks[wk].mSum += wObj.meta;
                entry.weeks[wk].mCnt += 1;
                uSlot[wk].mSum += wObj.meta;
                uSlot[wk].mCnt += 1;
              }}
              if (wObj.real !== null && wObj.real !== undefined && !(item.is_avg && wObj.real === 0)) {{
                entry.weeks[wk].rSum += wObj.real;
                entry.weeks[wk].rCnt += 1;
                uSlot[wk].rSum += wObj.real;
                uSlot[wk].rCnt += 1;
              }}
            }});

            const ac = item.acum;
            if (ac) {{
              if (ac.meta !== null && ac.meta !== undefined) {{
                entry.acum.mSum += ac.meta;
                entry.acum.mCnt += 1;
                uSlot.ACUM.mSum += ac.meta;
                uSlot.ACUM.mCnt += 1;
              }}
              if (ac.real !== null && ac.real !== undefined && !(item.is_avg && ac.real === 0)) {{
                entry.acum.rSum += ac.real;
                entry.acum.rCnt += 1;
                uSlot.ACUM.rSum += ac.real;
                uSlot.ACUM.rCnt += 1;
              }}
            }}
          }});
        }});
      }});

      const finalizeSlot = (slot, isAvg) => ({{
        meta: slot.mCnt > 0 ? (isAvg ? slot.mSum / slot.mCnt : slot.mSum) : null,
        real: slot.rCnt > 0 ? (isAvg ? slot.rSum / slot.rCnt : slot.rSum) : null
      }});

      const indicators = [];
      indMap.forEach(entry => {{
        const weeksFinal = {{}};
        ['W1','W2','W3','W4','W5'].forEach(wk => {{
          weeksFinal[wk] = finalizeSlot(entry.weeks[wk], entry.is_avg);
        }});
        const acumFinal = finalizeSlot(entry.acum, entry.is_avg);
        const byUnitFinal = {{}};
        Object.keys(entry.byUnit).forEach(uName => {{
          byUnitFinal[uName] = {{}};
          ['W1','W2','W3','W4','W5','ACUM'].forEach(k => {{
            byUnitFinal[uName][k] = finalizeSlot(entry.byUnit[uName][k], entry.is_avg);
          }});
        }});
        indicators.push({{
          name: entry.name,
          format: entry.format,
          lower_is_better: entry.lower_is_better,
          is_avg: entry.is_avg,
          weeks: weeksFinal,
          acum: acumFinal,
          byUnit: byUnitFinal
        }});
      }});

      return {{ indicators, weekHeaders }};
    }}

    function renderSemanalView() {{
      const mFilter = document.getElementById('semMonthFilter').value;
      const wFilter = document.getElementById('semWeekFilter').value; // 'ACUM' | 'W1'..'W5'
      const uFilter = document.getElementById('semUnitFilter').value;

      const {{ indicators, weekHeaders }} = getAggregatedCategoryData(activeCategory, mFilter, uFilter);

      // Update Week Headers in Table
      ['W1','W2','W3','W4','W5'].forEach(wk => {{
        document.getElementById('th' + wk).textContent = weekHeaders[wk] || wk;
      }});

      // Populate Indicator Select & Quick Pills
      const indSelect = document.getElementById('semIndicatorSelect');
      const pillsBox = document.getElementById('indicatorPillsContainer');
      indSelect.innerHTML = '';
      pillsBox.innerHTML = '';

      if (indicators.length === 0) {{
        document.getElementById('semMatrixBody').innerHTML = '<tr><td colspan="14" style="text-align:center;padding:24px;">Sem dados para este filtro.</td></tr>';
        document.getElementById('semUnitsGridContainer').innerHTML = '';
        const semNovCard = document.getElementById('semNovProjectionCard');
        if (semNovCard) {{
          semNovCard.classList.toggle('hidden', activeCategory !== 'VENDAS');
          if (activeCategory === 'VENDAS') renderNovProjectionAll();
        }}
        return;
      }}

      let currentIndName = selectedIndicatorByCat[activeCategory];
      if (!indicators.some(x => x.name === currentIndName)) {{
        currentIndName = indicators[0].name;
        selectedIndicatorByCat[activeCategory] = currentIndName;
      }}

      indicators.forEach(ind => {{
        const opt = document.createElement('option');
        opt.value = ind.name;
        opt.textContent = ind.name;
        if (ind.name === currentIndName) opt.selected = true;
        indSelect.appendChild(opt);

        const pill = document.createElement('button');
        pill.className = 'ind-pill' + (ind.name === currentIndName ? ' active' : '');
        pill.textContent = ind.name;
        pill.onclick = () => selectIndicator(ind.name);
        pillsBox.appendChild(pill);
      }});

      const selectedInd = indicators.find(x => x.name === currentIndName) || indicators[0];
      const activeSlot = wFilter === 'ACUM' ? selectedInd.acum : selectedInd.weeks[wFilter];
      const evalSelected = evaluateMeta(activeSlot.meta, activeSlot.real, selectedInd.lower_is_better);

      // Count how many indicators in this category hit their goal
      let hitCount = 0, totalWithMeta = 0;
      indicators.forEach(ind => {{
        const sl = wFilter === 'ACUM' ? ind.acum : ind.weeks[wFilter];
        const ev = evaluateMeta(sl.meta, sl.real, ind.lower_is_better);
        if (ev.hasMeta && sl.real !== null) {{
          totalWithMeta++;
          if (ev.hit) hitCount++;
        }}
      }});

      // Update KPI Cards
      const weekLabelMap = {{ ACUM: 'Acumulado', W1: 'Semana 1', W2: 'Semana 2', W3: 'Semana 3', W4: 'Semana 4', W5: 'Semana 5' }};
      document.getElementById('semKpiMetaTitle').textContent = `🎯 Meta: ${{selectedInd.name}}`;
      document.getElementById('semKpiCatBadge').textContent = activeCategory;
      document.getElementById('semKpiMetaVal').textContent = formatVal(activeSlot.meta, selectedInd.format);
      document.getElementById('semKpiMetaSub').textContent = selectedInd.is_avg ? 'Meta média do período' : 'Meta somada do período';

      document.getElementById('semKpiRealTitle').textContent = `📊 Realizado: ${{selectedInd.name}}`;
      document.getElementById('semKpiWeekBadge').textContent = weekLabelMap[wFilter];
      document.getElementById('semKpiRealVal').textContent = formatVal(activeSlot.real, selectedInd.format);
      document.getElementById('semKpiRealSub').textContent = uFilter === 'ALL' ? 'Consolidado das unidades' : `Unidade: ${{uFilter}}`;

      document.getElementById('semKpiStatusRule').textContent = selectedInd.lower_is_better ? 'Menor = Melhor (Teto)' : 'Maior = Melhor';
      document.getElementById('semKpiStatusVal').innerHTML = `<span class="status-pill ${{evalSelected.cls}}" style="font-size:1.05rem;padding:4px 12px;">${{evalSelected.label}}</span>`;
      if (activeSlot.meta !== null && activeSlot.real !== null) {{
        const diff = activeSlot.real - activeSlot.meta;
        const sign = diff > 0 ? '+' : '';
        document.getElementById('semKpiStatusDiff').textContent = `Diferença vs Meta: ${{sign}}${{formatVal(diff, selectedInd.format)}}`;
      }} else {{
        document.getElementById('semKpiStatusDiff').textContent = 'Sem comparativo disponível';
      }}

      const hitPct = totalWithMeta > 0 ? Math.round((hitCount / totalWithMeta) * 100) : 0;
      document.getElementById('semKpiSummaryTitle').textContent = `🏆 Metas Batidas (${{activeCategory}})`;
      document.getElementById('semKpiSummaryPct').textContent = `${{hitPct}}%`;
      document.getElementById('semKpiSummaryVal').textContent = `${{hitCount}} de ${{totalWithMeta}}`;
      document.getElementById('semKpiSummarySub').textContent = `Indicadores dentro da meta em ${{weekLabelMap[wFilter]}}`;

      // Render 2 Charts for Selected Indicator
      renderSemanalCharts(selectedInd, wFilter, weekHeaders);

      // Render Matrix Table (Semana 1..5 + Acumulado)
      document.getElementById('semMatrixTitle').textContent = `📋 Planilha de Metas Semanais — Categoria: ${{activeCategory}}`;
      const tbody = document.getElementById('semMatrixBody');
      tbody.innerHTML = '';

      indicators.forEach(ind => {{
        const evAcum = evaluateMeta(ind.acum.meta, ind.acum.real, ind.lower_is_better);
        const tr = document.createElement('tr');
        tr.className = 'clickable-row' + (ind.name === selectedInd.name ? ' selected-row' : '');
        tr.onclick = () => selectIndicator(ind.name);

        let cells = `<td><strong>${{ind.name}}</strong></td>`;
        ['W1','W2','W3','W4','W5'].forEach(wk => {{
          const w = ind.weeks[wk];
          cells += `
            <td class="col-sep val-meta">${{formatVal(w.meta, ind.format, true)}}</td>
            <td class="val-real">${{formatVal(w.real, ind.format, true)}}</td>
          `;
        }});
        cells += `
          <td class="col-sep val-meta" style="background:#fbf7ef;">${{formatVal(ind.acum.meta, ind.format, true)}}</td>
          <td class="val-real" style="background:#eef4ee;">${{formatVal(ind.acum.real, ind.format, true)}}</td>
          <td><span class="status-pill ${{evAcum.cls}}">${{evAcum.label}}</span></td>
        `;
        tr.innerHTML = cells;
        tbody.appendChild(tr);
      }});

      // Render Unit Cards Grid for this Category
      renderSemanalUnitCards(indicators, wFilter, uFilter, weekLabelMap[wFilter]);

      // Show/Hide & Render Nov 2025 vs Nov 2026 Projection in VENDAS tab
      const semNovCard = document.getElementById('semNovProjectionCard');
      if (semNovCard) {{
        semNovCard.classList.toggle('hidden', activeCategory !== 'VENDAS');
        if (activeCategory === 'VENDAS') {{
          renderNovProjectionAll();
        }}
      }}
    }}

    function renderSemanalCharts(selectedInd, wFilter, weekHeaders) {{
      // Chart 1: Units Comparison (Meta vs Realizado)
      const ctxU = document.getElementById('semUnitsChart').getContext('2d');
      if (semUnitsChartInst) semUnitsChartInst.destroy();

      const unitNames = RAW_DATA.semanal_units.map(u => u.unit).filter(uName => selectedInd.byUnit[uName]);
      const uMetaData = unitNames.map(uName => {{
        const sl = selectedInd.byUnit[uName][wFilter] || {{ meta: 0 }};
        return normalizeChartVal(sl.meta, selectedInd.format);
      }});
      const uRealData = unitNames.map(uName => {{
        const sl = selectedInd.byUnit[uName][wFilter] || {{ real: 0 }};
        return normalizeChartVal(sl.real, selectedInd.format);
      }});

      document.getElementById('semChartUnitsTitle').textContent = `🏢 ${{selectedInd.name}} — Meta vs Realizado por Unidade`;
      const realBarColor = activeCategory === 'CUSTOS' ? '#c92535' : (activeCategory === 'QUALIDADE' ? '#2f6db0' : '#254c25');

      semUnitsChartInst = new Chart(ctxU, {{
        type: 'bar',
        data: {{
          labels: unitNames,
          datasets: [
            {{
              label: '🎯 Meta',
              data: uMetaData,
              backgroundColor: 'rgba(151, 104, 22, 0.75)',
              borderRadius: 5
            }},
            {{
              label: '📊 Realizado',
              data: uRealData,
              backgroundColor: realBarColor,
              borderRadius: 5
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ labels: {{ color: '#1f1b16', font: {{ family: 'Mulish', size: 11, weight: '600' }} }} }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#2d2820', font: {{ weight: '600' }} }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#7c7263' }}, grid: {{ color: '#ece5d7' }} }}
          }}
        }}
      }});

      // Chart 2: Weeks W1..W5 Evolution (Meta vs Realizado)
      const ctxW = document.getElementById('semWeeksChart').getContext('2d');
      if (semWeeksChartInst) semWeeksChartInst.destroy();

      const wKeys = ['W1','W2','W3','W4','W5'];
      const wLabels = wKeys.map(k => weekHeaders[k] || k);
      const wMetaData = wKeys.map(k => normalizeChartVal(selectedInd.weeks[k].meta, selectedInd.format));
      const wRealData = wKeys.map(k => normalizeChartVal(selectedInd.weeks[k].real, selectedInd.format));

      document.getElementById('semChartWeeksTitle').textContent = `🗓️ ${{selectedInd.name}} — Semana 1 a Semana 5`;

      semWeeksChartInst = new Chart(ctxW, {{
        type: 'bar',
        data: {{
          labels: wLabels,
          datasets: [
            {{
              label: '🎯 Meta Semanal',
              data: wMetaData,
              backgroundColor: 'rgba(151, 104, 22, 0.75)',
              borderRadius: 5
            }},
            {{
              label: '📊 Realizado Semanal',
              data: wRealData,
              backgroundColor: realBarColor,
              borderRadius: 5
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ labels: {{ color: '#1f1b16', font: {{ family: 'Mulish', size: 11, weight: '600' }} }} }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#2d2820', font: {{ size: 10.5, weight: '600' }} }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#7c7263' }}, grid: {{ color: '#ece5d7' }} }}
          }}
        }}
      }});
    }}

    function renderSemanalUnitCards(indicators, wFilter, uFilter, periodLabel) {{
      const grid = document.getElementById('semUnitsGridContainer');
      grid.innerHTML = '';

      const unitsToShow = RAW_DATA.semanal_units.filter(u => uFilter === 'ALL' || u.unit === uFilter);
      unitsToShow.forEach(u => {{
        let rowsHtml = '';
        let hitCnt = 0, totCnt = 0;

        indicators.forEach(ind => {{
          const uData = ind.byUnit[u.unit];
          if (!uData) return;
          const slot = uData[wFilter];
          if (!slot || (slot.meta === null && slot.real === null)) return;
          const ev = evaluateMeta(slot.meta, slot.real, ind.lower_is_better);
          if (ev.hasMeta && slot.real !== null) {{
            totCnt++;
            if (ev.hit) hitCnt++;
          }}
          rowsHtml += `
            <tr class="clickable-row" onclick="selectIndicator('${{ind.name.replace(/'/g, "\\\\'")}}')">
              <td><strong>${{ind.name}}</strong></td>
              <td class="val-meta">${{formatVal(slot.meta, ind.format)}}</td>
              <td class="val-real">${{formatVal(slot.real, ind.format)}}</td>
              <td><span class="status-pill ${{ev.cls}}">${{ev.label}}</span></td>
            </tr>
          `;
        }});

        if (!rowsHtml) return;

        const card = document.createElement('div');
        card.className = 'unit-cat-card';
        card.innerHTML = `
          <div class="unit-cat-header">
            <h3>📍 ${{u.unit}} <span style="font-size:0.72rem;font-weight:600;color:var(--text-muted);">(${{activeCategory}} • ${{periodLabel}})</span></h3>
            <span class="status-pill ${{hitCnt >= totCnt/2 ? 'st-ok' : 'st-warn'}}">${{hitCnt}}/${{totCnt}} metas batidas</span>
          </div>
          <div class="table-responsive">
            <table class="semanal-table">
              <thead>
                <tr>
                  <th>Indicador (${{activeCategory}})</th>
                  <th>🎯 Meta</th>
                  <th>📊 Realizado</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>${{rowsHtml}}</tbody>
            </table>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    // =====================================================================
    // PAINEL 2: TURNOS DIA & NOITE — COMPLETO COMO ERA ANTES
    // =====================================================================
    const DOW_LABELS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
    const WOM_META = [
      {{ key: 'W1', label: 'Semana 1 (Dias 1–7)', shortLabel: 'Semana 1', min: 1, max: 7 }},
      {{ key: 'W2', label: 'Semana 2 (Dias 8–14)', shortLabel: 'Semana 2', min: 8, max: 14 }},
      {{ key: 'W3', label: 'Semana 3 (Dias 15–21)', shortLabel: 'Semana 3', min: 15, max: 21 }},
      {{ key: 'W4', label: 'Semana 4 (Dias 22–28)', shortLabel: 'Semana 4', min: 22, max: 28 }},
      {{ key: 'W5', label: 'Semana 5 (Dias 29–31)', shortLabel: 'Semana 5', min: 29, max: 31 }}
    ];

    let turnoWeeklyType = 'WOM';
    let turnoDonutChartInst = null;
    const turnoUnitChartInstances = {{}};
    const turnoUnitViewMode = {{}};
    RAW_DATA.units.forEach(u => {{ turnoUnitViewMode[u.unit] = 'MONTHLY'; }});

    function normalizeDow(name) {{
      if (!name) return null;
      const s = name.toLowerCase();
      if (s.includes('seg')) return 'Segunda';
      if (s.includes('ter')) return 'Terça';
      if (s.includes('qua')) return 'Quarta';
      if (s.includes('qui')) return 'Quinta';
      if (s.includes('sex')) return 'Sexta';
      if (s.includes('sab') || s.includes('sáb') || s.includes('sb')) return 'Sábado';
      if (s.includes('dom')) return 'Domingo';
      return null;
    }}

    function setTurnoWeeklyType(t) {{
      turnoWeeklyType = t;
      document.getElementById('btnTurnoWOM').classList.toggle('active', t === 'WOM');
      document.getElementById('btnTurnoDOW').classList.toggle('active', t === 'DOW');
      renderTurnosView();
    }}

    function getTurnoMonthVals(mo, mode) {{
      if (!mo) return {{ dia: 0, noite: 0, qtd_dia: 0, qtd_noite: 0 }};
      let d = mo.venda_dia || 0;
      let n = mo.venda_noite || 0;
      if (mode === 'cantina_plus_delivery') {{
        d += (mo.deliv_dia || 0);
        n += (mo.deliv_noite || 0);
      }}
      return {{ dia: d, noite: n, qtd_dia: mo.qtd_dia || 0, qtd_noite: mo.qtd_noite || 0 }};
    }}

    function getTurnoDayVals(dObj, mode) {{
      if (!dObj) return {{ dia: 0, noite: 0 }};
      let d = dObj.venda_dia || 0;
      let n = dObj.venda_noite || 0;
      if (mode === 'cantina_plus_delivery') {{
        d += (dObj.deliv_dia || 0);
        n += (dObj.deliv_noite || 0);
      }}
      return {{ dia: d, noite: n }};
    }}

    function computeTurnoWeeklyForUnit(u, isMonthSelected, mode, ignoreTpl) {{
      const wom = WOM_META.map(w => ({{ ...w, dia: 0, noite: 0, daysCount: 0 }}));
      const dow = DOW_LABELS.map(label => ({{ label, shortLabel: label, dia: 0, noite: 0, daysCount: 0 }}));
      RAW_DATA.month_order.forEach(([mk]) => {{
        if (!isMonthSelected(mk)) return;
        const mo = u.months[mk];
        if (!mo || (ignoreTpl && mo.is_template_copy)) return;
        mo.daily.forEach(dObj => {{
          const vals = getTurnoDayVals(dObj, mode);
          if (vals.dia === 0 && vals.noite === 0) return;
          const wIdx = wom.findIndex(w => dObj.dia >= w.min && dObj.dia <= w.max);
          if (wIdx >= 0) {{
            wom[wIdx].dia += vals.dia;
            wom[wIdx].noite += vals.noite;
            wom[wIdx].daysCount += 1;
          }}
          const dowName = normalizeDow(dObj.dia_semana);
          if (dowName) {{
            const dIdx = DOW_LABELS.indexOf(dowName);
            if (dIdx >= 0) {{
              dow[dIdx].dia += vals.dia;
              dow[dIdx].noite += vals.noite;
              dow[dIdx].daysCount += 1;
            }}
          }}
        }});
      }});
      return {{ wom, dow }};
    }}

    function renderTurnosView() {{
      const mFilter = document.getElementById('turnoMonthFilter').value;
      const uFilter = document.getElementById('turnoUnitFilter').value;
      const mode = document.getElementById('turnoModeFilter').value;
      const ignoreTpl = document.getElementById('turnoIgnoreTemplate').checked;

      const isMonthSelected = (mk) => {{
        if (mFilter === 'ALL') return true;
        if (mFilter === 'YEAR_2025') return mk.startsWith('2025-');
        if (mFilter === 'YEAR_2026') return mk.startsWith('2026-');
        return mk === mFilter;
      }};

      const activeUnits = RAW_DATA.units.filter(u => uFilter === 'ALL' || u.unit === uFilter);
      let grandDia = 0, grandNoite = 0, grandQtdDia = 0, grandQtdNoite = 0;

      const unitSummaries = activeUnits.map(u => {{
        let uDia = 0, uNoite = 0, uQtdDia = 0, uQtdNoite = 0;
        RAW_DATA.month_order.forEach(([mk]) => {{
          if (!isMonthSelected(mk)) return;
          const mo = u.months[mk];
          if (!mo || (ignoreTpl && mo.is_template_copy)) return;
          const vals = getTurnoMonthVals(mo, mode);
          uDia += vals.dia;
          uNoite += vals.noite;
          uQtdDia += vals.qtd_dia;
          uQtdNoite += vals.qtd_noite;
        }});
        grandDia += uDia;
        grandNoite += uNoite;
        grandQtdDia += uQtdDia;
        grandQtdNoite += uQtdNoite;
        return {{
          unit: u.unit,
          is_dk: u.is_dk,
          dia: uDia,
          noite: uNoite,
          total: uDia + uNoite,
          qtd_dia: uQtdDia,
          qtd_noite: uQtdNoite,
          raw: u
        }};
      }});

      const grandTot = grandDia + grandNoite;
      const pDia = grandTot > 0 ? (grandDia / grandTot) * 100 : 0;
      const pNoite = grandTot > 0 ? (grandNoite / grandTot) * 100 : 0;

      document.getElementById('tKpiDiaVal').textContent = formatVal(grandDia, 'currency');
      document.getElementById('tKpiDiaPct').textContent = pDia.toFixed(1).replace('.', ',') + '%';
      document.getElementById('tKpiDiaSub').textContent = `${{Math.round(grandQtdDia).toLocaleString('pt-BR')}} clientes/pedidos dia`;

      document.getElementById('tKpiNoiteVal').textContent = formatVal(grandNoite, 'currency');
      document.getElementById('tKpiNoitePct').textContent = pNoite.toFixed(1).replace('.', ',') + '%';
      document.getElementById('tKpiNoiteSub').textContent = `${{Math.round(grandQtdNoite).toLocaleString('pt-BR')}} clientes/pedidos noite`;

      document.getElementById('tKpiTotalVal').textContent = formatVal(grandTot, 'currency');
      document.getElementById('tKpiTotalBadge').textContent = mode === 'cantina_only' ? 'Cantina' : 'Cantina + Deliv';
      document.getElementById('tKpiTotalSub').textContent = `Dia: ${{pDia.toFixed(1).replace('.', ',')}}% | Noite: ${{pNoite.toFixed(1).replace('.', ',')}}%`;

      // Chart 1: Units Dia vs Noite
      const ctxTU = document.getElementById('turnoUnitsChart').getContext('2d');
      if (turnoUnitsChartInst) turnoUnitsChartInst.destroy();
      turnoUnitsChartInst = new Chart(ctxTU, {{
        type: 'bar',
        data: {{
          labels: unitSummaries.map(x => x.unit),
          datasets: [
            {{ label: '☀️ Venda Dia', data: unitSummaries.map(x => x.dia), backgroundColor: '#e0a233', borderRadius: 5 }},
            {{ label: '🌙 Venda Noite', data: unitSummaries.map(x => x.noite), backgroundColor: '#254c25', borderRadius: 5 }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ labels: {{ color: '#1f1b16' }} }} }},
          scales: {{
            x: {{ ticks: {{ color: '#2d2820', font: {{ weight: '600' }} }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#7c7263' }}, grid: {{ color: '#ece5d7' }} }}
          }}
        }}
      }});

      // Chart 2: Donut Dia vs Noite
      const ctxTD = document.getElementById('turnoDonutChart').getContext('2d');
      if (turnoDonutChartInst) turnoDonutChartInst.destroy();
      turnoDonutChartInst = new Chart(ctxTD, {{
        type: 'doughnut',
        data: {{
          labels: ['☀️ Venda Dia', '🌙 Venda Noite'],
          datasets: [{{
            data: [grandDia, grandNoite],
            backgroundColor: ['#e0a233', '#254c25'],
            borderColor: '#ffffff',
            borderWidth: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          cutout: '65%',
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#1f1b16', padding: 14, font: {{ weight: '600' }} }} }}
          }}
        }}
      }});

      // Monthly Comparison Chart & Table
      const mLabels = [], mDia = [], mNoite = [], monthlyRows = [];
      RAW_DATA.month_order.forEach(([mk, mlbl]) => {{
        let dSum = 0, nSum = 0;
        activeUnits.forEach(u => {{
          const mo = u.months[mk];
          if (!mo || (ignoreTpl && mo.is_template_copy)) return;
          const vals = getTurnoMonthVals(mo, mode);
          dSum += vals.dia;
          nSum += vals.noite;
        }});
        mLabels.push(mlbl);
        mDia.push(dSum);
        mNoite.push(nSum);
        monthlyRows.push({{ key: mk, label: mlbl, dia: dSum, noite: nSum, total: dSum + nSum }});
      }});

      // Best Month KPI
      let bestM = null;
      monthlyRows.forEach(r => {{
        if (isMonthSelected(r.key) && r.total > 0) {{
          if (!bestM || r.total > bestM.total) bestM = r;
        }}
      }});
      if (bestM) {{
        document.getElementById('tKpiBestMonthVal').textContent = formatVal(bestM.total, 'currency');
        document.getElementById('tKpiBestMonthBadge').textContent = bestM.label;
        document.getElementById('tKpiBestMonthSub').textContent = `☀️ ${{formatVal(bestM.dia, 'currency', true)}} | 🌙 ${{formatVal(bestM.noite, 'currency', true)}}`;
      }} else {{
        document.getElementById('tKpiBestMonthVal').textContent = 'R$ 0,00';
        document.getElementById('tKpiBestMonthBadge').textContent = '-';
        document.getElementById('tKpiBestMonthSub').textContent = '-';
      }}

      const mTableBody = document.getElementById('turnoMonthlyTableBody');
      mTableBody.innerHTML = '';
      monthlyRows.forEach((r, idx) => {{
        const pD = r.total > 0 ? (r.dia / r.total) * 100 : 0;
        const pN = r.total > 0 ? (r.noite / r.total) * 100 : 0;
        let varHtml = '<span style="color:var(--text-muted)">-</span>';
        if (idx > 0 && monthlyRows[idx - 1].total > 0 && r.total > 0) {{
          const diffPct = ((r.total - monthlyRows[idx - 1].total) / monthlyRows[idx - 1].total) * 100;
          const sign = diffPct >= 0 ? '▲ +' : '▼ ';
          const cls = diffPct >= 0 ? 'st-ok' : 'st-bad';
          varHtml = `<span class="status-pill ${{cls}}">${{sign}}${{diffPct.toFixed(1).replace('.', ',')}}%</span>`;
        }}
        const rowStyle = isMonthSelected(r.key) ? '' : 'opacity: 0.35;';
        mTableBody.innerHTML += `
          <tr style="${{rowStyle}}">
            <td><strong>${{r.label}}</strong></td>
            <td style="color:var(--dia-color);font-weight:600;">${{formatVal(r.dia, 'currency')}}</td>
            <td style="color:var(--noite-color);font-weight:600;">${{formatVal(r.noite, 'currency')}}</td>
            <td style="color:var(--vendas-color);font-weight:700;">${{formatVal(r.total, 'currency')}}</td>
            <td>${{pD.toFixed(1).replace('.', ',')}}%</td>
            <td>${{pN.toFixed(1).replace('.', ',')}}%</td>
            <td>${{varHtml}}</td>
          </tr>
        `;
      }});

      const ctxTM = document.getElementById('turnoMonthlyChart').getContext('2d');
      if (turnoMonthlyChartInst) turnoMonthlyChartInst.destroy();
      turnoMonthlyChartInst = new Chart(ctxTM, {{
        type: 'bar',
        data: {{
          labels: mLabels,
          datasets: [
            {{ label: '☀️ Venda Dia', data: mDia, backgroundColor: '#e0a233', borderRadius: 4 }},
            {{ label: '🌙 Venda Noite', data: mNoite, backgroundColor: '#254c25', borderRadius: 4 }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ labels: {{ color: '#1f1b16' }} }} }},
          scales: {{
            x: {{ ticks: {{ color: '#2d2820', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#7c7263' }}, grid: {{ color: '#ece5d7' }} }}
          }}
        }}
      }});

      // Weekly Comparison Chart & Table (WOM vs DOW)
      const consolidatedWom = WOM_META.map(w => ({{ ...w, dia: 0, noite: 0 }}));
      const consolidatedDow = DOW_LABELS.map(label => ({{ label, shortLabel: label, dia: 0, noite: 0 }}));

      activeUnits.forEach(u => {{
        const {{ wom, dow }} = computeTurnoWeeklyForUnit(u, isMonthSelected, mode, ignoreTpl);
        wom.forEach((w, i) => {{
          consolidatedWom[i].dia += w.dia;
          consolidatedWom[i].noite += w.noite;
        }});
        dow.forEach((d, i) => {{
          consolidatedDow[i].dia += d.dia;
          consolidatedDow[i].noite += d.noite;
        }});
      }});

      let bestW = consolidatedWom[0];
      consolidatedWom.forEach(w => {{ if ((w.dia + w.noite) > (bestW.dia + bestW.noite)) bestW = w; }});
      let bestD = consolidatedDow[0];
      consolidatedDow.forEach(d => {{ if ((d.dia + d.noite) > (bestD.dia + bestD.noite)) bestD = d; }});

      document.getElementById('tKpiBestWeekVal').textContent = formatVal(bestW.dia + bestW.noite, 'currency');
      document.getElementById('tKpiBestWeekBadge').textContent = bestW.shortLabel;
      document.getElementById('tKpiBestWeekSub').textContent = `Melhor dia sem.: ${{bestD.label}} (${{formatVal(bestD.dia + bestD.noite, 'currency', true)}})`;

      const weekItems = turnoWeeklyType === 'WOM' ? consolidatedWom : consolidatedDow;
      document.getElementById('turnoWeeklyColHeader').textContent = turnoWeeklyType === 'WOM' ? 'Semana do Mês' : 'Dia da Semana';
      document.getElementById('turnoWeeklySubtitle').textContent = turnoWeeklyType === 'WOM'
        ? 'Desempenho por Semana do Mês (Semana 1 a Semana 5)'
        : 'Desempenho acumulado por Dia da Semana (Segunda a Domingo)';

      const wTableBody = document.getElementById('turnoWeeklyTableBody');
      wTableBody.innerHTML = '';
      weekItems.forEach(item => {{
        const tot = item.dia + item.noite;
        const pD = tot > 0 ? (item.dia / tot) * 100 : 0;
        const pN = tot > 0 ? (item.noite / tot) * 100 : 0;
        wTableBody.innerHTML += `
          <tr>
            <td><strong>${{item.label}}</strong></td>
            <td style="color:var(--dia-color);font-weight:600;">${{formatVal(item.dia, 'currency')}}</td>
            <td style="color:var(--noite-color);font-weight:600;">${{formatVal(item.noite, 'currency')}}</td>
            <td style="color:var(--vendas-color);font-weight:700;">${{formatVal(tot, 'currency')}}</td>
            <td>${{pD.toFixed(1).replace('.', ',')}}%</td>
            <td>${{pN.toFixed(1).replace('.', ',')}}%</td>
          </tr>
        `;
      }});

      const ctxTW = document.getElementById('turnoWeeklyChart').getContext('2d');
      if (turnoWeeklyChartInst) turnoWeeklyChartInst.destroy();
      turnoWeeklyChartInst = new Chart(ctxTW, {{
        type: 'bar',
        data: {{
          labels: weekItems.map(x => x.shortLabel),
          datasets: [
            {{ label: '☀️ Venda Dia', data: weekItems.map(x => x.dia), backgroundColor: '#e0a233', borderRadius: 5 }},
            {{ label: '🌙 Venda Noite', data: weekItems.map(x => x.noite), backgroundColor: '#254c25', borderRadius: 5 }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ labels: {{ color: '#1f1b16' }} }} }},
          scales: {{
            x: {{ ticks: {{ color: '#2d2820' }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#7c7263' }}, grid: {{ color: '#ece5d7' }} }}
          }}
        }}
      }});

      // Render Week Date Cards & Daily Dates Breakdown at Bottom
      renderTurnoWeekDatesSection(consolidatedWom, activeUnits, isMonthSelected, mFilter, mode, ignoreTpl);

      // Render Separate Store Cards (Turnos Dia & Noite) AND Separate Nov 2025 vs Nov 2026 Projection Section
      const tBasis = document.getElementById('turnoNovProjBasisSelect') ? document.getElementById('turnoNovProjBasisSelect').value : 'META';
      renderTurnoStoreCards(unitSummaries, mode, uFilter);
      renderNovProjectionWidget('turno', uFilter, mode, tBasis);
    }}

    let semNovProjChartInst = null;
    let turnoNovProjChartInst = null;

    function onGlobalUnitChange(val) {{
      const sSel = document.getElementById('semUnitFilter');
      const tSel = document.getElementById('turnoUnitFilter');
      if (sSel && sSel.value !== val) sSel.value = val;
      if (tSel && tSel.value !== val) tSel.value = val;
      if (activeCategory === 'TURNOS') {{
        renderTurnosView();
      }} else {{
        renderSemanalView();
      }}
    }}

    function computeStoreNovProjection(u, mode) {{
      // 1. Nov 2025 Realizado
      const mNov25 = u.months['2025-11'];
      let nov25Dia = 0, nov25Noite = 0, nov25DelivDia = 0, nov25DelivNoite = 0, nov25Days = 0;
      if (mNov25 && !mNov25.is_template_copy) {{
        nov25Dia = mNov25.venda_dia || 0;
        nov25Noite = mNov25.venda_noite || 0;
        nov25DelivDia = mNov25.deliv_dia || 0;
        nov25DelivNoite = mNov25.deliv_noite || 0;
        (mNov25.daily || []).forEach(d => {{
          if ((d.venda_dia + d.venda_noite + d.deliv_dia + d.deliv_noite) > 0) nov25Days++;
        }});
      }}
      const nov25Salao = nov25Dia + nov25Noite;
      const nov25Deliv = nov25DelivDia + nov25DelivNoite;
      const nov25TotalFull = nov25Salao + nov25Deliv;
      const nov25TotalMode = mode === 'cantina_only' ? nov25Salao : nov25TotalFull;
      const nov25DiaMode = mode === 'cantina_only' ? nov25Dia : (nov25Dia + nov25DelivDia);
      const nov25NoiteMode = mode === 'cantina_only' ? nov25Noite : (nov25Noite + nov25DelivNoite);

      // 2. Recent Run-Rate (Ago, Set, Out 2026) -> 30 days for Nov 2026
      let recDays = 0, recDia = 0, recNoite = 0, recDelD = 0, recDelN = 0;
      ['2026-08', '2026-09', '2026-10'].forEach(mk => {{
        const mo = u.months[mk];
        if (!mo || mo.is_template_copy) return;
        (mo.daily || []).forEach(d => {{
          const t = (d.venda_dia || 0) + (d.venda_noite || 0) + (d.deliv_dia || 0) + (d.deliv_noite || 0);
          if (t > 0) {{
            recDays++;
            recDia += (d.venda_dia || 0);
            recNoite += (d.venda_noite || 0);
            recDelD += (d.deliv_dia || 0);
            recDelN += (d.deliv_noite || 0);
          }}
        }});
      }});
      const recSalao = recDia + recNoite;
      const recDeliv = recDelD + recDelN;
      const projRitmoDiaCantina = recDays > 0 ? (recDia / recDays) * 30 : 0;
      const projRitmoNoiteCantina = recDays > 0 ? (recNoite / recDays) * 30 : 0;
      const projRitmoSalao = projRitmoDiaCantina + projRitmoNoiteCantina;
      const projRitmoDelivDia = recDays > 0 ? (recDelD / recDays) * 30 : 0;
      const projRitmoDelivNoite = recDays > 0 ? (recDelN / recDays) * 30 : 0;
      const projRitmoDeliv = projRitmoDelivDia + projRitmoDelivNoite;
      const projRitmoTotalFull = projRitmoSalao + projRitmoDeliv;

      const recDiaMode = mode === 'cantina_only' ? recDia : (recDia + recDelD);
      const recNoiteMode = mode === 'cantina_only' ? recNoite : (recNoite + recDelN);
      const recTotMode = recDiaMode + recNoiteMode;
      const projRitmo30 = recDays > 0 ? (recTotMode / recDays) * 30 : 0;
      const shareDia26 = recTotMode > 0 ? (recDiaMode / recTotMode) : 0.5;
      const shareNoite26 = recTotMode > 0 ? (recNoiteMode / recTotMode) : 0.5;
      const shareDiaCantina = recSalao > 0 ? (recDia / recSalao) : 0.45;
      const shareNoiteCantina = recSalao > 0 ? (recNoite / recSalao) : 0.55;
      const shareDelivDia = recDeliv > 0 ? (recDelD / recDeliv) : 0.5;
      const shareDelivNoite = recDeliv > 0 ? (recDelN / recDeliv) : 0.5;

      // 3. Average Monthly 2026 (Jan..Sep full months + Oct scaled to 30d)
      let m26List = [];
      ['2026-01','2026-02','2026-03','2026-04','2026-05','2026-06','2026-07','2026-08','2026-09','2026-10'].forEach(mk => {{
        const mo = u.months[mk];
        if (!mo || mo.is_template_copy) return;
        const vals = getTurnoMonthVals(mo, mode);
        const tot = vals.dia + vals.noite;
        if (tot > 0) {{
          if (mk === '2026-10') {{
            let octDays = 0;
            (mo.daily || []).forEach(d => {{
              if ((d.venda_dia + d.venda_noite + d.deliv_dia + d.deliv_noite) > 0) octDays++;
            }});
            m26List.push(octDays > 0 && octDays < 28 ? (tot / octDays) * 30 : tot);
          }} else {{
            m26List.push(tot);
          }}
        }}
      }});
      const projMedia26 = m26List.length > 0 ? (m26List.reduce((a, b) => a + b, 0) / m26List.length) : projRitmo30;

      // 4. Official Nov 2026 Meta from SEMANAL
      const nm = u.nov2026_meta || {{}};
      const metaSalaoNov26 = nm.meta_cantina || 0;
      const metaDelivNov26 = nm.meta_deliv || 0;
      const metaTotalFullNov26 = nm.meta_total || 0;
      const metaNov26 = mode === 'cantina_only' ? metaSalaoNov26 : metaTotalFullNov26;
      const isRefOct = !!nm.is_ref_oct;

      // 5. Weekly Breakdown for Nov 2026 vs Nov 2025 (Standard 5 Weeks of November: 01-07, 08-14, 15-21, 22-28, 29-30)
      const stdWeeksNov = [
        {{ week: 'W1', shortLabel: 'Semana 1', label: 'Semana 1 (01 a 07/Nov)', min_day: 1, max_day: 7 }},
        {{ week: 'W2', shortLabel: 'Semana 2', label: 'Semana 2 (08 a 14/Nov)', min_day: 8, max_day: 14 }},
        {{ week: 'W3', shortLabel: 'Semana 3', label: 'Semana 3 (15 a 21/Nov)', min_day: 15, max_day: 21 }},
        {{ week: 'W4', shortLabel: 'Semana 4', label: 'Semana 4 (22 a 28/Nov)', min_day: 22, max_day: 28 }},
        {{ week: 'W5', shortLabel: 'Semana 5', label: 'Semana 5 (29 a 30/Nov)', min_day: 29, max_day: 30 }}
      ];

      const rawWeeks = stdWeeksNov.map((w) => {{
        const dMin = w.min_day;
        const dMax = w.max_day;
        const nDaysW = Math.max(1, dMax - dMin + 1);
        let w25Dia = 0, w25Noite = 0;
        if (mNov25 && !mNov25.is_template_copy) {{
          (mNov25.daily || []).forEach(dRow => {{
            if (dRow.dia >= dMin && dRow.dia <= dMax) {{
              const dv = getTurnoDayVals(dRow, mode);
              w25Dia += dv.dia;
              w25Noite += dv.noite;
            }}
          }});
        }}
        const w25Tot = w25Dia + w25Noite;
        return {{
          week: w.week,
          shortLabel: w.shortLabel,
          label: w.label,
          min_day: dMin,
          max_day: dMax,
          days: nDaysW,
          nov25Dia: w25Dia,
          nov25Noite: w25Noite,
          nov25Total: w25Tot
        }};
      }});

      const fullMonthNov25 = nov25Days >= 25 && nov25TotalMode > 0;
      const weeklyComp = rawWeeks.map(rw => {{
        const weight = fullMonthNov25 ? (rw.nov25Total / nov25TotalMode) : (rw.days / 30);
        const wMeta26 = (metaNov26 || projRitmo30) * weight;
        const wRitmo26 = projRitmo30 * weight;
        const wMedia26 = projMedia26 * weight;
        return {{
          ...rw,
          weight,
          ritmoNov26: wRitmo26,
          mediaNov26: wMedia26,
          metaNov26: wMeta26
        }};
      }});

      return {{
        unit: u.unit,
        unit_key: u.unit_key,
        is_dk: u.is_dk,
        nov25DiaCantina: nov25Dia,
        nov25NoiteCantina: nov25Noite,
        nov25DelivDia,
        nov25DelivNoite,
        nov25Dia: nov25DiaMode,
        nov25Noite: nov25NoiteMode,
        nov25Salao,
        nov25Deliv,
        nov25TotalFull,
        nov25Total: nov25TotalMode,
        nov25Days,
        hasNov25: nov25TotalMode > 0,
        projRitmoDiaCantina,
        projRitmoNoiteCantina,
        projRitmoSalao,
        projRitmoDelivDia,
        projRitmoDelivNoite,
        projRitmoDeliv,
        projRitmoTotalFull,
        projRitmo30,
        projMedia26,
        metaSalaoNov26,
        metaDelivNov26,
        metaTotalFullNov26,
        metaNov26,
        isRefOct,
        shareDia26,
        shareNoite26,
        shareDiaCantina,
        shareNoiteCantina,
        shareDelivDia,
        shareDelivNoite,
        weeklyComp
      }};
    }}

    function onNovBasisChange(val) {{
      const sB = document.getElementById('semNovProjBasisSelect');
      const tB = document.getElementById('turnoNovProjBasisSelect');
      if (sB && sB.value !== val) sB.value = val;
      if (tB && tB.value !== val) tB.value = val;
      if (activeCategory === 'TURNOS') {{
        renderTurnosView();
      }} else {{
        renderNovProjectionAll();
      }}
    }}

    function renderNovProjectionAll() {{
      const uFilter = document.getElementById('semUnitFilter') ? document.getElementById('semUnitFilter').value : 'ALL';
      const mode = document.getElementById('semNovModeSelect') ? document.getElementById('semNovModeSelect').value : 'cantina_plus_delivery';
      const basis = document.getElementById('semNovProjBasisSelect') ? document.getElementById('semNovProjBasisSelect').value : 'META';
      renderNovProjectionWidget('sem', uFilter, mode, basis);
    }}

    function renderNovProjectionWidget(prefix, uFilter, mode, basis) {{
      // 1. Render Store Selector Pills inside the Projection Card
      const pillsEl = document.getElementById(prefix + 'NovStorePills');
      if (pillsEl) {{
        pillsEl.innerHTML = '';
        const allBtn = document.createElement('button');
        allBtn.className = 'ind-pill' + (uFilter === 'ALL' ? ' active' : '');
        allBtn.textContent = '🏢 Todas as Lojas (8)';
        allBtn.onclick = () => onGlobalUnitChange('ALL');
        pillsEl.appendChild(allBtn);

        RAW_DATA.units.forEach(u => {{
          const btn = document.createElement('button');
          btn.className = 'ind-pill' + (uFilter === u.unit ? ' active' : '');
          btn.textContent = '📍 ' + u.unit;
          btn.onclick = () => onGlobalUnitChange(u.unit);
          pillsEl.appendChild(btn);
        }});
      }}

      const titleEl = document.getElementById(prefix + 'NovTitle');
      const subEl = document.getElementById(prefix + 'NovSubtitle');
      const bannerEl = document.getElementById(prefix + 'NovSummaryBanner');
      const theadEl = document.getElementById(prefix + 'NovProjTableHead');
      const tbody = document.getElementById(prefix + 'NovProjTableBody');
      const kpiBox = document.getElementById(prefix + 'NovKpiGrid');
      const canvasEl = document.getElementById(prefix + 'NovProjChart');

      const fmtVarBadge = (base, target) => {{
        if (!base || base <= 0) return '<span class="status-pill st-none">🆕 Sem venda Nov/25</span>';
        const p = ((target - base) / base) * 100;
        const cls = p >= 0 ? 'st-ok' : (p >= -5 ? 'st-warn' : 'st-bad');
        const s = p >= 0 ? '▲ +' : '▼ ';
        return `<span class="status-pill ${{cls}}">${{s}}${{p.toFixed(1).replace('.', ',')}}%</span>`;
      }};

      const targetUnits = uFilter === 'ALL'
        ? RAW_DATA.units
        : [RAW_DATA.units.find(u => u.unit === uFilter) || RAW_DATA.units[0]];

      const storeProjections = targetUnits.map(u => {{
        const st = computeStoreNovProjection(u, mode);
        const chosenProj = basis === 'META' ? (st.metaNov26 || st.projRitmo30) : (basis === 'RITMO' ? st.projRitmo30 : st.projMedia26);
        const projDia = chosenProj * st.shareDia26;
        const projNoite = chosenProj * st.shareNoite26;
        const weeks = st.weeklyComp.map(wk => {{
          const w26Tot = basis === 'META' ? wk.metaNov26 : (basis === 'RITMO' ? wk.ritmoNov26 : wk.mediaNov26);
          const w26Dia = w26Tot * st.shareDia26;
          const w26Noite = w26Tot * st.shareNoite26;
          return {{
            ...wk,
            proj26Dia: w26Dia,
            proj26Noite: w26Noite,
            proj26Total: w26Tot
          }};
        }});
        return {{
          ...st,
          chosenProj,
          projDia,
          projNoite,
          weeks
        }};
      }});

      // Aggregate the 5 Weeks across selected store(s)
      const aggWeeks = [0, 1, 2, 3, 4].map(idx => {{
        const baseW = storeProjections[0].weeks[idx];
        let v25Dia = 0, v25Noite = 0, v25Total = 0;
        let v26Dia = 0, v26Noite = 0, v26Total = 0;
        storeProjections.forEach(sp => {{
          const w = sp.weeks[idx];
          v25Dia += w.nov25Dia;
          v25Noite += w.nov25Noite;
          v25Total += w.nov25Total;
          v26Dia += w.proj26Dia;
          v26Noite += w.proj26Noite;
          v26Total += w.proj26Total;
        }});
        return {{
          week: baseW.week,
          shortLabel: baseW.shortLabel,
          label: baseW.label,
          min_day: baseW.min_day,
          max_day: baseW.max_day,
          days: baseW.days,
          v25Dia,
          v25Noite,
          v25Total,
          v26Dia,
          v26Noite,
          v26Total
        }};
      }});

      let tot25Dia = 0, tot25Noite = 0, tot25 = 0;
      let tot26Dia = 0, tot26Noite = 0, tot26 = 0;
      aggWeeks.forEach(w => {{
        tot25Dia += w.v25Dia;
        tot25Noite += w.v25Noite;
        tot25 += w.v25Total;
        tot26Dia += w.v26Dia;
        tot26Noite += w.v26Noite;
        tot26 += w.v26Total;
      }});

      const scopeTitle = uFilter === 'ALL' ? 'Todas as Lojas (Rede)' : `📍 ${{storeProjections[0].unit}}`;

      if (titleEl) {{
        titleEl.innerHTML = `🔮 Projeção de Novembro Semana a Semana — <span style="color:#254c25;">${{scopeTitle}}</span>`;
      }}
      if (subEl) {{
        subEl.textContent = `Veja direto para ${{uFilter === 'ALL' ? 'a rede' : 'a loja ' + storeProjections[0].unit}}: quanto vendeu em cada semana de Novembro/2025 e quanto tem que vender em cada semana de Novembro/2026`;
      }}

      if (bannerEl) {{
        bannerEl.innerHTML = '';
        bannerEl.style.display = 'none';
      }}

      // Render 6 Direct Cards: Semana 1, Semana 2, Semana 3, Semana 4, Semana 5 + Total de Novembro
      if (kpiBox) {{
        kpiBox.style.gridTemplateColumns = 'repeat(auto-fit, minmax(290px, 1fr))';
        const cardsData = [
          ...aggWeeks.map(w => ({{
            title: `🗓️ Novembro ${{w.shortLabel}} (${{String(w.min_day).padStart(2,'0')}} a ${{String(w.max_day).padStart(2,'0')}}/Nov)`,
            badge: `${{w.days}} dias`,
            v25: w.v25Total,
            v25Dia: w.v25Dia,
            v25Noite: w.v25Noite,
            v26: w.v26Total,
            v26Dia: w.v26Dia,
            v26Noite: w.v26Noite,
            isTotal: false
          }})),
          {{
            title: `💰 TOTAL MÊS DE NOVEMBRO (01 a 30/Nov)`,
            badge: `30 dias (${{scopeTitle}})`,
            v25: tot25,
            v25Dia: tot25Dia,
            v25Noite: tot25Noite,
            v26: tot26,
            v26Dia: tot26Dia,
            v26Noite: tot26Noite,
            isTotal: true
          }}
        ];

        kpiBox.innerHTML = cardsData.map(c => {{
          const diff = c.v26 - c.v25;
          const pct = c.v25 > 0 ? (diff / c.v25) * 100 : null;
          const borderColor = c.isTotal ? '#c92535' : '#254c25';
          const bgCard = c.isTotal ? '#eef4ee' : 'var(--card-bg)';
          return `
            <div class="kpi-card" style="border-top: 3px solid ${{borderColor}}; background: ${{bgCard}}; padding: 14px 16px;">
              <div class="kpi-header" style="margin-bottom: 10px;">
                <span class="kpi-title" style="font-size:0.82rem; color:#1f1b16; font-weight:800;">${{c.title}}</span>
                <span class="kpi-badge" style="color:${{c.isTotal ? '#34d399' : '#d8b4fe'}};">${{c.badge}}</span>
              </div>

              <div style="background:#fbf7ef; border:1px solid #ece5d7; border-left:4px solid #9d9384; padding:8px 10px; border-radius:6px; margin-bottom:8px;">
                <div style="font-size:0.70rem; color:#7c7263; font-weight:700; text-transform:uppercase;">📅 Em Novembro/2025 vendeu:</div>
                <div style="font-size:1.15rem; font-weight:800; color:#1f1b16; margin:2px 0;">
                  ${{c.v25 > 0 ? formatVal(c.v25, 'currency') : '<span style="color:#64748b;font-size:0.92rem;">Sem operação em Nov/25</span>'}}
                </div>
                <div style="font-size:0.70rem; color:#5d5446;">
                  ${{c.v25 > 0 ? `☀️ Dia: ${{formatVal(c.v25Dia, 'currency', true)}} &nbsp;|&nbsp; 🌙 Noite: ${{formatVal(c.v25Noite, 'currency', true)}}` : 'Unidade inaugurada em 2026'}}
                </div>
              </div>

              <div style="background:#eef4ee; border:1px solid #bcd5bc; border-left:4px solid #254c25; padding:8px 10px; border-radius:6px; margin-bottom:8px;">
                <div style="font-size:0.70rem; color:#254c25; font-weight:700; text-transform:uppercase;">🎯 Para Novembro/2026 tem que vender:</div>
                <div style="font-size:1.22rem; font-weight:900; color:#254c25; margin:2px 0;">
                  ${{formatVal(c.v26, 'currency')}}
                </div>
                <div style="font-size:0.70rem; color:#254c25;">
                  ☀️ Dia: ${{formatVal(c.v26Dia, 'currency', true)}} &nbsp;|&nbsp; 🌙 Noite: ${{formatVal(c.v26Noite, 'currency', true)}}
                </div>
              </div>

              <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.74rem; padding-top:4px; border-top:1px solid #ece5d7;">
                <span style="color:#7c7263;">Diferença (2026 vs 2025):</span>
                <strong style="color:${{diff >= 0 ? '#34d399' : '#fb7185'}};">
                  ${{c.v25 > 0 ? `${{diff >= 0 ? '+' : ''}}${{formatVal(diff, 'currency')}} (${{pct >= 0 ? '▲ +' : '▼ '}}${{pct.toFixed(1).replace('.', ',')}}%)` : `+${{formatVal(c.v26, 'currency')}} (Nova)`}}
                </strong>
              </div>
            </div>
          `;
        }}).join('');
      }}

      // Render Weekly Chart: Semana 1 to Semana 5 (Vendeu em Nov/2025 vs Tem que Vender em Nov/2026)
      if (canvasEl) {{
        const ctx = canvasEl.getContext('2d');
        if (prefix === 'sem' && semNovProjChartInst) semNovProjChartInst.destroy();
        if (prefix === 'turno' && turnoNovProjChartInst) turnoNovProjChartInst.destroy();

        const chartCfg = {{
          type: 'bar',
          data: {{
            labels: aggWeeks.map(w => `${{w.shortLabel}} (${{String(w.min_day).padStart(2,'0')}}–${{String(w.max_day).padStart(2,'0')}}/Nov)`),
            datasets: [
              {{
                label: `📅 Novembro/2025 Vendeu (${{scopeTitle}})`,
                data: aggWeeks.map(w => +w.v25Total.toFixed(2)),
                backgroundColor: '#c2b9a9',
                borderRadius: 6
              }},
              {{
                label: `🎯 Para Novembro/2026 Tem que Vender (${{scopeTitle}})`,
                data: aggWeeks.map(w => +w.v26Total.toFixed(2)),
                backgroundColor: '#254c25',
                borderRadius: 6
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ labels: {{ color: '#1f1b16', font: {{ family: 'Mulish', size: 12, weight: '700' }} }} }}
            }},
            scales: {{
              x: {{ ticks: {{ color: '#1f1b16', font: {{ weight: '700' }} }}, grid: {{ display: false }} }},
              y: {{ ticks: {{ color: '#7c7263' }}, grid: {{ color: '#ece5d7' }} }}
            }}
          }}
        }};

        if (prefix === 'sem') semNovProjChartInst = new Chart(ctx, chartCfg);
        else turnoNovProjChartInst = new Chart(ctx, chartCfg);
      }}

      // Render Table: Semana 1 to Semana 5 + Total de Novembro
      if (theadEl) {{
        theadEl.innerHTML = `
          <tr>
            <th>Semana de Novembro — ${{scopeTitle}}</th>
            <th class="col-sep">📅 Em Novembro/2025 Vendeu</th>
            <th class="col-sep">🎯 Para Novembro/2026 Tem que Vender</th>
            <th class="col-sep">💰 Quanto Tem que Vender a Mais (R$)</th>
            <th>📈 Variação %</th>
            <th>📌 Resumo Direto da Semana</th>
          </tr>
        `;
      }}

      if (tbody) {{
        let html = '';
        aggWeeks.forEach(w => {{
          const dVal = w.v26Total - w.v25Total;
          const resumoFrase = w.v25Total > 0
            ? `Em Nov/25 vendeu <strong>${{formatVal(w.v25Total, 'currency')}}</strong> ➔ Para Nov/26 tem que vender <strong style="color:#254c25;">${{formatVal(w.v26Total, 'currency')}}</strong>`
            : `Sem venda em Nov/25 ➔ Para Nov/26 tem que vender <strong style="color:#254c25;">${{formatVal(w.v26Total, 'currency')}}</strong>`;

          html += `
            <tr>
              <td>
                <strong>🗓️ ${{w.label}}</strong>
                <div style="font-size:0.68rem;color:var(--text-muted);">${{w.days}} dias do mês</div>
              </td>
              <td class="col-sep">
                <div style="font-weight:800;color:#1f1b16;font-size:0.90rem;">${{w.v25Total > 0 ? formatVal(w.v25Total, 'currency') : '<span style="color:var(--text-muted)">Sem operação</span>'}}</div>
                <div style="font-size:0.68rem;color:#7c7263;margin-top:2px;">${{w.v25Total > 0 ? `☀️ Dia: ${{formatVal(w.v25Dia, 'currency', true)}} | 🌙 Noite: ${{formatVal(w.v25Noite, 'currency', true)}}` : '-'}}</div>
              </td>
              <td class="col-sep" style="background:#fbf7ef;">
                <div style="font-weight:900;color:#254c25;font-size:0.94rem;">${{formatVal(w.v26Total, 'currency')}}</div>
                <div style="font-size:0.68rem;color:#5d5446;margin-top:2px;">☀️ Dia: ${{formatVal(w.v26Dia, 'currency', true)}} | 🌙 Noite: ${{formatVal(w.v26Noite, 'currency', true)}}</div>
              </td>
              <td class="col-sep" style="font-weight:800;color:${{dVal >= 0 ? '#34d399' : '#fb7185'}};">
                ${{dVal >= 0 ? '+' : ''}}${{formatVal(dVal, 'currency')}}
              </td>
              <td>${{fmtVarBadge(w.v25Total, w.v26Total)}}</td>
              <td style="font-size:0.78rem;color:#2d2820;">${{resumoFrase}}</td>
            </tr>
          `;
        }});

        const totDiff = tot26 - tot25;
        html += `
          <tr style="background:#eef4ee;border-top:2px solid #254c25;">
            <td><strong>💰 TOTAL DE NOVEMBRO (01 a 30/Nov) — ${{scopeTitle}}</strong></td>
            <td class="col-sep">
              <div style="font-weight:900;color:#1f1b16;font-size:0.95rem;">${{tot25 > 0 ? formatVal(tot25, 'currency') : '-'}}</div>
              <div style="font-size:0.68rem;color:#7c7263;">☀️ Dia: ${{formatVal(tot25Dia, 'currency', true)}} | 🌙 Noite: ${{formatVal(tot25Noite, 'currency', true)}}</div>
            </td>
            <td class="col-sep">
              <div style="font-weight:900;color:#254c25;font-size:0.98rem;">${{formatVal(tot26, 'currency')}}</div>
              <div style="font-size:0.68rem;color:#5d5446;">☀️ Dia: ${{formatVal(tot26Dia, 'currency', true)}} | 🌙 Noite: ${{formatVal(tot26Noite, 'currency', true)}}</div>
            </td>
            <td class="col-sep" style="font-weight:900;color:${{totDiff >= 0 ? '#34d399' : '#fb7185'}};">
              ${{totDiff >= 0 ? '+' : ''}}${{formatVal(totDiff, 'currency')}}
            </td>
            <td>${{fmtVarBadge(tot25, tot26)}}</td>
            <td style="font-size:0.80rem;font-weight:700;color:#1f1b16;">
              No mês todo: vendeu ${{formatVal(tot25, 'currency')}} em Nov/25 ➔ Tem que vender <span style="color:#254c25;">${{formatVal(tot26, 'currency')}}</span> em Nov/26
            </td>
          </tr>
        `;

        // If viewing ALL stores, also show each store's row right below so the user can click any store
        if (uFilter === 'ALL') {{
          html += `
            <tr style="background:#f6f1e7;">
              <td colspan="6" style="text-align:left;font-weight:800;color:#254c25;padding:10px 12px;">
                🏢 Resumo por Loja (Clique em uma loja para ver as 5 Semanas de Novembro exclusivamente dela)
              </td>
            </tr>
          `;
          storeProjections.forEach(sp => {{
            const dVal = sp.chosenProj - sp.nov25Total;
            const fraseLoja = sp.hasNov25
              ? `Em Nov/25 vendeu <strong>${{formatVal(sp.nov25Total, 'currency')}}</strong> ➔ Para Nov/26 tem que vender <strong style="color:#254c25;">${{formatVal(sp.chosenProj, 'currency')}}</strong>`
              : `Nova loja em 2026 ➔ Para Nov/26 tem que vender <strong style="color:#254c25;">${{formatVal(sp.chosenProj, 'currency')}}</strong>`;
            html += `
              <tr class="clickable-row" onclick="onGlobalUnitChange('${{sp.unit}}')">
                <td><strong>📍 ${{sp.unit}}</strong> <span style="font-size:0.68rem;color:#a855f7;">(Clique p/ ver Semanas 1 a 5)</span></td>
                <td class="col-sep">
                  <div style="font-weight:800;color:#1f1b16;">${{sp.hasNov25 ? formatVal(sp.nov25Total, 'currency') : '<span style="color:var(--text-muted)">Iniciou em 2026</span>'}}</div>
                  <div style="font-size:0.68rem;color:#7c7263;">${{sp.hasNov25 ? `☀️ Dia: ${{formatVal(sp.nov25Dia, 'currency', true)}} | 🌙 Noite: ${{formatVal(sp.nov25Noite, 'currency', true)}}` : '-'}}</div>
                </td>
                <td class="col-sep">
                  <div style="font-weight:800;color:#254c25;">${{formatVal(sp.chosenProj, 'currency')}}</div>
                  <div style="font-size:0.68rem;color:#5d5446;">☀️ Dia: ${{formatVal(sp.projDia, 'currency', true)}} | 🌙 Noite: ${{formatVal(sp.projNoite, 'currency', true)}}</div>
                </td>
                <td class="col-sep" style="font-weight:800;color:${{dVal >= 0 ? '#34d399' : '#fb7185'}};">
                  ${{dVal >= 0 ? '+' : ''}}${{formatVal(dVal, 'currency')}}
                </td>
                <td>${{fmtVarBadge(sp.nov25Total, sp.chosenProj)}}</td>
                <td style="font-size:0.78rem;color:#2d2820;">${{fraseLoja}}</td>
              </tr>
            `;
          }});
        }}

        tbody.innerHTML = html;
      }}
    }}

    // Separate Store Cards: ONLY Turnos Dia & Noite for the selected period!
    function renderTurnoStoreCards(unitSummaries, mode, uFilter) {{
      const box = document.getElementById('turnoStoreCardsContainer');
      if (!box) return;
      box.innerHTML = '';

      unitSummaries.forEach(us => {{
        const pD = us.total > 0 ? (us.dia / us.total) * 100 : 50;
        const pN = us.total > 0 ? (us.noite / us.total) * 100 : 50;
        const isSelected = uFilter === us.unit;

        const card = document.createElement('div');
        card.className = 'unit-card-turno';
        if (isSelected) card.style.borderColor = '#10b981';
        card.innerHTML = `
          <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);padding-bottom:8px;">
            <h3 style="font-size:1rem;font-weight:800;">📍 ${{us.unit}} ${{us.is_dk ? '<span class="kpi-badge">Dark Kitchen</span>' : ''}}</h3>
            <button class="ind-pill ${{isSelected ? 'active' : ''}}" onclick="onGlobalUnitChange('${{isSelected ? 'ALL' : us.unit}}')">
              ${{isSelected ? '✅ Loja Selecionada (Ver Todas)' : '🔮 Isolar Loja & Projeção Nov/26'}}
            </button>
          </div>

          <div class="unit-metrics-3">
            <div class="um-box">
              <div class="lbl"><span>☀️ Venda Dia</span><span>${{pD.toFixed(0)}}%</span></div>
              <div class="val" style="color:var(--dia-color);">${{formatVal(us.dia, 'currency')}}</div>
              <div class="sub">${{Math.round(us.qtd_dia).toLocaleString('pt-BR')}} atendimentos</div>
            </div>
            <div class="um-box">
              <div class="lbl"><span>🌙 Venda Noite</span><span>${{pN.toFixed(0)}}%</span></div>
              <div class="val" style="color:var(--noite-color);">${{formatVal(us.noite, 'currency')}}</div>
              <div class="sub">${{Math.round(us.qtd_noite).toLocaleString('pt-BR')}} atendimentos</div>
            </div>
            <div class="um-box">
              <div class="lbl"><span>💰 Total Período</span></div>
              <div class="val" style="color:var(--vendas-color);">${{formatVal(us.total, 'currency')}}</div>
              <div class="sub">${{mode === 'cantina_only' ? 'Apenas Cantina' : 'Cantina + Delivery'}}</div>
            </div>
          </div>

          <div class="split-bar-wrap">
            <div class="split-bar-labels">
              <span style="color:var(--dia-color);">☀️ Dia ${{pD.toFixed(1).replace('.', ',')}}%</span>
              <span style="color:var(--noite-color);">🌙 Noite ${{pN.toFixed(1).replace('.', ',')}}%</span>
            </div>
            <div class="split-bar-track">
              <div class="split-fill-dia" style="width:${{pD}}%"></div>
              <div class="split-fill-noite" style="width:${{pN}}%"></div>
            </div>
          </div>
        `;
        box.appendChild(card);
      }});
    }}

    let turnoDailyDatesChartInst = null;

    function renderTurnoWeekDatesSection(consolidatedWom, activeUnits, isMonthSelected, mFilter, mode, ignoreTpl) {{
      const cardsBox = document.getElementById('turnoWeekDateCardsContainer');
      cardsBox.innerHTML = '';

      const singleM = !['ALL', 'YEAR_2025', 'YEAR_2026'].includes(mFilter);
      const monthLabelObj = RAW_DATA.month_order.find(([k]) => k === mFilter);
      const mShort = monthLabelObj ? monthLabelObj[1] : '';

      const grandTotalWeeks = consolidatedWom.reduce((acc, w) => acc + w.dia + w.noite, 0);

      consolidatedWom.forEach((w, idx) => {{
        const tot = w.dia + w.noite;
        const pD = tot > 0 ? (w.dia / tot) * 100 : 50;
        const pN = tot > 0 ? (w.noite / tot) * 100 : 50;
        const shareOfMonth = grandTotalWeeks > 0 ? (tot / grandTotalWeeks) * 100 : 0;
        const dateTitle = singleM
          ? `De ${{String(w.min).padStart(2,'0')}} a ${{String(w.max).padStart(2,'0')}} (${{mShort}})`
          : `De ${{String(w.min).padStart(2,'0')}} a ${{String(w.max).padStart(2,'0')}} do mês`;

        const card = document.createElement('div');
        card.className = 'kpi-card';
        card.style.borderTop = '3px solid #a855f7';
        card.innerHTML = `
          <div class="kpi-header">
            <span class="kpi-title">🗓️ ${{w.shortLabel}} (${{dateTitle}})</span>
            <span class="kpi-badge" style="color:#254c25;">${{shareOfMonth.toFixed(1).replace('.', ',')}}% do total</span>
          </div>
          <div class="kpi-value" style="color:var(--vendas-color);margin:4px 0;">${{formatVal(tot, 'currency')}}</div>
          <div style="font-size:0.74rem;color:var(--text-muted);margin-bottom:8px;">
            De ${{w.min}} a ${{w.max}} vendeu <strong style="color:var(--text);">${{formatVal(tot, 'currency')}}</strong>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:0.74rem;margin-bottom:4px;">
            <span style="color:var(--dia-color);font-weight:700;">☀️ ${{formatVal(w.dia, 'currency', true)}} (${{tot > 0 ? pD.toFixed(0) : 0}}%)</span>
            <span style="color:var(--noite-color);font-weight:700;">🌙 ${{formatVal(w.noite, 'currency', true)}} (${{tot > 0 ? pN.toFixed(0) : 0}}%)</span>
          </div>
          <div class="split-bar-track">
            <div class="split-fill-dia" style="width:${{pD}}%"></div>
            <div class="split-fill-noite" style="width:${{pN}}%"></div>
          </div>
        `;
        cardsBox.appendChild(card);
      }});

      // Aggregate days 1..31 across selected units & months
      const daysAgg = [];
      for (let d = 1; d <= 31; d++) {{
        const wObj = WOM_META.find(w => d >= w.min && d <= w.max) || WOM_META[4];
        daysAgg.push({{
          dia: d,
          weekLabel: `De ${{String(wObj.min).padStart(2,'0')}} a ${{String(wObj.max).padStart(2,'0')}} (${{wObj.shortLabel}})`,
          vDia: 0,
          vNoite: 0
        }});
      }}

      activeUnits.forEach(u => {{
        RAW_DATA.month_order.forEach(([mk]) => {{
          if (!isMonthSelected(mk)) return;
          const mo = u.months[mk];
          if (!mo || (ignoreTpl && mo.is_template_copy)) return;
          mo.daily.forEach(dRow => {{
            if (dRow.dia >= 1 && dRow.dia <= 31) {{
              const vals = getTurnoDayVals(dRow, mode);
              daysAgg[dRow.dia - 1].vDia += vals.dia;
              daysAgg[dRow.dia - 1].vNoite += vals.noite;
            }}
          }});
        }});
      }});

      // Render Chart of Daily Sales (Days 1 to 31)
      const ctxDD = document.getElementById('turnoDailyDatesChart').getContext('2d');
      if (turnoDailyDatesChartInst) turnoDailyDatesChartInst.destroy();
      turnoDailyDatesChartInst = new Chart(ctxDD, {{
        type: 'bar',
        data: {{
          labels: daysAgg.map(x => `Dia ${{String(x.dia).padStart(2,'0')}}`),
          datasets: [
            {{ label: '☀️ Venda Dia', data: daysAgg.map(x => x.vDia), backgroundColor: '#e0a233', borderRadius: 3 }},
            {{ label: '🌙 Venda Noite', data: daysAgg.map(x => x.vNoite), backgroundColor: '#254c25', borderRadius: 3 }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ labels: {{ color: '#1f1b16' }} }} }},
          scales: {{
            x: {{ ticks: {{ color: '#2d2820', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#7c7263' }}, grid: {{ color: '#ece5d7' }} }}
          }}
        }}
      }});

      // Populate Table: First the 5 Week Date Ranges summary rows, then Days 1..31
      const tbody = document.getElementById('turnoDailyDatesTableBody');
      tbody.innerHTML = '';

      consolidatedWom.forEach(w => {{
        const tot = w.dia + w.noite;
        if (tot === 0) return;
        const pD = (w.dia / tot) * 100;
        const pN = (w.noite / tot) * 100;
        tbody.innerHTML += `
          <tr style="background:#eef4ee;">
            <td><strong>🗓️ De ${{String(w.min).padStart(2,'0')}} a ${{String(w.max).padStart(2,'0')}} ${{mShort ? '('+mShort+')' : ''}}</strong></td>
            <td><span class="status-pill st-ok">${{w.shortLabel}}</span></td>
            <td style="color:var(--dia-color);font-weight:700;">${{formatVal(w.dia, 'currency')}}</td>
            <td style="color:var(--noite-color);font-weight:700;">${{formatVal(w.noite, 'currency')}}</td>
            <td style="color:var(--vendas-color);font-weight:800;">${{formatVal(tot, 'currency')}}</td>
            <td>${{pD.toFixed(1).replace('.', ',')}}%</td>
            <td>${{pN.toFixed(1).replace('.', ',')}}%</td>
          </tr>
        `;
      }});

      daysAgg.forEach(d => {{
        const tot = d.vDia + d.vNoite;
        if (tot === 0) return;
        const pD = (d.vDia / tot) * 100;
        const pN = (d.vNoite / tot) * 100;
        tbody.innerHTML += `
          <tr>
            <td>Dia ${{String(d.dia).padStart(2,'0')}} ${{mShort ? 'de '+mShort : ''}}</td>
            <td style="color:var(--text-muted);">${{d.weekLabel}}</td>
            <td style="color:var(--dia-color);font-weight:600;">${{formatVal(d.vDia, 'currency')}}</td>
            <td style="color:var(--noite-color);font-weight:600;">${{formatVal(d.vNoite, 'currency')}}</td>
            <td style="color:var(--vendas-color);font-weight:700;">${{formatVal(tot, 'currency')}}</td>
            <td>${{pD.toFixed(1).replace('.', ',')}}%</td>
            <td>${{pN.toFixed(1).replace('.', ',')}}%</td>
          </tr>
        `;
      }});
    }}

    // Initial Render
    renderSemanalView();
  </script>
</body>
</html>
"""

targets = [
    r'C:\Users\NTI\Documents\VENDAS\index.html',
    r'C:\Users\NTI\Documents\VENDAS\Relatorio_Vendas_Cantina.html',
    r'C:\Users\NTI\Documents\VENDAS\vendas_cantina.html',
]

for t in targets:
    with open(t, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("Updated:", t)

