import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import json

# ===== INICIALIZAR COM DADOS VAZIOS =====
# O dashboard não carregará dados do Excel inicial
# Os dados virão APENAS do upload de arquivo pelo usuário

contas_valores_mes = {}
meses_contas_clean = []
totais_clean = []
total_contas = 0
total_entrada = 0
total_saida = 0
saldo_total = 0
media_contas = 0
maior_conta = 0
menor_conta = 0

meses_ganho = []
entrada_ganho = []
saida_ganho = []
total_ganho = []

gastos_por_local = {}
top_gastos = {}
total_gastos = 0
maior_gasto = 0

contas_json = json.dumps({})
meses_json = json.dumps([])

# Dados estruturados para ganhos e gastos (vazios inicialmente)
ganhos_por_mes = {
    'meses': [],
    'entrada': [],
    'saida': [],
    'total': []
}
ganhos_json = json.dumps(ganhos_por_mes)

gastos_mes_json = json.dumps({
    'meses': [],
    'categorias': {},
    'topGastos': {}
})

# Tabela inicial vazia
contas_tabela_html = """
                    <table class="tabla-contas">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Conta</th>
                                <th style="text-align: right;">Valor (R$)</th>
                                <th>Previsão de Término</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td colspan="4" style="text-align: center; padding: 20px; color: #999;">
                                📤 Faça upload de um arquivo Excel para carregar os dados
                            </td></tr>
                        </tbody>
                    </table>
"""

# Mensagem padrão
print("[OK] Dashboard criado sem dados. Carregue um arquivo Excel via upload!")

# Inicializar HTML dos gráficos como vazios
contas_bar_html = '<div style="text-align: center; padding: 40px; color: #999;">📤 Carregue um arquivo para ver os gráficos</div>'
contas_evolucao_html = '<div style="text-align: center; padding: 40px; color: #999;">📤 Carregue um arquivo para ver os gráficos</div>'
receita_html = '<div style="text-align: center; padding: 40px; color: #999;">📤 Carregue um arquivo para ver os gráficos</div>'
ganho_total_html = '<div style="text-align: center; padding: 40px; color: #999;">📤 Carregue um arquivo para ver os gráficos</div>'
gastos_bar_html = '<div style="text-align: center; padding: 40px; color: #999;">📤 Carregue um arquivo para ver os gráficos</div>'
gastos_pie_html = '<div style="text-align: center; padding: 40px; color: #999;">📤 Carregue um arquivo para ver os gráficos</div>'

# Variáveis JSON já inicializadas acima como vazias

# ============ CRIAR HTML ============
html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Financeiro Pessoal</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #eef2f5 100%);
            min-height: 100vh;
            padding: 20px;
            padding-top: 80px;
            padding-bottom: 70px;
            display: flex;
            overflow-x: hidden;
        }}
        
        .sidebar {{
            width: 260px;
            background: linear-gradient(180deg, #0052a3 0%, #003d7a 100%);
            color: white;
            position: fixed;
            left: 20px;
            top: 80px;
            height: calc(100vh - 160px);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            transition: all 0.3s ease;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            z-index: 1000;
        }}
        
        .sidebar.collapsed {{
            width: 80px;
        }}
        
        .sidebar-toggle {{
            align-self: flex-end;
            background: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 15px;
            color: #0052a3;
            font-weight: bold;
            font-size: 1.2em;
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }}
        
        .sidebar-toggle:hover {{
            transform: scale(1.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        
        .sidebar-header {{
            padding: 20px 15px;
            font-size: 1.3em;
            font-weight: bold;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .sidebar.collapsed .sidebar-header {{
            display: none;
        }}
        
        .sidebar-menu {{
            flex: 1;
            padding: 20px 0;
            overflow-y: auto;
        }}
        
        .menu-item {{
            padding: 15px 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
            display: flex;
            align-items: center;
            gap: 15px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .menu-item:hover {{
            background: rgba(255, 255, 255, 0.2);
            border-left-color: white;
        }}
        
        .menu-item.active {{
            background: rgba(255, 255, 255, 0.3);
            border-left-color: #64b5f6;
            font-weight: 600;
        }}
        
        .menu-icon {{
            width: 24px;
            min-width: 24px;
            text-align: center;
            font-size: 1.3em;
        }}
        
        .menu-label {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .sidebar.collapsed .menu-label {{
            display: none;
        }}
        
        .container {{
            width: calc(100vw - 340px);
            margin: 0;
            margin-left: 300px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            transition: margin-left 0.3s ease, width 0.3s ease;
        }}
        
        body.sidebar-collapsed .container {{
            margin-left: 120px;
            width: calc(100vw - 160px);
        }}
        
        header {{
            background: linear-gradient(135deg, #0052a3 0%, #003d7a 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: white;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
            overflow-x: auto;
        }}
        
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            border-bottom: 2px solid #eee;
            flex-wrap: wrap;
        }}
        
        .tab-button {{
            padding: 12px 24px;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 1.1em;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
            font-weight: 500;
        }}
        
        .tab-button.active {{
            color: #0052a3;
            border-bottom-color: #0052a3;
            font-weight: 600;
        }}
        
        .tab-button:hover {{
            color: #0052a3;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
            animation: fadeIn 0.3s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        @media (max-width: 1600px) {{
            .metrics-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #e8f0ff 0%, #f0f4ff 100%);
            color: #1f2937;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 12px rgba(0, 82, 163, 0.12);
            border-left: 4px solid #0052a3;
        }}
        
        .metric-card h3 {{
            font-size: 0.9em;
            opacity: 0.85;
            margin-bottom: 10px;
            text-transform: uppercase;
            color: #0052a3;
            font-weight: 600;
        }}
        
        .metric-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #0052a3;
        }}
        
        .chart-container {{
            background: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid #eee;
        }}
        
        .chart-container-fullwidth {{
            background: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid #eee;
            width: 100%;
            overflow-x: visible;
            min-width: 0;
        }}
        
        .chart-row {{
            display: flex;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            width: 100%;
        }}
        
        .table-scroll-container {{
            max-height: 600px;
            overflow-y: auto;
            border: 1px solid #eee;
            border-radius: 10px;
            margin-top: 20px;
        }}
        
        .tabla-contas {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 0;
            font-size: 0.95em;
        }}
        
        .tabla-contas th {{
            background: #0052a3;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .tabla-contas td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        .tabla-contas tr:hover {{
            background: #e8f0ff;
        }}
        
        footer {{
            background: #f9f9f9;
            padding: 20px;
            text-align: center;
            color: #888;
            border-top: 1px solid #eee;
        }}
        
        .info-box {{
            background: #e8f0ff;
            border-left: 4px solid #0052a3;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        
        .info-box p {{
            margin: 5px 0;
            color: #0052a3;
        }}
        
        .dark-mode {{
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%) !important;
            color: #e0e0e0;
        }}
        
        .dark-mode .container {{
            background: #2d2d2d !important;
            color: #e0e0e0;
        }}
        
        .dark-mode .content {{
            color: #e0e0e0;
        }}
        
        .dark-mode .tab-button {{
            color: #aaa;
        }}
        
        .dark-mode .tab-button.active {{
            color: #93c5fd;
            border-bottom-color: #93c5fd;
        }}
        
        .dark-mode .tab-button:hover {{
            color: #93c5fd;
        }}
        
        .dark-mode .info-box {{
            background: #1e3a8a;
            border-left-color: #93c5fd;
            color: #dbeafe;
        }}
        
        .dark-mode .info-box p {{
            color: #93c5fd;
        }}
        
        .dark-mode .tabla-contas th {{
            background: #0052a3;
            color: white;
        }}
        
        .dark-mode .tabla-contas tr:hover {{
            background: #3d3d3d;
        }}
        
        .dark-mode .table-scroll-container {{
            border-color: #555;
        }}
        
        .dark-mode .tabla-contas td {{
            color: #e0e0e0;
            border-bottom-color: #444;
        }}
        
        .dark-mode .tabs {{
            border-bottom-color: #444;
        }}
        
        .dark-mode footer {{
            background: #1e1e1e;
            color: #aaa;
            border-top-color: #444;
        }}
        
        #darkModeBtn {{
            position: absolute;
            right: 40px;
            top: 30px;
            background: white;
            border: 2px solid #0052a3;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            color: #0052a3;
            transition: all 0.3s;
        }}
        
        #darkModeBtn:hover {{
            background: #0052a3;
            color: white;
            transform: scale(1.05);
        }}
        
        .dark-mode #darkModeBtn {{
            background: #1e40af;
            color: white;
            border-color: #93c5fd;
        }}
        
        .dark-mode #darkModeBtn:hover {{
            background: #1e3a8a;
            border-color: #dbeafe;
        }}
        
        header {{
            position: relative;
        }}
        
        .filters {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .filter-group label {{
            font-weight: 600;
            font-size: 0.95em;
            color: #333;
        }}
        
        .dark-mode .filter-group label {{
            color: #b0bec5;
        }}
        
        .filter-group input,
        .filter-group select {{
            padding: 10px 12px;
            border: 2px solid #d1d5db;
            border-radius: 8px;
            font-size: 0.95em;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: border-color 0.3s, box-shadow 0.3s;
        }}
        
        .dark-mode .filter-group input,
        .dark-mode .filter-group select {{
            background: #3d3d3d;
            color: #e0e0e0;
            border-color: #555;
        }}
        
        .filter-group input:focus,
        .filter-group select:focus {{
            outline: none;
            border-color: #0052a3;
            box-shadow: 0 0 0 3px rgba(0, 82, 163, 0.1);
        }}
        
        .dark-mode .filter-group input:focus,
        .dark-mode .filter-group select:focus {{
            border-color: #64b5f6;
        }}
        
        /* Dark Mode Sidebar */
        .dark-mode .sidebar {{
            background: linear-gradient(180deg, #0f172a 0%, #1a202c 100%);
        }}
        
        .dark-mode .sidebar-toggle {{
            background: #1e40af;
            color: #93c5fd;
        }}
        
        .dark-mode .sidebar-toggle:hover {{
            background: #1e3a8a;
            color: #bfdbfe;
        }}
        
        .dark-mode .sidebar-header {{
            border-bottom-color: rgba(147, 197, 253, 0.2);
            color: #93c5fd;
        }}
        
        .dark-mode .menu-item {{
            color: #e0e7ff;
        }}
        
        .dark-mode .menu-item:hover {{
            background: rgba(93, 147, 253, 0.2);
            border-left-color: #93c5fd;
        }}
        
        .dark-mode .menu-item.active {{
            background: rgba(93, 147, 253, 0.3);
            border-left-color: #60a5fa;
        }}
        
        /* Top Header Fixo */
        .top-header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: linear-gradient(135deg, #0052a3 0%, #003d7a 100%);
            color: white;
            display: flex;
            align-items: center;
            padding: 0 40px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            z-index: 999;
            font-size: 1.2em;
            font-weight: 500;
        }}
        
        .dark-mode .top-header {{
            background: linear-gradient(135deg, #0f172a 0%, #1a202c 100%);
        }}
        
        /* Bottom Footer Fixo */
        .bottom-footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 50px;
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            color: #6b7280;
            display: flex;
            align-items: center;
            padding: 0 40px;
            box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
            z-index: 999;
            font-size: 0.9em;
            border-top: 1px solid #d1d5db;
        }}
        
        .dark-mode .bottom-footer {{
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            color: #aaa;
            border-top-color: #444;
        }}
        
        /* Upload Button */
        .upload-section {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-left: auto;
        }}
        
        .upload-btn {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid white;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 500;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .upload-btn:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }}
        
        #fileInput {{
            display: none;
        }}
        
        .upload-status {{
            color: white;
            font-size: 0.85em;
            margin-right: 10px;
            min-width: 150px;
        }}
    </style>
</head>
<body>
    <!-- TOP HEADER FIXO -->
    <div class="top-header">
        📊 Dashboard Financeiro Pessoal | Dados: CONTROLE_FINANCEIRO_ATUALIZADO.xlsx
        <div class="upload-section">
            <div class="upload-status" id="uploadStatus"></div>
            <button class="upload-btn" onclick="document.getElementById('fileInput').click()" title="Upload do arquivo Excel">
                📤 Upload Excel
            </button>
            <input type="file" id="fileInput" accept=".xlsx,.xls" onchange="handleFileUpload(event)">
        </div>
    </div>
    
    <!-- MENU LATERAL -->
    <div class="sidebar" id="sidebar">
        <button class="sidebar-toggle" onclick="toggleSidebar()" title="Recolher/Expandir menu">
            <span id="toggleIcon">◄</span>
        </button>
        <div class="sidebar-header">📊 Menu</div>
        <div class="sidebar-menu">
            <div class="menu-item active" onclick="switchTab('overview'); setActiveMenu(this)">
                <div class="menu-icon">📈</div>
                <div class="menu-label">Visão Geral</div>
            </div>
            <div class="menu-item" onclick="switchTab('contas'); setActiveMenu(this)">
                <div class="menu-icon">💼</div>
                <div class="menu-label">Contas</div>
            </div>
            <div class="menu-item" onclick="switchTab('ganhos'); setActiveMenu(this)">
                <div class="menu-icon">💰</div>
                <div class="menu-label">Ganhos</div>
            </div>
            <div class="menu-item" onclick="switchTab('gastos'); setActiveMenu(this)">
                <div class="menu-icon">💳</div>
                <div class="menu-label">Gastos</div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <header>
            <button id="darkModeBtn" onclick="toggleDarkMode()">🌙 Dark Mode</button>
            <h1>Dashboard Financeiro Pessoal</h1>
            <p>Análise Completa das Suas Contas e Gastos</p>
        </header>
        
        <div class="content">
            <div class="tabs">
                <button class="tab-button active" onclick="switchTab('overview')">Visao Geral</button>
                <button class="tab-button" onclick="switchTab('contas')">Contas</button>
                <button class="tab-button" onclick="switchTab('ganhos')">Ganhos</button>
                <button class="tab-button" onclick="switchTab('gastos')">Gastos</button>
            </div>
            
            <!-- TAB: VISÃO GERAL -->
            <div id="overview" class="tab-content active">
                <h2>Resumo Financeiro Completo</h2>
                <div class="info-box">
                    <p><strong>Total de Contas:</strong> R$ {total_contas:,.2f}</p>
                    <p><strong>Total de Entrada:</strong> R$ {total_entrada:,.2f}</p>
                    <p><strong>Total de Saida:</strong> R$ {total_saida:,.2f}</p>
                    <p><strong>Saldo Total:</strong> R$ {saldo_total:,.2f}</p>
                    <p><strong>Total de Gastos Registrados:</strong> R$ {total_gastos:,.2f}</p>
                    <p><strong>Atualizado em:</strong> {datetime.now().strftime('%d/%m/%Y as %H:%M')}</p>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Total de Contas</h3>
                        <div class="value">R$ {total_contas:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Media de Contas</h3>
                        <div class="value">R$ {media_contas:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Maior Conta</h3>
                        <div class="value">R$ {maior_conta:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Saldo Total</h3>
                        <div class="value">R$ {saldo_total:,.2f}</div>
                    </div>
                </div>
            </div>
            
            <!-- TAB: CONTAS -->
            <div id="contas" class="tab-content">
                <h2>Gestao de Contas</h2>
                <p style="margin-bottom: 20px; color: #666;">Analise detalhada de suas contas mensais com graficos comparativos:</p>
                
                <div class="filters">
                    <div class="filter-group">
                        <label for="contaFilter">Filtrar por Conta:</label>
                        <select id="contaFilter" onchange="filterByConta()" style="padding: 10px; font-size: 1em; border-radius: 5px; border: 1px solid #ddd;">
                            <option value="">Todas as Contas</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="mesFilter">Selecione o Mês:</label>
                        <select id="mesFilter" onchange="filterByMes()" style="padding: 10px; font-size: 1em; border-radius: 5px; border: 1px solid #ddd;">
                            <option value="">Todos os Meses</option>
                        </select>
                    </div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Total de Contas</h3>
                        <div class="value" id="totalContasFiltrado">R$ {total_contas:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Media de Contas</h3>
                        <div class="value" id="mediaContasFiltrado">R$ {media_contas:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Maior Gasto em Contas</h3>
                        <div class="value" id="maiorContaFiltrado">R$ {maior_conta:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Menor Gasto em Contas</h3>
                        <div class="value" id="menorContaFiltrado">R$ {menor_conta:,.2f}</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h3>Maiores Contas</h3>
                    <div id="chartMaioresContas" style="height: 650px; width: 100%; min-width: 800px;"></div>
                </div>
                
                <div class="chart-container">
                    <h3>Evolucao Total de Contas por Mes</h3>
                    <div id="chartEvolucaoContas" style="height: 600px; width: 100%; min-width: 800px;"></div>
                </div>
                
                <div style="margin-top: 40px;">
                    <h3>Lista de Contas</h3>
                    <div class="table-scroll-container">
                        {contas_tabela_html}
                    </div>
                </div>
            </div>
            
            <!-- TAB: GANHOS -->
            <div id="ganhos" class="tab-content">
                <h2>Analise de Ganhos e Receitas</h2>
                <p style="margin-bottom: 20px; color: #666;">Comparacao entre entrada e saida de recursos:</p>
                
                <div class="filters">
                    <div class="filter-group">
                        <label for="mesFilterGanhos">Filtrar por Mês:</label>
                        <select id="mesFilterGanhos" onchange="filterGanhos()" style="padding: 10px; font-size: 1em; border-radius: 5px; border: 1px solid #ddd;">
                            <option value="">Todos os Meses</option>
                        </select>
                    </div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Total de Entrada</h3>
                        <div class="value" id="totalEntrada">R$ {total_entrada:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Total de Saida</h3>
                        <div class="value" id="totalSaida">R$ {total_saida:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Saldo Total</h3>
                        <div class="value" id="saldoFiltrado">R$ {saldo_total:,.2f}</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h3>Receita vs Despesa por Mes</h3>
                    <div id="chartReceita" style="height: 650px; width: 100%; min-width: 800px;"></div>
                </div>
                
                <div class="chart-container">
                    <h3>Saldo Mensal (Entrada - Saida)</h3>
                    <div id="chartSaldo" style="height: 600px; width: 100%; min-width: 800px;"></div>
                </div>
            </div>
            
            <!-- TAB: GASTOS -->
            <div id="gastos" class="tab-content">
                <h2>Analise de Gastos Detalhados</h2>
                <p style="margin-bottom: 20px; color: #666;">Maiores gastos por categorias:</p>
                
                <div class="filters">
                    <div class="filter-group">
                        <label for="mesFilterGastos">Filtrar por Mês:</label>
                        <select id="mesFilterGastos" onchange="filterGastos()" style="padding: 10px; font-size: 1em; border-radius: 5px; border: 1px solid #ddd;">
                            <option value="">Todos os Meses</option>
                        </select>
                    </div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Total de Gastos</h3>
                        <div class="value" id="totalGastosFiltrado">R$ {total_gastos:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Maior Gasto</h3>
                        <div class="value" id="maiorGastoFiltrado">R$ {maior_gasto:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Categorias</h3>
                        <div class="value" id="qtdCategoriasFiltrada">{len(top_gastos)}</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h3>Top 10 Maiores Gastos</h3>
                    <div id="chartGastos" style="height: 600px; width: 100%; min-width: 800px;"></div>
                </div>
                
                <div class="chart-container">
                    <h3>Distribuicao dos Gastos</h3>
                    <div id="chartGastosPie" style="height: 600px; width: 100%; min-width: 800px;"></div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- BOTTOM FOOTER FIXO -->
    <div class="bottom-footer">
        Atualizado em {datetime.now().strftime('%d de %B de %Y as %H:%M')}
    </div>
    
    <script>
        // Dados de contas por mês (para filtro dinâmico)
        const contasData = {contas_json};
        const mesesContas = {meses_json};
        
        // Dados de ganhos e gastos
        const ganhosData = {ganhos_json};
        const gastosData = {gastos_mes_json};
        
        // Preencher dropdown de contas
        window.addEventListener('load', function() {{
            const select = document.getElementById('contaFilter');
            if (select) {{
                for (let conta of Object.keys(contasData).sort()) {{
                    const option = document.createElement('option');
                    option.value = conta;
                    option.textContent = conta;
                    select.appendChild(option);
                }}
            }}
            
            // Preencher dropdown de meses para Contas aba
            const selectMes = document.getElementById('mesFilter');
            if (selectMes) {{
                for (let mes of mesesContas) {{
                    const option = document.createElement('option');
                    option.value = mes;
                    option.textContent = mes;
                    selectMes.appendChild(option);
                }}
            }}
            
            // Preencher dropdown de meses para Ganhos
            const selectGanhos = document.getElementById('mesFilterGanhos');
            if (selectGanhos) {{
                for (let mes of ganhosData.meses) {{
                    const option = document.createElement('option');
                    option.value = mes;
                    option.textContent = mes;
                    selectGanhos.appendChild(option);
                }}
            }}
            
            // Preencher dropdown de meses para Gastos
            const selectGastos = document.getElementById('mesFilterGastos');
            if (selectGastos) {{
                for (let mes of Object.keys(gastosData).sort()) {{
                    const option = document.createElement('option');
                    option.value = mes;
                    option.textContent = mes;
                    selectGastos.appendChild(option);
                }}
            }}
            
            // Renderizar gráficos iniciais da aba Contas
            renderGraficosContas();
        }});
        
        // Função para filtrar por conta e atualizar gráficos
        function filterByConta() {{
            const contaSelect = document.getElementById('contaFilter');
            const contaSelecionada = contaSelect.value;
            
            // Filtrar tabela
            const filterTable = () => {{
                const filter = contaSelecionada.toUpperCase();
                const table = document.querySelector('.tabla-contas');
                if (!table) return;
                const rows = table.getElementsByTagName('tr');
                
                for (let i = 1; i < rows.length; i++) {{
                    const cells = rows[i].getElementsByTagName('td');
                    if (cells.length > 1) {{
                        const contaName = cells[1].textContent;
                        if (filter === '' || contaName.toUpperCase().indexOf(filter) > -1) {{
                            rows[i].style.display = '';
                        }} else {{
                            rows[i].style.display = 'none';
                        }}
                    }}
                }}
            }};
            filterTable();
            
            // Atualizar gráficos e métricas
            renderGraficosContas();
        }}
        
        // Função para renderizar gráficos da aba Contas
        function renderGraficosContas() {{
            const mesSelecionado = document.getElementById('mesFilter').value;
            const contaSelecionada = document.getElementById('contaFilter').value;
            let indicesMes = [];
            
            if (mesSelecionado === '') {{
                // Todos os meses
                indicesMes = Array.from({{length: mesesContas.length}}, (_, i) => i);
            }} else {{
                // Apenas o mês selecionado (não somar anteriores)
                const idx = mesesContas.indexOf(mesSelecionado);
                if (idx !== -1) {{
                    indicesMes = [idx];
                }}
            }}
            
            // Gráfico: Maiores Contas
            let contasValores = {{}};
            
            if (contaSelecionada === '') {{
                // Top 10 contas
                for (let conta in contasData) {{
                    if (mesSelecionado === '') {{
                        contasValores[conta] = contasData[conta][3] || 0;
                    }} else {{
                        const idx = mesesContas.indexOf(mesSelecionado);
                        contasValores[conta] = contasData[conta][idx] || 0;
                    }}
                }}
            }} else {{
                // Apenas a conta selecionada
                const dados = contasData[contaSelecionada];
                if (dados) {{
                    if (mesSelecionado === '') {{
                        contasValores[contaSelecionada] = dados[3] || 0;
                    }} else {{
                        const idx = mesesContas.indexOf(mesSelecionado);
                        contasValores[contaSelecionada] = dados[idx] || 0;
                    }}
                }}
            }}
            
            let contasOrd = Object.entries(contasValores)
                .sort((a, b) => b[1] - a[1])
                .slice(0, contaSelecionada === '' ? 10 : 1);
            
            let nomes = contasOrd.map(item => item[0]);
            let valores = contasOrd.map(item => item[1]);
            
            // Calcular thickness baseado na quantidade de contas
            let markerThickness = nomes.length <= 2 ? 15 : (nomes.length <= 5 ? 25 : 35);
            
            const traceContas = {{
                y: nomes,
                x: valores,
                orientation: 'h',
                type: 'bar',
                marker: {{
                    color: valores,
                    colorscale: 'Blues',
                    thickness: markerThickness
                }},
                text: valores.map(v => 'R$ ' + v.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})),
                textposition: 'outside',
                textfont: {{size: 12, family: 'Segoe UI'}}
            }};
            const layoutContas = {{
                height: 650,
                width: document.getElementById('chartMaioresContas').offsetWidth,
                font: {{family: 'Segoe UI', size: 12, color: '#333333'}},
                xaxis: {{showticklabels: false}},
                yaxis: {{showticklabels: true}},
                margin: {{l: 150, r: 50, t: 30, b: 30}},
                showlegend: false
            }};
            Plotly.newPlot('chartMaioresContas', [traceContas], layoutContas, {{displayModeBar: false}});
            
            // Gráfico: Evolução de Contas
            let mesesEvolucao = [];
            let totaisEvolucao = [];
            
            if (contaSelecionada === '') {{
                // Evolução total de todas as contas
                for (let i of indicesMes) {{
                    mesesEvolucao.push(mesesContas[i]);
                    let total = 0;
                    for (let conta in contasData) {{
                        total += contasData[conta][i] || 0;
                    }}
                    totaisEvolucao.push(total);
                }}
            }} else {{
                // Evolução apenas da conta selecionada
                const dados = contasData[contaSelecionada];
                if (dados) {{
                    for (let i of indicesMes) {{
                        mesesEvolucao.push(mesesContas[i]);
                        totaisEvolucao.push(dados[i] || 0);
                    }}
                }}
            }}
            
            const traceEvolucao = {{
                x: mesesEvolucao,
                y: totaisEvolucao,
                mode: 'lines+markers+text',
                line: {{color: '#1f77b4', width: 3}},
                text: totaisEvolucao.map(v => 'R$ ' + v.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})),
                textposition: 'top center',
                textfont: {{size: 12, family: 'Segoe UI'}},
                hovertemplate: '<b>%{{x}}</b><br>R$ %{{y:,.2f}}<extra></extra>'
            }};
            const layoutEvolucao = {{
                height: 600,
                width: document.getElementById('chartEvolucaoContas').offsetWidth,
                font: {{family: 'Segoe UI', size: 12, color: '#333333'}},
                xaxis: {{showticklabels: true}},
                yaxis: {{showticklabels: false}},
                margin: {{l: 50, r: 50, t: 30, b: 30}},
                showlegend: false
            }};
            Plotly.newPlot('chartEvolucaoContas', [traceEvolucao], layoutEvolucao, {{displayModeBar: false}});
            
            // Atualizar métricas
            if (contaSelecionada === '') {{
                // Métricas de todas as contas
                let totalMes = totaisEvolucao.reduce((a, b) => a + b, 0);
                let valoresAgora = Object.values(contasValores);
                let mediaMes = valoresAgora.length > 0 ? valoresAgora.reduce((a, b) => a + b, 0) / valoresAgora.length : 0;
                let maiorMes = Math.max(...valoresAgora);
                let menorMes = Math.min(...valoresAgora);
                
                document.getElementById('totalContasFiltrado').textContent = 'R$ ' + totalMes.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
                document.getElementById('mediaContasFiltrado').textContent = 'R$ ' + mediaMes.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
                document.getElementById('maiorContaFiltrado').textContent = 'R$ ' + maiorMes.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
                document.getElementById('menorContaFiltrado').textContent = 'R$ ' + menorMes.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
            }} else {{
                // Métricas apenas da conta selecionada
                let totalConta = totaisEvolucao.reduce((a, b) => a + b, 0);
                let mediaConta = totaisEvolucao.length > 0 ? totalConta / totaisEvolucao.length : 0;
                let maiorConta = Math.max(...(totaisEvolucao.length > 0 ? totaisEvolucao : [0]));
                let menorConta = Math.min(...(totaisEvolucao.length > 0 ? totaisEvolucao : [0]));
                
                document.getElementById('totalContasFiltrado').textContent = 'R$ ' + totalConta.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
                document.getElementById('mediaContasFiltrado').textContent = 'R$ ' + mediaConta.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
                document.getElementById('maiorContaFiltrado').textContent = 'R$ ' + maiorConta.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
                document.getElementById('menorContaFiltrado').textContent = 'R$ ' + menorConta.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
            }}
        }}
        
        // Função para filtrar por mês na aba Contas
        function filterByMes() {{
            renderGraficosContas();
        }}
        function filterGanhos() {{
            const mesSelecionado = document.getElementById('mesFilterGanhos').value;
            let entradaFiltrada = 0, saidaFiltrada = 0, saldoFiltrado = 0;
            let mesesFiltrados = [], entradaFiltrada_list = [], saidaFiltrada_list = [], saldoFiltrado_list = [];
            
            if (mesSelecionado === '') {{
                // Mostrar todos
                mesesFiltrados = ganhosData.meses;
                entradaFiltrada_list = ganhosData.entrada;
                saidaFiltrada_list = ganhosData.saida;
                saldoFiltrado_list = ganhosData.total;
                entradaFiltrada = entradaFiltrada_list.reduce((a, b) => a + b, 0);
                saidaFiltrada = saidaFiltrada_list.reduce((a, b) => a + b, 0);
                saldoFiltrado = saldoFiltrado_list.reduce((a, b) => a + b, 0);
            }} else {{
                // Mostrar apenas o mês selecionado
                const idx = ganhosData.meses.indexOf(mesSelecionado);
                if (idx !== -1) {{
                    mesesFiltrados = [mesSelecionado];
                    entradaFiltrada_list = [ganhosData.entrada[idx]];
                    saidaFiltrada_list = [ganhosData.saida[idx]];
                    saldoFiltrado_list = [ganhosData.total[idx]];
                    entradaFiltrada = entradaFiltrada_list[0];
                    saidaFiltrada = saidaFiltrada_list[0];
                    saldoFiltrado = saldoFiltrado_list[0];
                }}
            }}
            
            // Atualizar números
            document.getElementById('totalEntrada').textContent = 'R$ ' + entradaFiltrada.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
            document.getElementById('totalSaida').textContent = 'R$ ' + saidaFiltrada.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
            document.getElementById('saldoFiltrado').textContent = 'R$ ' + saldoFiltrado.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
            
            // Recriar gráfico Receita vs Despesa
            const traceEntrada = {{
                name: 'Entrada',
                x: mesesFiltrados,
                y: entradaFiltrada_list,
                type: 'bar',
                marker: {{
                    color: '#0052a3'
                }},
                text: entradaFiltrada_list.map(v => 'R$ ' + v.toLocaleString('pt-BR', {{maximumFractionDigits: 0}})),
                textposition: 'outside',
                textfont: {{size: 14, family: 'Segoe UI'}}
            }};
            const traceSaida = {{
                name: 'Saida',
                x: mesesFiltrados,
                y: saidaFiltrada_list,
                type: 'bar',
                marker: {{
                    color: '#ff9500'
                }},
                text: saidaFiltrada_list.map(v => 'R$ ' + v.toLocaleString('pt-BR', {{maximumFractionDigits: 0}})),
                textposition: 'outside',
                textfont: {{size: 14, family: 'Segoe UI'}}
            }};
            // Calcular bargap baseado na quantidade de meses
            let bargapReceita = mesesFiltrados.length <= 2 ? 0.7 : (mesesFiltrados.length <= 4 ? 0.5 : 0.3);
            const layout = {{
                barmode: 'group',
                height: 650,
                width: document.getElementById('chartReceita').offsetWidth,
                font: {{family: 'Segoe UI', size: 12, color: '#333333'}},
                xaxis: {{showticklabels: true}},
                yaxis: {{showticklabels: false}},
                margin: {{l: 50, r: 50, t: 50, b: 30}},
                showlegend: true,
                bargap: bargapReceita
            }};
            Plotly.newPlot('chartReceita', [traceEntrada, traceSaida], layout, {{displayModeBar: false}});
            
            // Recriar gráfico de saldo
            const traceSaldo = {{
                x: mesesFiltrados,
                y: saldoFiltrado_list,
                mode: 'lines+markers+text',
                line: {{color: '#2ca02c', width: 3}},
                text: saldoFiltrado_list.map(v => 'R$ ' + v.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})),
                textposition: 'top center',
                textfont: {{size: 12, family: 'Segoe UI'}},
                hovertemplate: '<b>%{{x}}</b><br>R$ %{{y:,.2f}}<extra></extra>'
            }};
            const layoutSaldo = {{
                height: 600,
                width: document.getElementById('chartSaldo').offsetWidth,
                font: {{family: 'Segoe UI', size: 12, color: '#333333'}},
                xaxis: {{showticklabels: true}},
                yaxis: {{showticklabels: false}},
                margin: {{l: 50, r: 50, t: 30, b: 30}},
                showlegend: false
            }};
            Plotly.newPlot('chartSaldo', [traceSaldo], layoutSaldo, {{displayModeBar: false}});
        }}
        
        // Função para filtrar gastos por mês
        function filterGastos() {{
            const mesSelecionado = document.getElementById('mesFilterGastos').value;
            let gastosAgrupado = {{}};
            
            if (mesSelecionado === '') {{
                // Somar todos os meses
                for (let mes in gastosData) {{
                    for (let gasto of gastosData[mes]) {{
                        if (!gastosAgrupado[gasto.local]) {{
                            gastosAgrupado[gasto.local] = 0;
                        }}
                        gastosAgrupado[gasto.local] += gasto.valor;
                    }}
                }}
            }} else {{
                // Apenas o mês selecionado
                if (gastosData[mesSelecionado]) {{
                    for (let gasto of gastosData[mesSelecionado]) {{
                        if (!gastosAgrupado[gasto.local]) {{
                            gastosAgrupado[gasto.local] = 0;
                        }}
                        gastosAgrupado[gasto.local] += gasto.valor;
                    }}
                }}
            }}
            
            // Ordenar top 10
            let gastosOrdenados = Object.entries(gastosAgrupado)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            
            let totalGastos = Object.values(gastosAgrupado).reduce((a, b) => a + b, 0);
            let maiorGasto = gastosOrdenados.length > 0 ? gastosOrdenados[0][1] : 0;
            
            // Atualizar métricas
            document.getElementById('totalGastosFiltrado').textContent = 'R$ ' + totalGastos.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
            document.getElementById('maiorGastoFiltrado').textContent = 'R$ ' + maiorGasto.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
            document.getElementById('qtdCategoriasFiltrada').textContent = Object.keys(gastosAgrupado).length;
            
            // Gráfico de barras
            let nomes = gastosOrdenados.map(item => item[0]);
            let valores = gastosOrdenados.map(item => item[1]);
            
            // Calcular thickness baseado na quantidade de categorias
            let markerThicknessGastos = nomes.length <= 2 ? 15 : (nomes.length <= 5 ? 25 : 35);
            
            const traceBar = {{
                y: nomes,
                x: valores,
                orientation: 'h',
                type: 'bar',
                marker: {{
                    color: valores,
                    colorscale: 'Reds',
                    thickness: markerThicknessGastos
                }},
                text: valores.map(v => 'R$ ' + v.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})),
                textposition: 'outside',
                textfont: {{size: 12, family: 'Segoe UI'}}
            }};
            const layoutBar = {{
                height: 600,
                width: document.getElementById('chartGastos').offsetWidth,
                font: {{family: 'Segoe UI', size: 12, color: '#333333'}},
                xaxis: {{showticklabels: false}},
                yaxis: {{showticklabels: true}},
                margin: {{l: 150, r: 50, t: 30, b: 30}},
                showlegend: false
            }};
            Plotly.newPlot('chartGastos', [traceBar], layoutBar, {{displayModeBar: false}});
            
            // Gráfico de pizza
            const tracePie = {{
                labels: nomes,
                values: valores,
                type: 'pie',
                text: valores.map(v => 'R$ ' + v.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})),
                textposition: 'inside',
                textfont: {{size: 11, family: 'Segoe UI'}}
            }};
            const layoutPie = {{
                height: 600,
                width: document.getElementById('chartGastosPie').offsetWidth,
                font: {{family: 'Segoe UI', size: 12, color: '#333333'}},
                margin: {{l: 20, r: 20, t: 20, b: 20}},
                showlegend: false
            }};
            Plotly.newPlot('chartGastosPie', [tracePie], layoutPie, {{displayModeBar: false}});
        }}
        
        // Função para alternar Dark Mode
        function toggleSidebar() {{
            const body = document.body;
            const sidebar = document.getElementById('sidebar');
            const toggleIcon = document.getElementById('toggleIcon');
            
            body.classList.toggle('sidebar-collapsed');
            sidebar.classList.toggle('collapsed');
            
            // Alternar ícone
            if (body.classList.contains('sidebar-collapsed')) {{
                toggleIcon.textContent = '►';
            }} else {{
                toggleIcon.textContent = '◄';
            }}
        }}
        
        function setActiveMenu(element) {{
            const items = document.querySelectorAll('.menu-item');
            items.forEach(item => item.classList.remove('active'));
            element.classList.add('active');
        }}
        
        function toggleDarkMode() {{
            const body = document.body;
            body.classList.toggle('dark-mode');
            // Salvar preferência
            localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
            // Atualizar texto do botão
            const btn = document.getElementById('darkModeBtn');
            if (body.classList.contains('dark-mode')) {{
                btn.textContent = '☀️ Light Mode';
            }} else {{
                btn.textContent = '🌙 Dark Mode';
            }}
        }}
        
        // Verificar preferência ao carregar
        window.addEventListener('load', function() {{
            if (localStorage.getItem('darkMode') === 'true') {{
                document.body.classList.add('dark-mode');
                document.getElementById('darkModeBtn').textContent = '☀️ Light Mode';
            }}
            
            // Verificar se servidor está rodando
            verificarServidorUpload();
        }});
        
        // Verificar se servidor Flask está rodando
        function verificarServidorUpload() {{
            fetch('http://localhost:5000/saude', {{
                method: 'GET'
            }})
            .then(response => response.json())
            .then(data => {{
                console.log('✅ Servidor está rodando!', data);
                exibirStatusServidor(true);
            }})
            .catch(error => {{
                console.warn('⚠️ Servidor não está acessível');
                exibirStatusServidor(false);
            }});
        }}
        
        // Exibir/ocultar alerta de servidor
        function exibirStatusServidor(ativo) {{
            const uploadBtn = document.querySelector('.upload-btn');
            const uploadStatus = document.getElementById('uploadStatus');
            
            if (!ativo) {{
                uploadStatus.innerHTML = '⚠️ <b>Servidor não está rodando!</b><br><small>Execute: python servidor_upload.py</small>';
                uploadStatus.style.color = '#ef4444';
                uploadStatus.style.display = 'block';
                uploadStatus.style.fontSize = '0.8em';
                uploadStatus.style.minWidth = '300px';
                uploadBtn.style.opacity = '0.5';
                uploadBtn.style.cursor = 'not-allowed';
                uploadBtn.style.pointerEvents = 'none';
            }} else {{
                uploadStatus.textContent = '';
                uploadStatus.style.display = 'none';
                uploadBtn.style.opacity = '1';
                uploadBtn.style.cursor = 'pointer';
                uploadBtn.style.pointerEvents = 'auto';
            }}
        }}
        
        // Retentar servidor a cada 10 segundos se estiver inativo
        setInterval(() => {{
            verificarServidorUpload();
        }}, 10000);
        
        // Função para alternar entre abas
        function switchTab(tabName) {{
            const contents = document.querySelectorAll('.tab-content');
            const buttons = document.querySelectorAll('.tab-button');
            
            contents.forEach(content => content.classList.remove('active'));
            buttons.forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}
        
        // Função para filtrar tabela por nome da conta
        function filterTable() {{
            const input = document.getElementById('contaFilter');
            const filter = input.value.toUpperCase();
            const table = document.querySelector('.tabla-contas');
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {{
                const cells = rows[i].getElementsByTagName('td');
                if (cells.length > 1) {{
                    const contaName = cells[1].textContent;
                    if (contaName.toUpperCase().indexOf(filter) > -1) {{
                        rows[i].style.display = '';
                    }} else {{
                        rows[i].style.display = 'none';
                    }}
                }}
            }}
        }}
        
        // Função para filtrar tabela por mês de término
        function filterTableByMonth() {{
            const select = document.getElementById('mesFilter');
            const filter = select.value.toUpperCase();
            const table = document.querySelector('.tabla-contas');
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {{
                const cells = rows[i].getElementsByTagName('td');
                if (cells.length > 3) {{
                    const mesStr = cells[3].textContent.toUpperCase();
                    if (filter === '' || mesStr.indexOf(filter) > -1) {{
                        rows[i].style.display = '';
                    }} else {{
                        rows[i].style.display = 'none';
                    }}
                }}
            }}
        }}
        
        // Função para fazer upload e processar Excel
        function handleFileUpload(event) {{
            const file = event.target.files[0];
            if (!file) return;
            
            console.log('📂 Arquivo selecionado:', file.name);
            processarExcel(file);
            
            event.target.value = '';
        }}
        
        // Função para processar Excel via servidor
        function processarExcel(file) {{
            const statusDiv = document.getElementById('uploadStatus');
            statusDiv.textContent = '📤 Enviando arquivo...';
            statusDiv.style.color = '#fbbf24';
            
            console.log('📂 Arquivo selecionado:', file.name);
            
            // Criar FormData
            const formData = new FormData();
            formData.append('arquivo', file);
            
            // Enviar para servidor
            console.log('🌐 Enviando para servidor em localhost:5000...');
            fetch('http://localhost:5000/processar-excel', {{
                method: 'POST',
                body: formData
            }})
            .then(response => {{
                if (!response.ok) {{
                    return response.json().then(err => {{
                        throw new Error(err.erro || 'Erro no servidor');
                    }});
                }}
                return response.json();
            }})
            .then(dados => {{
                if (!dados.sucesso) {{
                    throw new Error(dados.erro || 'Erro ao processar');
                }}
                
                console.log('✅ Dados recebidos do servidor');
                console.log('💼 Contas:', Object.keys(dados.contasData).length);
                console.log('📅 Meses:', dados.mesesContas.length);
                console.log('💰 Ganhos:', Object.keys(dados.ganhosData).length);
                console.log('💳 Gastos:', Object.keys(dados.gastosData).length);
                
                // Atualizar variáveis globais
                window.mesesContas = dados.mesesContas;
                window.contasData = dados.contasData;
                window.ganhosData = dados.ganhosData;
                window.gastosData = dados.gastosData;
                
                // Recarregar gráficos
                console.log('🎨 Atualizando tema...');
                setupTheme();
                
                console.log('📊 Atualizando gráficos...');
                if (typeof renderGraficosContas !== 'undefined') {{
                    renderGraficosContas();
                    console.log('✅ Gráfico Contas atualizado');
                }}
                if (typeof filterGanhos !== 'undefined') {{
                    filterGanhos();
                    console.log('✅ Gráfico Ganhos atualizado');
                }}
                if (typeof filterGastos !== 'undefined') {{
                    filterGastos();
                    console.log('✅ Gráfico Gastos atualizado');
                }}
                
                statusDiv.textContent = '✅ Atualizado com sucesso!';
                statusDiv.style.color = '#10b981';
                console.log('🎉 Arquivo processado com sucesso!');
                
                setTimeout(() => {{
                    statusDiv.textContent = '';
                }}, 3000);
            }})
            .catch(error => {{
                const errorMsg = error.message || 'Erro desconhecido';
                statusDiv.textContent = '❌ ' + errorMsg;
                statusDiv.style.color = '#ef4444';
                console.error('❌ ERRO:', error);
                
                // Verificar se servidor está rodando
                if (errorMsg.includes('Failed to fetch')) {{
                    statusDiv.textContent = '❌ Servidor não está rodando em localhost:5000';
                    console.error('❌ Por favor, execute: python servidor_upload.py');
                }}
                
                setTimeout(() => {{
                    statusDiv.textContent = '';
                }}, 5000);
            }});
        }}
    </script>
</body>
</html>
"""

# Salvar HTML
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("[OK] Dashboard atualizado com valores corretos do Excel!")

