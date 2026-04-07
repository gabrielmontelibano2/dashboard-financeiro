#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Flask para Dashboard Financeiro
Versão v3 - Diagnóstico completo de GASTOS
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
import tempfile
import sys

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def index():
    """Servir o dashboard.html"""
    arquivo_html = os.path.join(SCRIPT_DIR, 'dashboard.html')
    if os.path.exists(arquivo_html):
        return send_file(arquivo_html, mimetype='text/html')
    return "Dashboard nao encontrado.", 404

@app.route('/saude', methods=['GET'])
def saude():
    """Health check"""
    return jsonify({"status": "ok", "servidor": "rodando"}), 200

@app.route('/processar-excel', methods=['POST'])
def processar_excel():
    """Processar upload de Excel"""
    sys.stdout.write("[UPLOAD] Requisicao recebida\n")
    sys.stdout.flush()
    
    filepath = None
    try:
        # Receber arquivo
        if 'arquivo' not in request.files:
            return jsonify({"erro": "Nenhum arquivo enviado"}), 400
        
        arquivo = request.files['arquivo']
        if not arquivo.filename:
            return jsonify({"erro": "Arquivo vazio"}), 400
        
        # Salvar temporariamente
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
        arquivo.save(filepath)
        
        # ===== CONTAS =====
        contas_dados = {}
        meses_contas = []
        
        try:
            contas_df = pd.read_excel(filepath, sheet_name="CONTAS", header=None)
            
            # Ler meses
            for col in range(16, min(28, len(contas_df.columns))):
                m = contas_df.iloc[1, col]
                if pd.notna(m):
                    meses_contas.append(str(m).strip())
            
            # Ler contas
            for idx in range(2, min(28, len(contas_df))):
                nome = str(contas_df.iloc[idx, 0]).strip() if pd.notna(contas_df.iloc[idx, 0]) else ""
                if nome and nome != "TOTAL DE CONTAS":
                    valores = []
                    for col in range(16, min(28, len(contas_df.columns))):
                        try:
                            val = contas_df.iloc[idx, col]
                            valores.append(float(val) if pd.notna(val) else 0)
                        except:
                            valores.append(0)
                    if valores:
                        contas_dados[nome] = valores
        except Exception as e:
            sys.stdout.write(f"[CONTAS] Erro: {str(e)}\n")
            sys.stdout.flush()
        
        # ===== GANHOS =====
        meses_ganho = []
        entrada = []
        saida = []
        total_ganho = []
        
        try:
            ganho_df = pd.read_excel(filepath, sheet_name="GANHO MENSAL", header=None)
            for idx in range(19, min(29, len(ganho_df))):
                mes = ganho_df.iloc[idx, 1] if len(ganho_df.columns) > 1 else None
                if pd.notna(mes) and str(mes).strip():
                    meses_ganho.append(str(mes).strip())
                    entrada.append(float(ganho_df.iloc[idx, 2]) if len(ganho_df.columns) > 2 and pd.notna(ganho_df.iloc[idx, 2]) else 0)
                    saida.append(float(ganho_df.iloc[idx, 3]) if len(ganho_df.columns) > 3 and pd.notna(ganho_df.iloc[idx, 3]) else 0)
                    total_ganho.append(float(ganho_df.iloc[idx, 4]) if len(ganho_df.columns) > 4 and pd.notna(ganho_df.iloc[idx, 4]) else 0)
        except Exception as e:
            sys.stdout.write(f"[GANHO] Erro: {str(e)}\n")
            sys.stdout.flush()
        
        # ===== GASTOS - DIAGNÓSTICO =====
        sys.stdout.write("[GASTOS] Iniciando processamento...\n")
        sys.stdout.flush()
        
        gastos_por_mes = {}
        
        try:
            # Listar todas as sheets
            with pd.ExcelFile(filepath) as xls:
                sheets = xls.sheet_names
                sys.stdout.write(f"[GASTOS] Sheets disponíveis: {sheets}\n")
                sys.stdout.flush()
            
            # Tentar ler
            sys.stdout.write("[GASTOS] Tentando ler sheet 'GASTOS ' (com espaço)...\n")
            sys.stdout.flush()
            
            gastos_df = pd.read_excel(filepath, sheet_name="GASTOS ", header=None)
            sys.stdout.write(f"[GASTOS] Sucesso! Shape: {gastos_df.shape}\n")
            sys.stdout.flush()
            
            # Processar
            sys.stdout.write(f"[GASTOS] Processando {len(gastos_df) - 12} linhas (a partir de linha 12)...\n")
            sys.stdout.flush()
            
            for idx in range(12, len(gastos_df)):
                try:
                    if len(gastos_df.columns) > 3:
                        mes = gastos_df.iloc[idx, 1]
                        local = gastos_df.iloc[idx, 2]
                        valor = gastos_df.iloc[idx, 3]
                        
                        if pd.notna(valor) and pd.notna(local) and pd.notna(mes):
                            valor_num = float(valor)
                            mes_str = str(mes).strip()
                            local_str = str(local).strip()
                            
                            if valor_num > 0 and mes_str and local_str and mes_str != 'nan' and local_str != 'nan':
                                if mes_str not in gastos_por_mes:
                                    gastos_por_mes[mes_str] = {}
                                if local_str not in gastos_por_mes[mes_str]:
                                    gastos_por_mes[mes_str][local_str] = 0
                                gastos_por_mes[mes_str][local_str] += valor_num
                except Exception as e:
                    pass
            
            sys.stdout.write(f"[GASTOS] Resultado final: {len(gastos_por_mes)} meses com dados\n")
            for mes, cats in gastos_por_mes.items():
                total = sum(cats.values())
                sys.stdout.write(f"  - {mes}: {len(cats)} categorias, Total R$ {total:,.2f}\n")
            sys.stdout.flush()
            
        except Exception as e:
            sys.stdout.write(f"[GASTOS] ERRO FATAL: {type(e).__name__}: {str(e)}\n")
            sys.stdout.flush()
        
        # Retornar JSON
        return jsonify({
            'contasData': contas_dados,
            'mesesContas': meses_contas,
            'ganhosData': {
                'meses': meses_ganho,
                'entrada': entrada,
                'saida': saida,
                'total': total_ganho
            },
            'gastosData': gastos_por_mes
        }), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

if __name__ == '__main__':
    sys.stdout.write("[OK] Servidor iniciado em http://0.0.0.0:5000\n")
    sys.stdout.write("[OK] Acesse de outro PC usando: http://<seu-ip>:5000\n")
    sys.stdout.flush()
    app.run(host='0.0.0.0', port=5000, debug=False)
