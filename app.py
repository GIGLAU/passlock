import streamlit as st
import pyperclip
from database import (
    conectar,
    criar_tabela,
    criar_tabela_master,
    salvar_master,
    validar_master,
    adicionar,
    listar,
    excluir
)

criar_tabela()
criar_tabela_master()

from crypto import (
    criptografar,
    descriptografar
)

criar_tabela()
conn = conectar()
cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM configuracao"
)

existe_master = cursor.fetchone()[0]> 0

conn.close()
if not existe_master:

    st.title("🔐 Criar Senha Mestra")

    senha1 = st.text_input(
        "Senha Mestra",
        type="password",
        key="senha1"
    )

    senha2 = st.text_input(
        "Confirmar Senha",
        type="password",
        key="senha2"
    )

    if st.button(
        "Criar senha mestra",
        key="criar_master"
    ):

        if len(senha1.strip()) < 8:
            st.error(
                "A senha deve ter no mínimo 8 caracteres."
            )

        elif senha1 != senha2:
            st.error(
                "As senhas não coincidem."
            )

        else:
            salvar_master(senha1)

            st.success(
                "Senha mestra criada com sucesso!"
            )

            st.rerun()

    st.stop()

st.title("🔒 PassLock")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "master" not in st.session_state:
    st.session_state.master = ""
if not st.session_state.autenticado:

    senha_mestra = st.text_input(
        "Senha Mestra",
        type="password"
    )

    if st.button("Entrar"):

        if validar_master(senha_mestra):
            st.session_state.autenticado = True
            st.session_state.master = senha_mestra
            st.rerun()
        else:
            st.error("Senha mestra inválida")

        st.stop()
if validar_master(senha_mestra):
    st.session_state.autenticado = True
    st.session_state.master = senha_mestra
    st.rerun()
# DAQUI PARA BAIXO O USUÁRIO JÁ ESTÁ LOGADO
senha_mestra = st.session_state.get("master", "")
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