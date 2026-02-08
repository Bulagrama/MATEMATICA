import streamlit as st
import random

# Configurazione stile "scuola"
st.set_page_config(page_title="Il Gioco dei Muretti", page_icon="🧱", layout="wide")

# CSS personalizzato per rendere i caratteri più grandi
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight: bold; }
    .mattoncino { font-size:40px; }
    </style>
    """, unsafe_allow_complete=True)

st.title("🧱 Il Gioco dei Muretti")
st.write("### Aiuta i muratori a completare il muretto del numero!")

# Scelta del numero obiettivo nella sidebar (o in alto)
target = st.number_input("Su quale numero lavoriamo oggi?", min_value=2, max_value=10, value=6)

st.divider()

# Inizializzazione della sessione per mantenere la domanda
if 'parte_nota' not in st.session_state or st.session_state.get('last_target') != target:
    st.session_state.parte_nota = random.randint(0, target)
    st.session_state.last_target = target
    st.session_state.risposta_corretta = False

# Layout a due colonne per l'esercizio centrale
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("La Sfida:")
    st.markdown(f"<p class='big-font'>Il muretto è alto {target}</p>", unsafe_allow_complete=True)
    st.markdown(f"Abbiamo già messo <span style='color:blue; font-size:40px;'>{st.session_state.parte_nota}</span> mattoncini.", unsafe_allow_complete=True)
    
    # Visualizzazione grafica dei mattoncini presenti
    st.markdown("🟦 " * st.session_state.parte_nota)
    
    st.write("---")
    risposta = st.number_input("Quanti ne mancano per arrivare in cima?", min_value=0, max_value=target, step=1, key="input_bimbo")

with col2:
    st.subheader("Il tuo Muretto:")
    # Visualizzazione del muretto che si compone
    mancanti = target - st.session_state.parte_nota
    
    if risposta == mancanti:
        st.success("BRAVISSIMO! 🎉")
        st.markdown(f"<p class='mattoncino'>{'🟦' * st.session_state.parte_nota}{'🟧' * risposta}</p>", unsafe_allow_complete=True)
        st.write(f"### {st.session_state.parte_nota} + {risposta} = {target}")
        if st.button("Prossimo Muretto ➡️"):
            st.session_state.parte_nota = random.randint(0, target)
            st.rerun()
    elif risposta != 0:
        st.warning("Ancora un piccolo sforzo... prova a contare!")
        # Mostra i mattoncini attuali + quelli inseriti dall'utente (se sbagliati)
        st.markdown(f"<p class='mattoncino'>{'🟦' * st.session_state.parte_nota}{'⬜' * risposta}</p>", unsafe_allow_complete=True)

# Footer con i muretti già scoperti
st.sidebar.header("I muretti amici")
for i in range(target + 1):
    st.sidebar.text(f"{i} + {target-i} = {target}")
