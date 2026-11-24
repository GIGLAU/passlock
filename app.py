import streamlit as st
import pyperclip

from database import (
    criar_tabela,
    adicionar,
    listar,
    excluir
)

from crypto import (
    criptografar,
    descriptografar
)

criar_tabela()

st.set_page_config(
    page_title="PassLock",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 PassLock")

if "master" not in st.session_state:
    st.session_state.master = ""

senha_mestra = st.text_input(
    "Senha Mestra",
    type="password"
)

if senha_mestra:
    st.session_state.master = senha_mestra

    st.subheader("Nova Credencial")

    with st.form("cadastro"):
        servico = st.text_input("Serviço")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        observacao = st.text_area("Observação")

        salvar = st.form_submit_button("Salvar")

        if salvar:

            senha_cripto = criptografar(
                senha,
                senha_mestra
            )

            adicionar(
                servico,
                usuario,
                senha_cripto,
                observacao
            )

            st.success("Registro salvo!")

    st.divider()

    st.subheader("Credenciais")

    registros = listar()

    for item in registros:

        id_, servico, usuario, senha, obs = item

        try:
            senha_real = descriptografar(
                senha,
                senha_mestra
            )

        except:
            senha_real = "Senha mestra inválida"

        with st.expander(servico):

            st.write(f"Usuário: {usuario}")
            st.write(f"Senha: {senha_real}")
            st.write(f"Obs: {obs}")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    f"Copiar {id_}"
                ):
                    pyperclip.copy(
                        senha_real
                    )
                    st.success(
                        "Senha copiada!"
                    )

            with col2:

                if st.button(
                    f"Excluir {id_}"
                ):
                    excluir(id_)
                    st.rerun()