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
            
            # Linha 1 tem MÊS REFERENCIA e depois meses em colunas 16-27 (JANEIRO até DEZEMBRO)
            for col in range(16, 28):  # 12 meses
                if col < len(contas_df.columns):
                    m = contas_df.iloc[1, col]
                    if pd.notna(m):
                        meses_contas.append(str(m).strip())
            
            # Linhas 2-28 contém os dados das contas
            for idx in range(2, 29):  # Até linha 28 (antes de TOTAL)
                if idx < len(contas_df):
                    nome = str(contas_df.iloc[idx, 0]).strip() if pd.notna(contas_df.iloc[idx, 0]) else ""
                    if nome and nome != "TOTAL DE CONTAS" and nome != "nan":
                        valores = []
                        for col in range(16, 28):  # Colunas 16-27 (12 meses)
                            try:
                                val = contas_df.iloc[idx, col]
                                valores.append(float(val) if pd.notna(val) else 0)
                            except:
                                valores.append(0)
                        if valores and any(v > 0 for v in valores):  # Só adiciona se tem algum valor > 0
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
            
            # Há 2 blocos! Usar o segundo bloco "RECEITA BRUTA MENSAL" (linhas 17+)
            # Linha 17 tem headers: MÊS REF (col 1), ENTRADA (col 2), SAÍDA (col 3), TOTAL (col 4)
            # Linhas 19+ contêm os dados (linha 18 é vazia)
            
            for idx in range(19, len(ganho_df)):
                mes = ganho_df.iloc[idx, 1] if len(ganho_df.columns) > 1 else None
                if pd.notna(mes) and str(mes).strip() and str(mes).strip() != "nan":
                    meses_ganho.append(str(mes).strip())
                    
                    # ENTRADA (col 2)
                    entrada_val = float(ganho_df.iloc[idx, 2]) if len(ganho_df.columns) > 2 and pd.notna(ganho_df.iloc[idx, 2]) else 0
                    entrada.append(entrada_val)
                    
                    # SAÍDA (col 3)
                    saida_val = float(ganho_df.iloc[idx, 3]) if len(ganho_df.columns) > 3 and pd.notna(ganho_df.iloc[idx, 3]) else 0
                    saida.append(saida_val)
                    
                    # TOTAL (col 4)
                    total_val = float(ganho_df.iloc[idx, 4]) if len(ganho_df.columns) > 4 and pd.notna(ganho_df.iloc[idx, 4]) else 0
                    total_ganho.append(total_val)
        except Exception as e:
            sys.stdout.write(f"[GANHO] Erro: {str(e)}\n")
            sys.stdout.flush()
        
        # ===== GASTOS =====
        gastos_por_mes = {}
        
        try:
            gastos_df = pd.read_excel(filepath, sheet_name="GASTOS ", header=None)
            
            # Processar em blocos: cada bloco tem header + dados + total + vazio
            idx = 0
            while idx < len(gastos_df):
                # Procurar por header "TOTAL DE GASTOS"
                if len(gastos_df.columns) > 1:
                    header_val = gastos_df.iloc[idx, 1]
                    if pd.notna(header_val) and "TOTAL DE GASTOS" in str(header_val):
                        # Extrair nome do mês do header
                        header_str = str(header_val).strip()
                        # Format: "TOTAL DE GASTOS MARÇO" -> "MARÇO"
                        mes_name = header_str.replace("TOTAL DE GASTOS", "").strip()
                        
                        if mes_name and mes_name not in gastos_por_mes:
                            gastos_por_mes[mes_name] = {}
                        
                        # Ler categorias nos próximos 2-3 linhas (até encontrar VALOR TOTAL)
                        for cat_idx in range(idx + 1, min(idx + 5, len(gastos_df))):
                            categoria = gastos_df.iloc[cat_idx, 0]
                            valor = gastos_df.iloc[cat_idx, 1]
                            
                            if pd.notna(categoria) and pd.notna(valor):
                                cat_str = str(categoria).strip()
                                
                                # Pular se for VALOR TOTAL (é só o totalizador)
                                if cat_str and "VALOR TOTAL" not in cat_str and "CATEGORIA" not in cat_str and cat_str != "nan":
                                    try:
                                        valor_num = float(valor)
                                        if valor_num > 0:
                                            gastos_por_mes[mes_name][cat_str] = valor_num
                                    except:
                                        pass
                        
                        # Pular 5 linhas para próximo bloco
                        idx += 5
                    else:
                        idx += 1
                else:
                    idx += 1
            
        except Exception as e:
            sys.stdout.write(f"[GASTOS] Erro: {str(e)}\n")
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
