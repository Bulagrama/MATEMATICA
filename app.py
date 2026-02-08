import streamlit as st
import random
import time

# 1. Configurazione
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS PER BOTTONI GIGANTI (Segmented Control Customization)
st.markdown("""
    <style>
    /* Ingrandisce il titolo e le scritte */
    .titolo { font-size: 38px !important; text-align: center; color: #FF4B4B; font-weight: bold; margin-bottom: 5px; }
    .info-testo { font-size: 24px; text-align: center; margin: 10px 0; line-height: 1.2; }
    .mattoncino-testo { font-size: 55px; text-align: center; letter-spacing: 4px; line-height: 1.1; margin: 15px 0; }
    .evidenza { color: #1f77b4; font-weight: bold; font-size: 30px; }

    /* FORZA DIMENSIONE BOTTONI SEGMENTED CONTROL */
    div[data-testid="stSegmentedControl"] button {
        min-height: 80px !important; /* Molto alti */
        min-width: 60px !important;  /* Più larghi */
        font-size: 30px !important;  /* Numeri giganti */
        font-weight: bold !important;
        background-color: #f0f2f6 !important;
        border: 2px solid #1f77b4 !important;
        margin: 2px !important;
    }

    /* Colore quando il bottone è selezionato */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
    }
    
    /* Nasconde l'etichetta del controllo per pulizia */
    div[data-testid="stSegmentedControl"] label {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titolo">🧱 Gioco dei Muretti</p>', unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Muretto del:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])
    st.info("Ideale per la classe 1ª")

# 4. Inizializzazione Sessione
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = random.randint(1, target - 1)
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

# 6. TASTIERA GIGANTE (Segmented Control forzato)
scelta_fatta = st.segmented_control(
    label="Scegli il numero",
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
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
        
        st.rerun()
    else:
        st.error(f"Riprova! {st.session_state.parte_nota} + {scelta_fatta} non fa {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta_fatta}</p>', unsafe_allow_html=True)

# 8. Aiuto
with st.expander("Vedi i muretti amici"):
    for i in range(1, target):
        st.write(f"{i} + {target-i} = {target}")
