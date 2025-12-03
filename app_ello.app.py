%%writefile app.py
import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(page_title="Ello Consultoria - Comparativo Tarifário", page_icon="⚡")

# --- Cabeçalho e Identidade Visual ---
st.title("⚡ Ello Consultoria")
st.header("Análise Técnica: Azul vs. Verde")
st.write("Calculadora fundamentada nas resoluções vigentes da CEMIG (Grupo A).")
st.markdown("---")

# --- BLOCO 1: INPUT DE DADOS (Lateral) ---
with st.sidebar:
    st.header("1. Parâmetros da Fatura")
    demanda_medida = st.number_input("Demanda Máxima Medida (kW)", value=150.0)
    consumo_ponta = st.number_input("Consumo na Ponta (kWh)", value=2500.0)
    consumo_fponta = st.number_input("Consumo Fora de Ponta (kWh)", value=35000.0)

    st.markdown("---")
    st.header("2. Tarifas CEMIG (R$)")
    st.caption("Ajuste conforme resolução ANEEL vigente")

    # Tarifas Verde
    tv_demanda = st.number_input("Verde: Demanda (R$/kW)", value=28.50)
    tv_kwh_ponta = st.number_input("Verde: Energia Ponta (R$/kWh)", value=1.95)
    tv_kwh_fponta = st.number_input("Verde: Energia F. Ponta (R$/kWh)", value=0.55)

    # Tarifas Azul
    ta_dem_ponta = st.number_input("Azul: Demanda Ponta (R$/kW)", value=45.00)
    ta_dem_fponta = st.number_input("Azul: Demanda F. Ponta (R$/kW)", value=18.00)
    ta_kwh_ponta = st.number_input("Azul: Energia Ponta (R$/kWh)", value=0.85)
    ta_kwh_fponta = st.number_input("Azul: Energia F. Ponta (R$/kWh)", value=0.55)

# --- BLOCO 2: MOTOR DE CÁLCULO ---

# Cálculo Tarifa VERDE
custo_verde_dem = demanda_medida * tv_demanda
custo_verde_kwh_p = consumo_ponta * tv_kwh_ponta
custo_verde_kwh_fp = consumo_fponta * tv_kwh_fponta
total_verde = custo_verde_dem + custo_verde_kwh_p + custo_verde_kwh_fp

# Cálculo Tarifa AZUL (Simulação)
custo_azul_dem_p = demanda_medida * ta_dem_ponta
custo_azul_dem_fp = demanda_medida * ta_dem_fponta
custo_azul_kwh_p = consumo_ponta * ta_kwh_ponta
custo_azul_kwh_fp = consumo_fponta * ta_kwh_fponta
total_azul = custo_azul_dem_p + custo_azul_dem_fp + custo_azul_kwh_p + custo_azul_kwh_fp

# Delta
economia = total_verde - total_azul

# --- BLOCO 3: APRESENTAÇÃO DOS RESULTADOS ---

col1, col2 = st.columns(2)

with col1:
    st.subheader("Cenário Tarifa VERDE")
    st.metric(label="Custo Mensal Estimado", value=f"R$ {total_verde:,.2f}")
    st.text(f"Demanda: R$ {custo_verde_dem:,.2f}")
    st.text(f"Consumo: R$ {custo_verde_kwh_p + custo_verde_kwh_fp:,.2f}")

with col2:
    st.subheader("Cenário Tarifa AZUL")
    st.metric(label="Custo Mensal Estimado", value=f"R$ {total_azul:,.2f}", delta=f"R$ {economia:,.2f}")
    st.text(f"Demanda: R$ {custo_azul_dem_p + custo_azul_dem_fp:,.2f}")
    st.text(f"Consumo: R$ {custo_azul_kwh_p + custo_azul_kwh_fp:,.2f}")

st.markdown("---")

# --- Veredito Técnico ---
st.subheader("📋 Veredito Técnico Ello")

if economia > 0:
    st.success(f"**RECOMENDAÇÃO: MIGRAÇÃO PARA TARIFA AZUL.**")
    st.write(f"A economia estimada é de **R$ {economia:,.2f} por mês**. O alto consumo na ponta justifica pagar uma demanda diferenciada para obter um kWh mais barato.")
else:
    st.error(f"**RECOMENDAÇÃO: MANTER TARIFA VERDE.**")
    st.write(f"A Tarifa Azul aumentaria a conta em **R$ {abs(economia):,.2f}**. O perfil de carga atual não justifica os custos fixos elevados da demanda de ponta da modalidade Azul.")

# --- Gráfico Visual ---
dados_grafico = pd.DataFrame({
    'Modalidade': ['Verde', 'Azul'],
    'Custo Total (R$)': [total_verde, total_azul]
})
st.bar_chart(dados_grafico, x='Modalidade', y='Custo Total (R$)')