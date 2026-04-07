import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configurar página
st.set_page_config(page_title="Dashboard Financeiro", layout="wide", initial_sidebar_state="expanded")

# Título e cor tema
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💰 Dashboard Financeiro Pessoal</h1>', unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    file_path = r"CONTROLE_FINANCEIRO_ATUALIZADO (1).xlsx"
    
    # Ler abas
    contas_df = pd.read_excel(file_path, sheet_name="CONTAS")
    ganho_df = pd.read_excel(file_path, sheet_name="GANHO MENSAL")
    gastos_df = pd.read_excel(file_path, sheet_name="GASTOS ")
    
    return contas_df, ganho_df, gastos_df

try:
    contas_df, ganho_df, gastos_df = load_data()
    
    # ===== TAB 1: VISÃO GERAL =====
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "💳 Contas", "📈 Ganhos", "💸 Gastos"])
    
    with tab1:
        st.header("Resumo Financeiro")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Informações Principais")
            st.info(f"""
            **Total de Contas:** {len([x for x in contas_df.iloc[:, 0] if pd.notna(x) and x != 'PROGRAMAÇÃO DE CONTAS' and x != 'MÊS REFERENCIA'])}
            
            **Período Analisado:** Março a Dezembro 2026
            """)
        
        with col2:
            st.subheader("📅 Última Atualização")
            st.success(f"**Data:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    
    # ===== TAB 2: CONTAS =====
    with tab2:
        st.header("Gestão de Contas")
        
        # Extrair dados relevantes da aba CONTAS
        contas_relevantes = contas_df.iloc[1:15, [0, 28]].copy()
        contas_relevantes.columns = ['Conta', 'Observações']
        contas_relevantes = contas_relevantes.dropna(subset=['Conta'])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Relação de Contas")
            st.dataframe(
                contas_relevantes,
                use_container_width=True,
                height=400
            )
        
        with col2:
            st.subheader("📊 Status de Contas")
            conta_count = len(contas_relevantes)
            fig = go.Figure(data=[
                go.Pie(
                    labels=['Ativas', 'Informativas'],
                    values=[conta_count, max(0, conta_count - 5)],
                    marker=dict(colors=['#1f77b4', '#ff7f0e'])
                )
            ])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 3: GANHOS =====
    with tab3:
        st.header("Análise de Ganhos Mensais")
        
        # Tentar extrair dados de ganhos
        try:
            # Procurar por padrão de months e values
            ganho_meses = []
            ganho_valores = []
            
            for idx, row in ganho_df.iterrows():
                mes_col = row.iloc[1] if len(row) > 1 else None
                valor_col = row.iloc[2] if len(row) > 2 else None
                
                if pd.notna(mes_col) and mes_col not in ['MÊS REF', 'NaN', np.nan]:
                    if isinstance(mes_col, str) and mes_col.strip() not in ['', 'NaN']:
                        ganho_meses.append(mes_col)
                        if pd.notna(valor_col) and isinstance(valor_col, (int, float)):
                            ganho_valores.append(float(valor_col))
            
            if ganho_meses and ganho_valores:
                ganhos_chart_df = pd.DataFrame({
                    'Mês': ganho_meses[:len(ganho_valores)],
                    'Ganho': ganho_valores
                })
                
                fig = px.bar(
                    ganhos_chart_df,
                    x='Mês',
                    y='Ganho',
                    title="📈 Ganho Mensal",
                    labels={'Ganho': 'Valor (R$)', 'Mês': 'Mês'},
                    color='Ganho',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Métricas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Ganho", f"R$ {sum(ganho_valores):.2f}")
                with col2:
                    st.metric("Média Mensal", f"R$ {np.mean(ganho_valores):.2f}")
                with col3:
                    st.metric("Meses Registrados", len(ganho_valores))
            else:
                st.warning("Dados de ganho não encontrados ou em formato diferente.")
        
        except Exception as e:
            st.warning(f"Não foi possível processar dados de ganhos: {e}")
    
    # ===== TAB 4: GASTOS =====
    with tab4:
        st.header("Análise de Gastos")
        
        try:
            # Procurar por categorias e valores
            gastos_dict = {}
            
            for idx, row in gastos_df.iterrows():
                categoria = row.iloc[0] if len(row) > 0 else None
                valor = row.iloc[1] if len(row) > 1 else None
                
                if isinstance(categoria, str) and categoria not in ['CATEGORIA', 'VALOR TOTAL', 'DATA'] and pd.notna(categoria):
                    if categoria.strip() not in ['', 'NaN']:
                        # Tentar converter valor
                        try:
                            if pd.notna(valor):
                                valor_num = float(str(valor).replace(',', '.'))
                                if valor_num > 0:
                                    gastos_dict[categoria.strip()] = valor_num
                        except:
                            pass
            
            if gastos_dict:
                gastos_clean = {k: v for k, v in gastos_dict.items() if v > 0}
                
                if gastos_clean:
                    gastos_df_plot = pd.DataFrame(list(gastos_clean.items()), columns=['Categoria', 'Valor'])
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        fig = px.bar(
                            gastos_df_plot.sort_values('Valor', ascending=True),
                            y='Categoria',
                            x='Valor',
                            orientation='h',
                            title="💸 Gastos por Categoria",
                            labels={'Valor': 'Valor (R$)', 'Categoria': 'Categoria'},
                            color='Valor',
                            color_continuous_scale='Reds'
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig_pie = px.pie(
                            gastos_df_plot,
                            values='Valor',
                            names='Categoria',
                            title="Distribuição de Gastos"
                        )
                        fig_pie.update_layout(height=400)
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    # Métricas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Gastos", f"R$ {sum(gastos_clean.values()):.2f}")
                    with col2:
                        st.metric("Maior Gasto", f"R$ {max(gastos_clean.values()):.2f}")
                    with col3:
                        st.metric("Categorias", len(gastos_clean))
        
        except Exception as e:
            st.warning(f"Não foi possível processar dados de gastos: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9em;">
    📊 Dashboard Financeiro | Dados atualizados de: CONTROLE_FINANCEIRO_ATUALIZADO.xlsx
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.info("Certifique-se de que o arquivo 'CONTROLE_FINANCEIRO_ATUALIZADO (1).xlsx' está na mesma pasta que o script.")
