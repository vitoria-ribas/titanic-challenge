import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Titanic Dashboard", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        border: 1px solid var(--color-400, #d6d6d6);
        border-radius: 10px;
        padding: 14px 18px;
    }
    [data-testid="stMetric"] label { font-size: 0.85rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Titanic - Dashboard de Análise")

df = pd.read_csv("train.csv")

# --- Paleta de Cores Padronizada ---
COR_NAO_SOBREVIVEU = "#E07A5F"  # coral suave
COR_SOBREVIVEU = "#2A6F97"       # azul-petróleo
COR_AZUL_ESCURO = "#1B2A4A"     # azul escuro (fundo/destaque)
COR_NEUTRO = "#6C757D"           # cinza neutro

PALETA_SEXO = {"male": "#2A6F97", "female": "#E07A5F"}
PALETA_SOBREVIVEU = {0: COR_NAO_SOBREVIVEU, 1: COR_SOBREVIVEU}
MAPA_TEXTO = {0: "Não Sobreviveu", 1: "Sobreviveu"}

MAPA_PORTO = {"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"}
MAPA_SEXO_DISPLAY = {"male": "Masculino", "female": "Feminino"}
MAPA_SEXO_FILTRO = {v: k for k, v in MAPA_SEXO_DISPLAY.items()}

# --- Sidebar ---
st.sidebar.header("Filtros")
sexo = st.sidebar.multiselect(
    "Sexo",
    list(MAPA_SEXO_DISPLAY.values()),
    default=list(MAPA_SEXO_DISPLAY.values()),
)
sexo_original = [MAPA_SEXO_FILTRO[s] for s in sexo]
classe = st.sidebar.multiselect("Classe", df["Pclass"].unique(), default=df["Pclass"].unique())
embarque = st.sidebar.multiselect("Embarque", df["Embarked"].dropna().unique(), default=df["Embarked"].dropna().unique())

if not sexo or not classe or not embarque:
    st.warning("Por favor, selecione pelo menos uma opção em cada filtro da barra lateral.")
    st.stop()

filtro = df["Sex"].isin(sexo_original) & df["Pclass"].isin(classe) & df["Embarked"].isin(embarque)
df_f = df[filtro]

# --- Métricas ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    with st.container(border=True):
        st.metric("Total de Passageiros", len(df_f))
with c2:
    with st.container(border=True):
        st.metric("Taxa de Sobrevivência", f"{df_f['Survived'].mean()*100:.1f}%")
with c3:
    with st.container(border=True):
        st.metric("Idade Média", f"{df_f['Age'].mean():.1f}")
with c4:
    with st.container(border=True):
        st.metric("Tarifa Média", f"${df_f['Fare'].mean():.2f}")

st.markdown("")

# --- Gráficos ---
with st.container(border=True):
    st.subheader("Sobrevivência")
    col_a, col_b = st.columns(2)

    with col_a:
        df_f["Status"] = df_f["Survived"].map(MAPA_TEXTO)
        fig1 = px.histogram(
            df_f, x="Status", color="Sex", barmode="group",
            title="Sobrevivência por Sexo",
            color_discrete_map=PALETA_SEXO,
            labels={"Status": "Situação", "Sex": "Sexo", "count": "Quantidade"},
            category_orders={"Status": ["Não Sobreviveu", "Sobreviveu"]},
            template="plotly_white",
        )
        fig1.update_layout(
            xaxis_title="Situação", yaxis_title="Quantidade",
            legend_title="Sexo",
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.histogram(
            df_f, x="Pclass", color="Status", barmode="group",
            title="Sobrevivência por Classe",
            color_discrete_map=PALETA_SOBREVIVEU,
            labels={"Pclass": "Classe", "count": "Quantidade", "Status": "Situação"},
            category_orders={"Status": ["Não Sobreviveu", "Sobreviveu"]},
            template="plotly_white",
        )
        fig2.update_layout(
            xaxis_title="Classe", yaxis_title="Quantidade",
            legend_title="Situação",
        )
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("")

with st.container(border=True):
    st.subheader("Distribuições")
    col_c, col_d = st.columns(2)

    with col_c:
        fig3 = px.box(
            df_f, x="Pclass", y="Age", color="Status",
            title="Distribuição de Idade por Classe e Sobrevivência",
            color_discrete_map=PALETA_SOBREVIVEU,
            labels={"Pclass": "Classe", "Age": "Idade", "Status": "Situação"},
            category_orders={"Status": ["Não Sobreviveu", "Sobreviveu"]},
            template="plotly_white",
        )
        fig3.update_layout(
            xaxis_title="Classe", yaxis_title="Idade",
            legend_title="Situação",
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        fig4 = px.box(
            df_f, x="Pclass", y="Fare", color="Status",
            title="Distribuição de Tarifa por Classe e Sobrevivência",
            color_discrete_map=PALETA_SOBREVIVEU,
            labels={"Pclass": "Classe", "Fare": "Tarifa", "Status": "Situação"},
            category_orders={"Status": ["Não Sobreviveu", "Sobreviveu"]},
            template="plotly_white",
        )
        fig4.update_layout(
            xaxis_title="Classe", yaxis_title="Tarifa",
            legend_title="Situação",
        )
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("")

with st.container(border=True):
    st.subheader("Embarque e Relações")
    col_e, col_f = st.columns(2)

    with col_e:
        sobrev = df_f[df_f["Survived"] == 1].groupby("Embarked").size().reset_index(name="count")
        sobrev["Porto"] = sobrev["Embarked"].map(MAPA_PORTO)
        fig5 = px.pie(
            sobrev, names="Porto", values="count",
            title="Embarque dos Sobreviventes",
            color_discrete_sequence=[COR_SOBREVIVEU, COR_AZUL_ESCURO, COR_NAO_SOBREVIVEU],
            template="plotly_white",
        )
        fig5.update_traces(textinfo="label+percent+value")
        fig5.update_layout(legend_title="Porto de Embarque")
        st.plotly_chart(fig5, use_container_width=True)

    with col_f:
        fig6 = px.scatter(
            df_f, x="Age", y="Fare", color="Status",
            title="Idade vs Tarifa",
            color_discrete_map=PALETA_SOBREVIVEU,
            labels={"Age": "Idade", "Fare": "Tarifa", "Status": "Situação"},
            category_orders={"Status": ["Não Sobreviveu", "Sobreviveu"]},
            opacity=0.6,
            template="plotly_white",
        )
        fig6.update_layout(
            xaxis_title="Idade", yaxis_title="Tarifa",
            legend_title="Situação",
        )
        st.plotly_chart(fig6, use_container_width=True)

st.markdown("")

# --- Análise Idade vs Tarifa ---
with st.container(border=True):
    st.subheader("Análise Idade vs Tarifa por Sobrevivência")
    col_age, col_age_ctrl = st.columns([3, 1])

    with col_age_ctrl:
        st.markdown("**Filtros rápidos**")
        mostra_todos = st.checkbox("Mostrar todos os pontos", value=True)
        opacidade = st.slider("Opacidade", 0.1, 1.0, 0.55)
        tamanho = st.slider("Tamanho dos pontos", 4, 20, 8)

    with col_age:
        fig_age = px.scatter(
            df_f, x="Age", y="Fare", color="Status",
            size="Fare" if mostra_todos else None,
            size_max=tamanho * 3,
            title="Idade vs Tarifa — Segmentado por Sobrevivência",
            color_discrete_map=PALETA_SOBREVIVEU,
            labels={"Age": "Idade", "Fare": "Tarifa", "Status": "Situação"},
            category_orders={"Status": ["Não Sobreviveu", "Sobreviveu"]},
            opacity=opacidade,
            template="plotly_white",
            marginal_x="histogram",
            marginal_y="box",
        )
        fig_age.update_layout(
            xaxis_title="Idade", yaxis_title="Tarifa (Fare)",
            legend_title="Situação",
            height=520,
        )
        st.plotly_chart(fig_age, use_container_width=True)

    fig_age_hist = px.histogram(
        df_f, x="Age", y="Fare", color="Status",
        histfunc="avg",
        barmode="overlay",
        title="Tarifa Média por Faixa de Idade",
        color_discrete_map=PALETA_SOBREVIVEU,
        labels={"Age": "Idade", "Fare": "Tarifa Média", "Status": "Situação"},
        category_orders={"Status": ["Não Sobreviveu", "Sobreviveu"]},
        template="plotly_white",
        nbins=25,
    )
    fig_age_hist.update_layout(
        xaxis_title="Idade", yaxis_title="Tarifa Média",
        legend_title="Situação",
    )
    st.plotly_chart(fig_age_hist, use_container_width=True)

st.markdown("")

# --- Análise Interativa ---
with st.container(border=True):
    st.subheader("Análise Interativa: Distribuição por Status de Sobrevivência")

    METRICAS = {
        "Idade": "Age",
        "Tarifa": "Fare",
        "Número de Parentes a Bordo": "SibSp",
        "Número de Pais/Filhos a Bordo": "Parch",
    }

    metrica_label = st.selectbox("Selecione a métrica", list(METRICAS.keys()), index=0)
    metrica_coluna = METRICAS[metrica_label]

    fig_hist = px.histogram(
        df_f, x=metrica_coluna, color="Status",
        barmode="group",
        title=f"Distribuição de {metrica_label} por Sobrevivência",
        color_discrete_map=PALETA_SOBREVIVEU,
        labels={metrica_coluna: metrica_label, "count": "Quantidade", "Status": "Situação"},
        category_orders={"Status": ["Não Sobreviveu", "Sobreviveu"]},
        template="plotly_white",
    )
    fig_hist.update_layout(
        xaxis_title=metrica_label, yaxis_title="Quantidade",
        legend_title="Situação",
        bargap=0.1,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# --- Tabela ---
with st.container(border=True):
    st.subheader("Dados dos Passageiros")
    df_tabela = df_f[["PassengerId", "Name", "Sex", "Age", "Pclass", "Fare", "Survived"]].rename(columns={
        "PassengerId": "ID do Passageiro",
        "Name": "Nome",
        "Sex": "Sexo",
        "Age": "Idade",
        "Pclass": "Classe",
        "Fare": "Tarifa",
        "Survived": "Sobreviveu",
    })
    st.dataframe(df_tabela, use_container_width=True)
