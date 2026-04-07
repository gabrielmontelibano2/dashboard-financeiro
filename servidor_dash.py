#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Flask Simples para Dashboard Financeiro
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(SCRIPT_DIR, 'dashboard.html')

@app.route('/', methods=['GET', 'OPTIONS'])
def serve_html():
    """Servir o dashboard.html"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            html = f.read()
        return html, 200, {
            'Content-Type': 'text/html; charset=utf-8',
            'Access-Control-Allow-Origin': '*'
        }
    except Exception as e:
        return str(e), 500

@app.route('/saude', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok'}), 200

@app.route('/processar-excel', methods=['POST', 'OPTIONS'])
def processar_excel():
    """Processar um arquivo Excel"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if 'arquivo' not in request.files:
            return jsonify({'erro': 'Arquivo não encontrado'}), 400
        
        arquivo = request.files['arquivo']
        if not arquivo or arquivo.filename == '':
            return jsonify({'erro': 'Arquivo vazio'}), 400
        
        # Salvar temporário
        filename = secure_filename(arquivo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
        arquivo.save(filepath)
        
        # Ler CONTAS
        contas_df = pd.read_excel(filepath, sheet_name="CONTAS", header=None)
        
        meses = []
        for col in range(16, min(28, len(contas_df.columns))):
            m = contas_df.iloc[1, col]
            if pd.notna(m):
                meses.append(str(m))
        
        contas_data = {}
        for row in range(2, len(contas_df)):
            conta = contas_df.iloc[row, 0]
            if pd.notna(conta):
                conta_str = str(conta).strip()
                valores = []
                for col in range(16, 16 + len(meses)):
                    try:
                        v = float(contas_df.iloc[row, col])
                    except:
                        v = 0
                    valores.append(v)
                if conta_str and valores:
                    contas_data[conta_str] = valores
        
        # Ler GANHO MENSAL
        ganho_df = pd.read_excel(filepath, sheet_name="GANHO MENSAL", header=None)
        
        meses_ganho = []
        entrada = []
        saida = []
        
        for row in range(19, min(29, len(ganho_df))):
            m = ganho_df.iloc[row, 1]
            if pd.notna(m):
                meses_ganho.append(str(m))
                try:
                    e = float(ganho_df.iloc[row, 2])
                except:
                    e = 0
                try:
                    s = float(ganho_df.iloc[row, 3])
                except:
                    s = 0
                entrada.append(e)
                saida.append(s)
        
        # Ler GASTOS
        gastos_df = pd.read_excel(filepath, sheet_name="GASTOS", header=None)
        
        gastos_data = {}
        for row in range(11, len(gastos_df)):
            try:
                mes = str(gastos_df.iloc[row, 1])
                cat = str(gastos_df.iloc[row, 2]).strip()
                val = float(gastos_df.iloc[row, 3])
                
                if mes and cat and val > 0:
                    if mes not in gastos_data:
                        gastos_data[mes] = {}
                    if cat not in gastos_data[mes]:
                        gastos_data[mes][cat] = 0
                    gastos_data[mes][cat] += val
            except:
                pass
        
        # Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Retornar
        result = {
            'contasData': contas_data,
            'mesesContas': meses,
            'ganhosData': {
                'meses': meses_ganho,
                'entrada': entrada,
                'saida': saida
            },
            'gastosData': gastos_data
        }
        
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n[OK] Servidor iniciando na porta {port}\n")
    app.run(host='0.0.0.0', port=port, debug=False)
