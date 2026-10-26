"""
Dashboard demonstrativo da NexoContábil
ATENÇÃO: o arquivo CSV incluído contém dados inteiramente simulados.
Não representa registros financeiros reais da empresa.
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="NexoContábil | Dashboard demonstrativo", layout="wide")
st.title("Dashboard demonstrativo — NexoContábil")
st.caption("Base 100% simulada para fins acadêmicos. Não utilizar como retrato financeiro real.")

DATA_PATH = Path(__file__).parent / "dados" / "cobrancas_simuladas.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["data_vencimento"] = pd.to_datetime(data["data_vencimento"], errors="coerce")
    data["data_pagamento"] = pd.to_datetime(data["data_pagamento"], errors="coerce")
    data["valor_cobrado"] = pd.to_numeric(data["valor_cobrado"], errors="coerce")
    data["competencia"] = data["competencia"].astype(str)
    return data

df = load_data()

# Filtros
competencias = sorted(df["competencia"].dropna().unique())
selected = st.multiselect("Filtrar competência", competencias, default=competencias)
view = df[df["competencia"].isin(selected)].copy()

if view.empty:
    st.warning("Selecione pelo menos uma competência para visualizar os dados.")
    st.stop()

# Define vencida não paga a partir da data atual do computador
hoje = pd.Timestamp.today().normalize()
view["inadimplente"] = (view["data_vencimento"] < hoje) & (view["data_pagamento"].isna())

total_cobrado = view["valor_cobrado"].sum()
qtd_cobrancas = len(view)
qtd_vencidas_nao_pagas = int(view["inadimplente"].sum())
taxa_inadimplencia = (qtd_vencidas_nao_pagas / qtd_cobrancas * 100) if qtd_cobrancas else 0

c1, c2 = st.columns(2)
c1.metric("Total de cobranças registradas", f"R$ {total_cobrado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Taxa de cobranças vencidas e não pagas", f"{taxa_inadimplencia:.1f}%")

st.caption(f"Registros no filtro: {qtd_cobrancas} | Vencidas e não pagas: {qtd_vencidas_nao_pagas}")

# Gráfico 1: status por quantidade
status_counts = view["status"].value_counts().rename_axis("Situação").reset_index(name="Quantidade")
fig_status = px.pie(status_counts, names="Situação", values="Quantidade",
                    title="Distribuição das cobranças por situação", hole=0.35)
st.plotly_chart(fig_status, use_container_width=True)

# Gráfico 2: valor cobrado por condomínio (top 10 no filtro)
por_condominio = (view.groupby("condominio_id", as_index=False)["valor_cobrado"]
                  .sum().sort_values("valor_cobrado", ascending=False).head(10))
fig_condo = px.bar(por_condominio, x="condominio_id", y="valor_cobrado",
                   title="10 condomínios com maior valor de cobranças na amostra",
                   labels={"condominio_id": "Condomínio simulado", "valor_cobrado": "Valor cobrado (R$)"})
st.plotly_chart(fig_condo, use_container_width=True)

# Gráfico 3: evolução mensal por status
mensal = (view.groupby(["competencia", "status"], as_index=False)
          .agg(valor_cobrado=("valor_cobrado", "sum")))
fig_mensal = px.line(mensal, x="competencia", y="valor_cobrado", color="status",
                     markers=True, title="Evolução mensal dos valores cobrados por situação",
                     labels={"competencia": "Competência", "valor_cobrado": "Valor cobrado (R$)", "status": "Situação"})
st.plotly_chart(fig_mensal, use_container_width=True)

with st.expander("Visualizar registros simulados"):
    st.dataframe(view, use_container_width=True)

st.download_button(
    "Baixar CSV filtrado",
    data=view.to_csv(index=False).encode("utf-8-sig"),
    file_name="cobrancas_filtradas_simuladas.csv",
    mime="text/csv"
)
