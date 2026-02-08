import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS PER TASTI GIGANTI E GRAFICA (Massima dimensione)
st.markdown("""
    <style>
    /* Intestazione muretto */
    .header-muretto { 
        background-color: #FF4B4B; 
        color: white; 
        padding: 20px; 
        border-radius: 20px; 
        text-align: center; 
        font-size: 45px !important; 
        font-weight: bold;
        margin-bottom: 25px;
    }
    .info-testo { font-size: 28px; text-align: center; margin: 10px 0; color: #444; }
    .operazione { 
        font-size: 60px; 
        text-align: center; 
        font-weight: bold; 
        color: #333; 
        margin: 20px 0; 
        background: #fdfdfd; 
        border-radius: 20px; 
        padding: 20px; 
        border: 4px dashed #1f77b4; 
    }
    .mattoncino-testo { font-size: 70px; text-align: center; letter-spacing: 8px; line-height: 1.1; margin-bottom: 30px; }
    
    /* FORZA TASTI GIGANTI - SEGMENTED CONTROL */
    div[data-testid="stSegmentedControl"] {
        display: flex;
        justify-content: center;
    }
    
    div[data-testid="stSegmentedControl"] button {
        min-height: 110px !important; /* ALTEZZA MASSIMA */
        min-width: 85px !important;  /* LARGHEZZA MASSIMA */
        font-size: 45px !important;  /* NUMERI ENORMI */
        font-weight: 900 !important;
        background-color: #ffffff !important;
        border: 3px solid #1f77b4 !important;
        margin: 5px !important;
        border-radius: 15px !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* Colore quando premuto */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
        transform: scale(1.05);
    }
    
    div[data-testid="stSegmentedControl"] label { display: none; }
    
    /* Ottimizzazione mobile */
    @media (max-width: 600px) {
        div[data-testid="stSegmentedControl"] button {
            min-height: 90px !important;
            min-width: 70px !important;
            font-size: 35px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Scegli il muretto:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])

# 4. Inizializzazione Sessione
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

# 5. Interfaccia
st.markdown(f'<div class="header-muretto">IL MURETTO DEL {target}</div>', unsafe_allow_html=True)

st.markdown(f'''
    <div class="operazione">
        <span style="color: blue;">{st.session_state.parte_nota}</span> 
        &nbsp;<span style="font-size: 40px; color: #666;">e</span>&nbsp; 
        <span style="color: #ff7f0e;">?</span>
    </div>
''', unsafe_allow_html=True)


st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)
st.markdown('<p class="info-testo">Qual è il numero amico? 👇</p>', unsafe_allow_html=True)

# 6. Tastiera "SUPER GIGANTE"
scelta_fatta = st.segmented_control(
    label="Scegli",
    options=[i for i in range(1, target)],
    selection_mode="single",
    key=f"tast_v{st.session_state.domanda_id}" 
)

# 7. Logica Risposta
if scelta_fatta is not None:
    if scelta_fatta == mancanti_reali:
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta_fatta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success(f"GRANDE! {st.session_state.parte_nota} e {scelta_fatta} fanno {target}")
        
        time.sleep(2.5)
        
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
        
        st.session_state.domanda_id += 1 
        st.rerun()
    else:
        st.error(f"Sbagliato! {st.session_state.parte_nota} e {scelta_fatta} non fanno {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta_fatta}</p>', unsafe_allow_html=True)

# 8. Espansore per aiuto
with st.expander("Aiuto"):
    for i in range(1, target):
        st.write(f"**{i}** e **{target-i}**")
