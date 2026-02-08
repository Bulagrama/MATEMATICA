import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS PER BOTTONI E GRAFICA (Migliorato)
st.markdown("""
    <style>
    .header-muretto { 
        background-color: #FF4B4B; 
        color: white; 
        padding: 15px; 
        border-radius: 15px; 
        text-align: center; 
        font-size: 35px !important; 
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .info-testo { font-size: 24px; text-align: center; margin: 5px 0; color: #555; }
    .operazione { 
        font-size: 50px; 
        text-align: center; 
        font-weight: bold; 
        color: #333; 
        margin: 15px 0; 
        background: #fdfdfd; 
        border-radius: 15px; 
        padding: 15px; 
        border: 3px dashed #1f77b4; 
    }
    .mattoncino-testo { font-size: 60px; text-align: center; letter-spacing: 5px; line-height: 1.1; margin-bottom: 20px; }
    
    /* BOTTONI GIGANTI */
    div[data-testid="stSegmentedControl"] button {
        min-height: 85px !important;
        min-width: 65px !important;
        font-size: 35px !important;
        font-weight: bold !important;
        background-color: #f0f2f6 !important;
        border: 2px solid #1f77b4 !important;
        color: #1f77b4 !important;
    }
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
    }
    div[data-testid="stSegmentedControl"] label { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar per impostazioni
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Scegli il muretto:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])

# 4. Inizializzazione Sessione (Sicura)
if 'domanda_id' not in st.session_state: st.session_state.domanda_id = 0
if 'ordine_attuale' not in st.session_state: st.session_state.ordine_attuale = 1
if 'current_target' not in st.session_state: st.session_state.current_target = target
if 'ultimo_metodo' not in st.session_state: st.session_state.ultimo_metodo = metodo

if st.session_state.current_target != target or st.session_state.ultimo_metodo != metodo:
    st.session_state.current_target = target
    st.session_state.ultimo_metodo = metodo
    st.session_state.ordine_attuale = 1
    st.session_state.domanda_id += 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

if 'parte_nota' not in st.session_state:
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

mancanti_reali = target - st.session_state.parte_nota

# 5. Visualizzazione Principale
st.markdown(f'<div class="header-muretto">MURETTO DEL {target}</div>', unsafe_allow_html=True)

# Operazione con la "E" al posto del "+"
st.markdown(f'''
    <div class="operazione">
        <span style="color: blue;">{st.session_state.parte_nota}</span> 
        &nbsp;<span style="font-size: 35px; color: #666;">e</span>&nbsp; 
        <span style="color: #ff7f0e;">?</span>
    </div>
''', unsafe_allow_html=True)

# Visualizzazione mattoncini
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)
st.markdown('<p class="info-testo">Tocca il numero amico: 🤔</p>', unsafe_allow_html=True)

# 6. Tastiera Gigante
scelta_fatta = st.segmented_control(
    label="Scegli",
    options=[i for i in range(1, target)],
    selection_mode="single",
    key=f"tast_v{st.session_state.domanda_id}" 
)

# 7. Gestione Risposta
if scelta_fatta is not None:
    if scelta_fatta == mancanti_reali:
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta_fatta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success(f"BRAVISSIMO! {st.session_state.parte_nota} e {scelta_fatta} fanno {target}!")
        
        time.sleep(2.5)
        
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
        
        st.session_state.domanda_id += 1 
        st.rerun()
    else:
        st.error(f"Prova ancora! {st.session_state.parte_nota} e {scelta_fatta} non formano il {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta_fatta}</p>', unsafe_allow_html=True)

# 8. Riepilogo
with st.expander("Vedi tutti i mattoncini amici"):
    for i in range(1, target):
        st.write(f"**{i}** e **{target-i}**")
