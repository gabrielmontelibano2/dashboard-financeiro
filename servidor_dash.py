#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Flask Robusto para Dashboard Financeiro
- Aceita conexões de qualquer IP
- Serve o HTML com CORS apropriado
- Processa uploads de Excel
"""

from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import pandas as pd
import json
from werkzeug.utils import secure_filename
import os
import tempfile
import traceback
import sys

app = Flask(__name__, static_folder=os.path.dirname(__file__))
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================== ROTAS ====================

@app.route('/', methods=['GET', 'OPTIONS'])
def index():
    """Servir o dashboard.html"""
    if request.method == 'OPTIONS':
        return '', 204
    
    arquivo_html = os.path.join(SCRIPT_DIR, 'dashboard.html')
    
    try:
        if os.path.exists(arquivo_html):
            with open(arquivo_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            response = app.make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            print(f"[OK] Dashboard servido para {request.remote_addr}")
            return response
        else:
            print(f"[ERRO] Arquivo não encontrado: {arquivo_html}")
            return jsonify({'erro': 'Dashboard não encontrado'}), 404
    except Exception as e:
        print(f"[ERRO] Ao servir dashboard: {str(e)}")
        return jsonify({'erro': str(e)}), 500

@app.route('/processar-excel', methods=['POST', 'OPTIONS'])
def processar_excel():
    """Processa arquivo Excel e retorna dados JSON"""
    if request.method == 'OPTIONS':
        response = app.make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 204
    
    filepath = None
    try:
        if 'arquivo' not in request.files:
            return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
        
        arquivo = request.files['arquivo']
        if arquivo.filename == '':
            return jsonify({'erro': 'Arquivo sem nome'}), 400
        
        if not arquivo.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'erro': 'Arquivo deve ser Excel (.xlsx ou .xls)'}), 400
        
        # Salvar arquivo
        filename = secure_filename(arquivo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
        arquivo.save(filepath)
        
        print(f"[OK] Arquivo recebido: {filename} de {request.remote_addr}")
        
        # Processar CONTAS
        try:
            contas_df = pd.read_excel(filepath, sheet_name="CONTAS", header=None)
        except Exception as e:
            return jsonify({'erro': f'Aba CONTAS não encontrada: {str(e)}'}), 400
        
        meses_contas = []
        if len(contas_df) > 1:
            for col_idx in range(16, min(28, len(contas_df.columns))):
                if col_idx < len(contas_df.columns):
                    m = contas_df.iloc[1, col_idx]
                    if pd.notna(m):
                        meses_contas.append(str(m).strip())
        
        contas_valores_mes = {}
        for idx in range(2, min(28, len(contas_df))):
            if len(contas_df.columns) > 0:
                nome_conta = contas_df.iloc[idx, 0]
                if pd.notna(nome_conta):
                    nome_str = str(nome_conta).strip()
                    if nome_str and nome_str != "TOTAL DE CONTAS":
                        valores = []
                        for col_idx in range(16, min(28, len(contas_df.columns))):
                            val = contas_df.iloc[idx, col_idx]
                            try:
                                valores.append(float(val) if pd.notna(val) else 0)
                            except:
                                valores.append(0)
                        if valores:
                            contas_valores_mes[nome_str] = valores
        
        # Processar GANHOS
        meses_ganho = []
        entrada_ganho = []
        saida_ganho = []
        total_ganho = []
        
        try:
            ganho_df = pd.read_excel(filepath, sheet_name="GANHO MENSAL", header=None)
            if len(ganho_df) > 19:
                for idx in range(19, min(29, len(ganho_df))):
                    if len(ganho_df.columns) > 4:
                        mes = ganho_df.iloc[idx, 1]
                        entrada = ganho_df.iloc[idx, 2]
                        saida = ganho_df.iloc[idx, 3]
                        total_g = ganho_df.iloc[idx, 4]
                        
                        if pd.notna(mes) and str(mes).strip() != '':
                            meses_ganho.append(str(mes).strip())
                            entrada_ganho.append(float(entrada) if pd.notna(entrada) else 0)
                            saida_ganho.append(float(saida) if pd.notna(saida) else 0)
                            total_ganho.append(float(total_g) if pd.notna(total_g) else 0)
        except:
            pass
        
        # Processar GASTOS
        gastos_por_mes = {}
        try:
            gastos_df = pd.read_excel(filepath, sheet_name="GASTOS ", header=None)
            if len(gastos_df) > 12:
                for idx in range(12, len(gastos_df)):
                    if len(gastos_df.columns) > 3:
                        try:
                            mes = gastos_df.iloc[idx, 1]
                            local = gastos_df.iloc[idx, 2]
                            valor = gastos_df.iloc[idx, 3]
                            
                            if pd.notna(valor) and pd.notna(local) and pd.notna(mes):
                                valor_num = float(valor) if pd.notna(valor) else 0
                                mes_str = str(mes).strip()
                                local_str = str(local).strip()
                                
                                if valor_num > 0 and mes_str and local_str:
                                    if mes_str not in gastos_por_mes:
                                        gastos_por_mes[mes_str] = {}
                                    if local_str not in gastos_por_mes[mes_str]:
                                        gastos_por_mes[mes_str][local_str] = 0
                                    gastos_por_mes[mes_str][local_str] += valor_num
                        except:
                            pass
        except:
            pass
        
        # Deletar arquivo temporário
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        
        # Retornar JSON
        response_data = {
            'sucesso': True,
            'contasData': contas_valores_mes,
            'mesesContas': meses_contas,
            'ganhosData': {
                'meses': meses_ganho,
                'entrada': entrada_ganho,
                'saida': saida_ganho,
                'total': total_ganho
            },
            'gastosData': gastos_por_mes
        }
        
        response = jsonify(response_data)
        response.headers['Access-Control-Allow-Origin'] = '*'
        print(f"[OK] Dados processados e retornados de {request.remote_addr}")
        return response
    
    except Exception as e:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        
        print(f"[ERRO] Processando Excel: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'erro': f'Erro: {str(e)}'}), 500

@app.route('/saude', methods=['GET', 'OPTIONS'])
def saude():
    """Verificar saúde do servidor"""
    if request.method == 'OPTIONS':
        return '', 204
    
    response = jsonify({'status': 'ok', 'servidor': 'rodando'})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# ==================== MIDDLEWARE ====================

@app.after_request
def add_cors_headers(response):
    """Adicionar headers CORS a todas as respostas"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print("DASHBOARD FINANCEIRO - SERVIDOR ATIVO")
    print("="*60)
    print(f"\n[✓] Servidor rodando em http://0.0.0.0:{port}")
    print(f"[✓] Acesse localmente: http://localhost:{port}")
    print(f"[✓] Acesse remotamente: http://<seu-ip>:{port}")
    print(f"\n[✓] CORS habilitado para todos os domínios")
    print(f"[✓] Máximo de upload: 16MB")
    print(f"[✓] Diretório de scripts: {SCRIPT_DIR}")
    print("\n" + "="*60)
    print("Pressione CTRL+C para parar o servidor")
    print("="*60 + "\n")
    
    sys.stdout.flush()
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
