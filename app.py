import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS "ULTRA-AGGRESSIVO" PER MOBILE
st.markdown("""
    <style>
    /* Forza le colonne a stare affiancate anche su schermi piccolissimi */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 45px !important; /* Ridotto per far stare più bottoni */
    }
    
    /* Riduce lo spazio tra le colonne */
    [data-testid="stHorizontalBlock"] {
        gap: 5px !important;
    }

    .titolo { font-size: 30px !important; text-align: center; color: #FF4B4B; font-weight: bold; }
    .info-testo { font-size: 18px; text-align: center; margin-bottom: 5px; }
    .mattoncino-testo { font-size: 40px; text-align: center; line-height: 1.2; }

    /* Rende i bottoni dei quadratini compatti */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0 !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
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
    st.session_state.messaggio_errore = False
    st.session_state.indovinato = False

if 'ultimo_metodo' not in st.session_state or st.session_state.ultimo_metodo != metodo:
    st.session_state.ultimo_metodo = metodo
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

# 5. Logica
mancanti_reali = target - st.session_state.parte_nota

st.markdown(f'<p class="info-testo">Muretto del <b>{target}</b>. Hai <b>{st.session_state.parte_nota}</b> blu:</p>', unsafe_allow_html=True)
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)
st.markdown('<p class="info-testo">Quanti ne mancano? 🤔</p>', unsafe_allow_html=True)

# 6. PULSANTIERA ORIZZONTALE - IL TRUCCO DELLE COLONNE MULTIPLE
# Usiamo tante colonne quante sono i pulsanti necessari
numero_pulsanti = target - 1
cols = st.columns(numero_pulsanti)

scelta = None
for i in range(1, target):
    with cols[i-1]:
        if st.button(str(i), key=f"btn_{i}"):
            scelta = i

# 7. Gestione Risposta
if scelta is not None:
    if scelta == mancanti_reali:
        st.session_state.indovinato = True
        st.session_state.messaggio_errore = False
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success("BRAVO!")
        
        time.sleep(2) 
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
            
        st.session_state.indovinato = False
        st.rerun()
    else:
        st.session_state.messaggio_errore = True
        st.session_state.ultima_scelta_errata = scelta

if st.session_state.messaggio_errore and not st.session_state.indovinato:
    st.error(f"Riprova! {st.session_state.parte_nota} + {st.session_state.ultima_scelta_errata} non fa {target}")
    st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * st.session_state.ultima_scelta_errata}</p>', unsafe_allow_html=True)
