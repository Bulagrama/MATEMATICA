import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS "GIGANTE" PER MOBILE
st.markdown("""
    <style>
    .header-muretto { 
        background-color: #FF4B4B; color: white; padding: 15px; 
        border-radius: 15px; text-align: center; font-size: 30px !important; font-weight: bold;
    }
    .operazione { font-size: 55px; text-align: center; font-weight: bold; margin: 15px 0; }
    .mattoncino-testo { font-size: 60px; text-align: center; letter-spacing: 8px; line-height: 1; }

    /* FORZA IL SEGMENTED CONTROL A DIVENTARE UNA TASTIERA GIGANTE */
    div[data-testid="stSegmentedControl"] > div {
        display: flex !important;
        flex-direction: row !important; 
        flex-wrap: wrap !important;   
        justify-content: center !important;
        gap: 15px !important; /* Più spazio tra i tasti per non sbagliare */
    }

    div[data-testid="stSegmentedControl"] button {
        flex: 0 1 120px !important; /* LARGHEZZA GIGANTE */
        height: 120px !important;    /* ALTEZZA GIGANTE */
        min-width: 120px !important;
        font-size: 50px !important;  /* NUMERO ENORME */
        font-weight: 900 !important;
        border: 4px solid #1f77b4 !important;
        border-radius: 20px !important;
        background-color: white !important;
        box-shadow: 0px 6px 0px #1a5e8f !important; /* Effetto 3D per bimbi */
    }

    /* Colore quando selezionato */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
        transform: translateY(4px);
        box-shadow: 0px 2px 0px #1a5e8f !important;
    }
    
    div[data-testid="stSegmentedControl"] label { display: none; }

    /* Adattamento per schermi molto stretti */
    @media (max-width: 400px) {
        div[data-testid="stSegmentedControl"] button {
            flex: 0 1 100px !important;
            height: 100px !important;
            min-width: 100px !important;
            font-size: 40px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Muretto del:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])

# 4. Inizializzazione Sessione
if 'domanda_id' not in st.session_state: st.session_state.domanda_id = 0
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)
    st.session_state.domanda_id += 1

mancanti_reali = target - st.session_state.parte_nota

# 5. UI
st.markdown(f'<div class="header-muretto">MURETTO DEL {target}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="operazione"><span style="color: blue;">{st.session_state.parte_nota}</span> <span style="font-size: 30px; color: #666;">e</span> <span style="color: #ff7f0e;">?</span></div>', unsafe_allow_html=True)
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

# 6. TASTIERA "PULSANTONI"
scelta = st.segmented_control(
    "Scegli", 
    options=[i for i in range(1, target)], 
    key=f"tasto_{st.session_state.domanda_id}"
)

# 7. Risposta
if scelta:
    if scelta == mancanti_reali:
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success("BRAVO!")
        time.sleep(2)
        
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
            
        st.session_state.domanda_id += 1
        st.rerun()
    else:
        st.error("Riprova!")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)
