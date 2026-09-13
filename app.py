import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Titanic Dashboard", layout="wide")
st.title("Titanic - Dashboard de Análise")

df = pd.read_csv("train.csv")

# --- Sidebar ---
st.sidebar.header("Filtros")
sexo = st.sidebar.multiselect("Sexo", df["Sex"].unique(), default=df["Sex"].unique())
classe = st.sidebar.multiselect("Classe", df["Pclass"].unique(), default=df["Pclass"].unique())
embarque = st.sidebar.multiselect("Embarque", df["Embarked"].dropna().unique(), default=df["Embarked"].dropna().unique())

filtro = df["Sex"].isin(sexo) & df["Pclass"].isin(classe) & df["Embarked"].isin(embarque)
df_f = df[filtro]

# --- Métricas ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de Passageiros", len(df_f))
c2.metric("Taxa de Sobrevivência", f"{df_f['Survived'].mean()*100:.1f}%")
c3.metric("Idade Média", f"{df_f['Age'].mean():.1f}")
c4.metric("Tarifa Média", f"${df_f['Fare'].mean():.2f}")

st.divider()

# --- Gráficos ---
col_a, col_b = st.columns(2)

with col_a:
    fig1 = px.histogram(df_f, x="Survived", color="Sex", barmode="group",
                        title="Sobrevivência por Sexo",
                        labels={"Survived": "Sobreviveu (0=Não, 1=Sim)", "count": "Quantidade"})
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    fig2 = px.histogram(df_f, x="Pclass", color="Survived", barmode="group",
                        title="Sobrevivência por Classe",
                        color_discrete_map={0: "#EF553B", 1: "#636EFA"},
                        labels={"Pclass": "Classe", "count": "Quantidade", "Survived": "Sobreviveu"})
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    fig3 = px.box(df_f, x="Pclass", y="Age", color="Survived",
                  title="Distribuição de Idade por Classe e Sobrevivência",
                  color_discrete_map={0: "#EF553B", 1: "#636EFA"},
                  labels={"Pclass": "Classe", "Age": "Idade", "Survived": "Sobreviveu"})
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    fig4 = px.box(df_f, x="Pclass", y="Fare", color="Survived",
                  title="Distribuição de Tarifa por Classe e Sobrevivência",
                  color_discrete_map={0: "#EF553B", 1: "#636EFA"},
                  labels={"Pclass": "Classe", "Fare": "Tarifa", "Survived": "Sobreviveu"})
    st.plotly_chart(fig4, use_container_width=True)

col_e, col_f = st.columns(2)

with col_e:
    sobrev = df_f[df_f["Survived"] == 1].groupby("Embarked").size().reset_index(name="count")
    fig5 = px.pie(sobrev, names="Embarked", values="count",
                  title="Embarque dos Sobreviventes",
                  labels={"Embarked": "Porto", "count": "Quantidade"})
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    fig6 = px.scatter(df_f, x="Age", y="Fare", color="Survived",
                      title="Idade vs Tarifa",
                      color_discrete_map={0: "#EF553B", 1: "#636EFA"},
                      labels={"Age": "Idade", "Fare": "Tarifa", "Survived": "Sobreviveu"},
                      opacity=0.6)
    st.plotly_chart(fig6, use_container_width=True)

# --- Tabela ---
st.divider()
st.subheader("Dados dos Passageiros")
st.dataframe(df_f[["PassengerId", "Name", "Sex", "Age", "Pclass", "Fare", "Survived"]], use_container_width=True)
