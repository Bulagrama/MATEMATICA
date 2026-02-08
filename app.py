import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Il Gioco dei Muretti", page_icon="🧱", layout="centered")

# 2. CSS "FORZATO" per la Griglia Mobile
st.markdown("""
    <style>
    /* Titolo e testi */
    .titolo { font-size: 32px !important; text-align: center; color: #FF4B4B; font-weight: bold; }
    .info-testo { font-size: 20px; text-align: center; margin: 10px 0; }
    .evidenza { color: #1f77b4; font-weight: bold; font-size: 26px; }
    .mattoncino-testo { font-size: 45px; text-align: center; letter-spacing: 2px; line-height: 1.2; margin: 15px 0; }

    /* CONTENITORE GRIGLIA: Forza i bottoni a stare vicini */
    .grid-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        padding: 10px;
    }

    /* Stile specifico per i bottoni dentro la griglia */
    div.stButton > button {
        width: 65px !important;
        height: 65px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        background-color: #f8f9fa !important;
        border: 2px solid #1f77b4 !important;
        color: #1f77b4 !important;
    }
    
    /* Rimuove i margini automatici di Streamlit che creano le colonne */
    [data-testid="column"] {
        flex: 0 1 auto !important;
        min-width: 0px !important;
        width: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titolo">🧱 Gioco dei Muretti</p>', unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Muretto del:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])
    if st.button("🔄 Reset"):
        st.session_state.ordine_attuale = 1
        st.rerun()

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

# 5. Logica e Grafica
mancanti_reali = target - st.session_state.parte_nota

st.markdown(f'<p class="info-testo">Muretto del <span class="evidenza">{target}</span></p>', unsafe_allow_html=True)
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)
st.markdown('<p class="info-testo">Quanti ne mancano? 🤔</p>', unsafe_allow_html=True)

# 6. PULSANTIERA ORIZZONTALE (Usando molte colonne piccole)
# Questo trucco crea una riga di bottoni che non va a capo in verticale su mobile
scelta = None
# Creiamo tante colonne quanti sono i possibili bottoni
col_list = st.columns(target) 

for i in range(1, target):
    with col_list[i-1]:
        if st.button(str(i), key=f"btn_{i}"):
            scelta = i

# 7. Gestione Risposta
if scelta is not None:
    if scelta == mancanti_reali:
        st.session_state.indovinato = True
        st.session_state.messaggio_errore = False
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success("BRAVISSIMO!")
        
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
