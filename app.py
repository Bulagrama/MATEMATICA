import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS "FLESSIBILE" PER BOTTONI GIGANTI ORIZZONTALI
st.markdown("""
    <style>
    /* Intestazione */
    .header-muretto { 
        background-color: #FF4B4B; 
        color: white; 
        padding: 20px; 
        border-radius: 20px; 
        text-align: center; 
        font-size: 35px !important; 
        font-weight: bold;
        margin-bottom: 20px;
    }
    .operazione { 
        font-size: 60px; 
        text-align: center; 
        font-weight: bold; 
        margin: 15px 0;
    }
    .mattoncino-testo { font-size: 70px; text-align: center; letter-spacing: 10px; line-height: 1; margin-bottom: 20px; }

    /* IL SEGRETO: Forza i contenitori dei bottoni a stare uno accanto all'altro */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
    }

    div[data-testid="column"] {
        flex: 0 1 auto !important;
        min-width: 90px !important; /* Forza i bottoni a non allargarsi a tutta pagina */
        max-width: 100px !important;
    }

    /* BOTTONI GIGANTI QUADRATI */
    .stButton > button {
        width: 90px !important;
        height: 90px !important;
        font-size: 40px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        background-color: #ffffff !important;
        border: 4px solid #1f77b4 !important;
        color: #1f77b4 !important;
        box-shadow: 0px 5px 0px #1a5e8f !important;
    }

    .stButton > button:active {
        box-shadow: 0px 1px 0px #1a5e8f !important;
        transform: translateY(4px);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Scegli il muretto:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])

# 4. Session State
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)
    st.session_state.domanda_id = 0

if 'ultimo_metodo' not in st.session_state or st.session_state.ultimo_metodo != metodo:
    st.session_state.ultimo_metodo = metodo
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)
    st.session_state.domanda_id += 1

mancanti_reali = target - st.session_state.parte_nota

# 5. UI
st.markdown(f'<div class="header-muretto">IL MURETTO DEL {target}</div>', unsafe_allow_html=True)

st.markdown(f'''
    <div class="operazione">
        <span style="color: blue;">{st.session_state.parte_nota}</span> 
        <span style="font-size: 35px; color: #666;">e</span> 
        <span style="color: #ff7f0e;">?</span>
    </div>
''', unsafe_allow_html=True)



st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

# 6. TASTIERA ORIZZONTALE FORZATA
# Creiamo tante colonne ma il CSS impedirà che diventino verticali
cols = st.columns(9) # Creiamo un numero fisso di colonne
scelta = None

for i in range(1, target):
    with cols[i-1]:
        if st.button(str(i), key=f"btn_{i}_id{st.session_state.domanda_id}"):
            scelta = i

# 7. Risposta
if scelta is not None:
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
        st.error(f"Sbagliato! {st.session_state.parte_nota} e {scelta} non fanno {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)
