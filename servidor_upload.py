#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Flask para Dashboard Financeiro
Roda em localhost:5000 e fornece:
- Página HTML do dashboard
- API para processar uploads de Excel
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import json
from werkzeug.utils import secure_filename
import os
import tempfile
import traceback

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()  # Usar pasta temp do SO

# Obter diretório do script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def index():
    """Servir o dashboard.html"""
    arquivo_html = os.path.join(SCRIPT_DIR, 'dashboard.html')
    if os.path.exists(arquivo_html):
        with open(arquivo_html, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        from flask import Response
        resp = Response(conteudo, mimetype='text/html')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp
    return "Dashboard não encontrado.", 404

@app.route('/processar-excel', methods=['POST'])
def processar_excel():
    """Recebe arquivo Excel, processa e retorna dados em JSON"""
    filepath = None
    try:
        if 'arquivo' not in request.files:
            return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
        
        arquivo = request.files['arquivo']
        if arquivo.filename == '':
            return jsonify({'erro': 'Arquivo sem nome'}), 400
        
        if not arquivo.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'erro': 'Arquivo deve ser Excel (.xlsx ou .xls)'}), 400
        
        # Salvar temporariamente
        filename = secure_filename(arquivo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        arquivo.save(filepath)
        
        # Processar dados
        try:
            contas_df = pd.read_excel(filepath, sheet_name="CONTAS", header=None)
        except Exception as e:
            return jsonify({'erro': f'Aba CONTAS não encontrada: {str(e)}'}), 400
        
        try:
            ganho_df = pd.read_excel(filepath, sheet_name="GANHO MENSAL", header=None)
        except:
            ganho_df = None
        
        try:
            gastos_df = pd.read_excel(filepath, sheet_name="GASTOS ", header=None)
        except:
            gastos_df = None
        
        # ===== PROCESSAR CONTAS =====
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
                        if valores:  # Só adicionar se houver valores
                            contas_valores_mes[nome_str] = valores
        
        # ===== PROCESSAR GANHOS =====
        meses_ganho = []
        entrada_ganho = []
        saida_ganho = []
        total_ganho = []
        
        if ganho_df is not None and len(ganho_df) > 19:
            for idx in range(19, min(29, len(ganho_df))):
                if len(ganho_df.columns) > 4:
                    mes = ganho_df.iloc[idx, 1] if len(ganho_df.columns) > 1 else None
                    entrada = ganho_df.iloc[idx, 2] if len(ganho_df.columns) > 2 else None
                    saida = ganho_df.iloc[idx, 3] if len(ganho_df.columns) > 3 else None
                    total_g = ganho_df.iloc[idx, 4] if len(ganho_df.columns) > 4 else None
                    
                    if pd.notna(mes) and str(mes).strip() != '':
                        meses_ganho.append(str(mes).strip())
                        try:
                            entrada_ganho.append(float(entrada) if pd.notna(entrada) else 0)
                        except:
                            entrada_ganho.append(0)
                        try:
                            saida_ganho.append(float(saida) if pd.notna(saida) else 0)
                        except:
                            saida_ganho.append(0)
                        try:
                            total_ganho.append(float(total_g) if pd.notna(total_g) else 0)
                        except:
                            total_ganho.append(0)
        
        # ===== PROCESSAR GASTOS =====
        gastos_por_mes = {}
        
        print(f"[DEBUG] gastos_df type: {type(gastos_df)}, is None: {gastos_df is None}")
        if gastos_df is not None:
            print(f"[DEBUG] gastos_df shape: {gastos_df.shape}")
        
        if gastos_df is not None and len(gastos_df) > 12:
            print(f"[DEBUG] GASTOS tem {len(gastos_df)} linhas e {len(gastos_df.columns)} colunas")
            
            for idx in range(12, min(15, len(gastos_df))):
                print(f"[DEBUG] Linha {idx}: {gastos_df.iloc[idx, :4].tolist()}")
            
            for idx in range(12, len(gastos_df)):
                if len(gastos_df.columns) > 3:
                    try:
                        data_val = gastos_df.iloc[idx, 0] if len(gastos_df.columns) > 0 else None
                        mes = gastos_df.iloc[idx, 1] if len(gastos_df.columns) > 1 else None
                        local = gastos_df.iloc[idx, 2] if len(gastos_df.columns) > 2 else None
                        valor = gastos_df.iloc[idx, 3] if len(gastos_df.columns) > 3 else None
                        
                        if pd.notna(valor) and pd.notna(local) and pd.notna(mes):
                            valor_num = float(valor) if pd.notna(valor) else 0
                            mes_str = str(mes).strip() if pd.notna(mes) else "INDEFINIDO"
                            local_str = str(local).strip() if pd.notna(local) else "OUTROS"
                            
                            if valor_num > 0 and mes_str and mes_str != 'nan' and local_str != 'nan':
                                if mes_str not in gastos_por_mes:
                                    gastos_por_mes[mes_str] = {}
                                if local_str not in gastos_por_mes[mes_str]:
                                    gastos_por_mes[mes_str][local_str] = 0
                                gastos_por_mes[mes_str][local_str] += valor_num
                    except Exception as e:
                        print(f"[DEBUG] Erro ao processar linha {idx}: {str(e)}")
                        pass
        else:
            print(f"[DEBUG] Condicao nao atendida: gastos_df={gastos_df}, len={len(gastos_df) if gastos_df is not None else 'N/A'}")
        
        print(f"[DEBUG] Gastos processados: {len(gastos_por_mes)} meses")
        
        
        # Retornar JSON
        return jsonify({
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
        })
    
    except Exception as e:
        # Limpar arquivo temporário em caso de erro
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        
        print(f"[ERRO] {str(e)}")
        print(traceback.format_exc())
        return jsonify({'erro': f'Erro ao processar: {str(e)}'}), 500

@app.route('/saude', methods=['GET'])
def saude():
    """Verificar se servidor está rodando"""
    return jsonify({'status': 'ok', 'servidor': 'rodando'})

if __name__ == '__main__':
    print("[OK] Servidor de upload iniciado em http://0.0.0.0:5000")
    print("[OK] Acesse de outro PC usando: http://<seu-ip>:5000")
    print("[OK] O dashboard pode agora fazer upload de arquivos Excel!")
    app.run(host='0.0.0.0', port=5000, debug=False)
