import streamlit as st
import random
import time

# 1. Configurazione
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS per testi e grafica
st.markdown("""
    <style>
    .titolo { font-size: 32px !important; text-align: center; color: #FF4B4B; font-weight: bold; }
    .info-testo { font-size: 20px; text-align: center; margin: 10px 0; }
    .mattoncino-testo { font-size: 50px; text-align: center; letter-spacing: 3px; line-height: 1.2; }
    .evidenza { color: #1f77b4; font-weight: bold; font-size: 26px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titolo">🧱 Gioco dei Muretti</p>', unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Muretto del:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])

# 4. Inizializzazione Sessione
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = random.randint(1, target - 1)
    st.session_state.scelta = None
    st.session_state.indovinato = False

if 'ultimo_metodo' not in st.session_state or st.session_state.ultimo_metodo != metodo:
    st.session_state.ultimo_metodo = metodo
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

mancanti_reali = target - st.session_state.parte_nota

# 5. Visualizzazione
st.markdown(f'<p class="info-testo">Muretto del <span class="evidenza">{target}</span></p>', unsafe_allow_html=True)
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)
st.markdown('<p class="info-testo">Quanti ne mancano? 🤔</p>', unsafe_allow_html=True)

# 6. TASTIERA ORIZZONTALE (FIX MOBILE DEFINITIVO)
# Creiamo una riga di bottoni usando un selettore nativo di Streamlit che su mobile resta compatto
scelta_fatta = st.segmented_control(
    label="Scegli il numero:",
    options=[i for i in range(1, target)],
    selection_mode="single",
    key="tastiera_muretti"
)

# 7. Gestione Risposta
if scelta_fatta:
    if scelta_fatta == mancanti_reali:
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta_fatta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success("BRAVISSIMO!")
        
        time.sleep(2)
        # Logica avanzamento
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
        
        # Reset del controllo segmentato per la prossima domanda
        st.rerun()
    else:
        st.error(f"Riprova! {st.session_state.parte_nota} + {scelta_fatta} non fa {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta_fatta}</p>', unsafe_allow_html=True)

# 8. Aiuto
with st.expander("Aiuto"):
    for i in range(1, target):
        st.write(f"{i} + {target-i} = {target}")
