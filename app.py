import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS PER TASTI "GIGANTESCHI" E INTERFACCIA
st.markdown("""
    <style>
    /* Intestazione muretto */
    .header-muretto { 
        background-color: #FF4B4B; 
        color: white; 
        padding: 20px; 
        border-radius: 20px; 
        text-align: center; 
        font-size: 40px !important; 
        font-weight: bold;
        margin-bottom: 20px;
    }
    .operazione { 
        font-size: 70px; 
        text-align: center; 
        font-weight: bold; 
        color: #333; 
        margin: 20px 0;
    }
    .mattoncino-testo { font-size: 80px; text-align: center; letter-spacing: 10px; line-height: 1; margin-bottom: 20px; }
    
    /* LA GRIGLIA DEI TASTI GIGANTI */
    .container-tasti {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        margin-top: 30px;
    }

    /* Stile del singolo bottone */
    .stButton > button {
        width: 120px !important;   /* LARGHEZZA ENORME */
        height: 120px !important;  /* ALTEZZA ENORME */
        font-size: 50px !important; /* NUMERO GIGANTE */
        font-weight: bold !important;
        border-radius: 20px !important;
        background-color: #ffffff !important;
        border: 4px solid #1f77b4 !important;
        color: #1f77b4 !important;
        transition: 0.2s;
        box-shadow: 0px 6px 0px #1a5e8f !important; /* Effetto 3D */
    }

    .stButton > button:active {
        box-shadow: 0px 2px 0px #1a5e8f !important;
        transform: translateY(4px);
    }

    /* Nasconde i margini delle colonne per tenere i bottoni vicini */
    [data-testid="column"] {
        width: auto !important;
        flex: none !important;
    }
    [data-testid="stHorizontalBlock"] {
        justify-content: center !important;
        gap: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Scegli il muretto:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])

# 4. Inizializzazione Sessione
if 'ordine_attuale' not in st.session_state: st.session_state.ordine_attuale = 1
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

if 'ultimo_metodo' not in st.session_state or st.session_state.ultimo_metodo != metodo:
    st.session_state.ultimo_metodo = metodo
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

mancanti_reali = target - st.session_state.parte_nota

# 5. Interfaccia Visiva
st.markdown(f'<div class="header-muretto">MURETTO DEL {target}</div>', unsafe_allow_html=True)

st.markdown(f'''
    <div class="operazione">
        <span style="color: blue;">{st.session_state.parte_nota}</span> 
        <span style="font-size: 40px; color: #666;">e</span> 
        <span style="color: #ff7f0e;">?</span>
    </div>
''', unsafe_allow_html=True)

st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

# 6. TASTIERA A COLONNE FISSE (Massima dimensione)
# Usiamo st.columns ma forziamo la larghezza via CSS
scelta = None
# Creiamo una riga di bottoni. Se sono troppi, Streamlit li manderà a capo, 
# ma grazie al CSS sopra resteranno grandi.
cols = st.columns(5) # Griglia di 5 colonne per riga

for i in range(1, target):
    with cols[(i-1) % 5]:
        if st.button(str(i), key=f"btn_{i}"):
            scelta = i

# 7. Logica Risposta
if scelta is not None:
    if scelta == mancanti_reali:
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success(f"BRAVO! {st.session_state.parte_nota} e {scelta} fanno {target}")
        
        time.sleep(2.5)
        
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
        st.rerun()
    else:
        st.error(f"Sbagliato! {st.session_state.parte_nota} e {scelta} non fanno {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)
