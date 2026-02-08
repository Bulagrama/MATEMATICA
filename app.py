import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS MIRATO (Solo per la tastiera del gioco)
st.markdown("""
    <style>
    /* Titoli e testi */
    .header-muretto { 
        background-color: #FF4B4B; color: white; padding: 15px; 
        border-radius: 15px; text-align: center; font-size: 30px !important; font-weight: bold;
    }
    .operazione { font-size: 55px; text-align: center; font-weight: bold; margin: 15px 0; }
    .mattoncino-testo { font-size: 60px; text-align: center; letter-spacing: 8px; line-height: 1; margin-bottom: 20px; }

    /* TRUCCO PER LA TASTIERA: Colpiamo solo il radio button nel corpo centrale */
    [data-testid="stMain"] div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 20px !important; /* SPAZIO TRA I TASTI */
    }

    /* TRASFORMAZIONE LABEL IN MATTONCINI GIGANTI */
    [data-testid="stMain"] div[data-testid="stRadio"] label {
        background-color: white !important;
        border: 4px solid #1f77b4 !important;
        border-radius: 15px !important;
        width: 100px !important;
        height: 100px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 5px 0px #1a5e8f !important;
        padding: 0 !important;
    }

    /* MOSTRA SOLO IL NUMERO E NASCONDE IL PALLINO */
    [data-testid="stMain"] div[data-testid="stRadio"] label div[dir] {
        display: none !important; /* Nasconde il cerchietto */
    }
    
    [data-testid="stMain"] div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        font-size: 45px !important;
        font-weight: bold !important;
        color: #1f77b4 !important;
        margin: 0 !important;
    }

    /* Stile quando selezionato */
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #1f77b4 !important;
    }
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Ora protetta, non verrà colpita dal CSS)
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Muretto del:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo di gioco:", ["Casuale", "Ordinato"])

# 4. Inizializzazione Sessione
if 'domanda_id' not in st.session_state: st.session_state.domanda_id = 0
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)
    st.session_state.domanda_id += 1

mancanti_reali = target - st.session_state.parte_nota

# 5. UI Principale
st.markdown(f'<div class="header-muretto">IL MURETTO DEL {target}</div>', unsafe_allow_html=True)
st.markdown(f'''
    <div class="operazione">
        <span style="color: blue;">{st.session_state.parte_nota}</span> 
        <span style="font-size: 35px; color: #666;">e</span> 
        <span style="color: #ff7f0e;">?</span>
    </div>
''', unsafe_allow_html=True)



st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

# 6. TASTIERA A MATTONCINI
opzioni = [str(i) for i in range(1, target)]
scelta_radio = st.radio(
    "Tastiera", 
    options=opzioni, 
    index=None, 
    key=f"tastiera_{st.session_state.domanda_id}",
    label_visibility="collapsed"
)

# 7. Risposta
if scelta_radio:
    scelta = int(scelta_radio)
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
        st.error(f"Riprova! {st.session_state.parte_nota} e {scelta} non fanno {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)
