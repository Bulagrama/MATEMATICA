import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS PER TESTI E BOTTONI FANTASMA
st.markdown("""
    <style>
    .header-muretto { 
        background-color: #FF4B4B; color: white; padding: 15px; 
        border-radius: 15px; text-align: center; font-size: 30px !important; font-weight: bold;
    }
    .operazione { font-size: 60px; text-align: center; font-weight: bold; margin: 15px 0; }
    .mattoncino-testo { font-size: 65px; text-align: center; letter-spacing: 8px; line-height: 1; margin-bottom: 20px; }
    
    /* Rendiamo i bottoni di Streamlit dei quadratoni giganti e forziamo l'allineamento */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 10px !important;
    }
    
    div[data-testid="column"] {
        flex: 0 1 20% !important; /* Forza 5 bottoni per riga circa */
        min-width: 80px !important;
        max-width: 100px !important;
    }

    .stButton > button {
        width: 80px !important;
        height: 80px !important;
        font-size: 40px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        background-color: white !important;
        border: 4px solid #1f77b4 !important;
        color: #1f77b4 !important;
        box-shadow: 0px 4px 0px #1a5e8f !important;
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

# 5. Interfaccia
st.markdown(f'<div class="header-muretto">IL MURETTO DEL {target}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="operazione"><span style="color: blue;">{st.session_state.parte_nota}</span> <span style="font-size: 40px; color: #666;">e</span> <span style="color: #ff7f0e;">?</span></div>', unsafe_allow_html=True)
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

# 6. TASTIERA GIGANTE (Trucco CSS Flexbox)
scelta = None
# Creiamo un numero fisso di colonne molto piccole
cols = st.columns(10) 

for i in range(1, target):
    with cols[i-1]:
        if st.button(str(i), key=f"btn_{i}_{st.session_state.domanda_id}"):
            scelta = i

# 7. Logica Risposta
if scelta is not None:
    if scelta == mancanti_reali:
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success(f"BRAVO! {st.session_state.parte_nota} e {scelta} fanno {target}")
        time.sleep(2)
        
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
            
        st.session_state.domanda_id += 1
        st.rerun()
    else:
        st.error(f"Riprova!")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)
