import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS MIRATO
st.markdown("""
    <style>
    .header-muretto { 
        background-color: #FF4B4B; color: white; padding: 15px; 
        border-radius: 15px; text-align: center; font-size: 30px !important; font-weight: bold;
    }
    .operazione { font-size: 55px; text-align: center; font-weight: bold; margin: 15px 0; }
    .mattoncino-testo { font-size: 60px; text-align: center; letter-spacing: 8px; line-height: 1; margin-bottom: 20px; }

    /* Rende il selettore del numero più grande e centrato */
    div[data-testid="stNumberInput"] {
        width: 200px;
        margin: 0 auto;
    }

    /* NASCONDE L'ETICHETTA "TASTIERA" */
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] {
        display: none !important;
    }

    /* TASTIERA: Layout orizzontale e staccato */
    [data-testid="stMain"] div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 15px !important;
    }

    /* MATTONCINI GIGANTI */
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

    [data-testid="stMain"] div[data-testid="stRadio"] label div[dir] {
        display: none !important;
    }
    
    [data-testid="stMain"] div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        font-size: 45px !important;
        font-weight: bold !important;
        color: #1f77b4 !important;
        margin: 0 !important;
    }

    /* EFFETTO SELEZIONE */
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #1f77b4 !important;
        box-shadow: none !important;
        transform: translateY(4px) !important;
    }
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Solo per il metodo)
with st.sidebar:
    st.header("⚙️ Modalità")
    metodo = st.radio("Metodo di gioco:", ["Casuale", "Ordinato"])

# 4. Scelta del Muretto in pagina principale
st.markdown('<p style="text-align: center; font-size: 20px; margin-bottom: 0;">Scegli il muretto da studiare:</p>', unsafe_allow_html=True)
target = st.number_input("Target", min_value=2, max_value=10, value=6, label_visibility="collapsed")

# 5. Inizializzazione Sessione
if 'domanda_id' not in st.session_state: st.session_state.domanda_id = 0
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)
    st.session_state.domanda_id += 1

mancanti_reali = target - st.session_state.parte_nota

# 6. UI Principale
st.markdown(f'<div class="header-muretto">IL MURETTO DEL {target}</div>', unsafe_allow_html=True)
st.markdown(f'''
    <div class="operazione">
        <span style="color: blue;">{st.session_state.parte_nota}</span> 
        <span style="font-size: 35px; color: #666;">e</span> 
        <span style="color: #ff7f0e;">?</span>
    </div>
''', unsafe_allow_html=True)

st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

# 7. TASTIERA
opzioni = [str(i) for i in range(1, target)]
scelta_radio = st.radio(
    "TastieraNumerica", 
    options=opzioni, 
    index=None, 
    key=f"tastiera_{st.session_state.domanda_id}"
)

# 8. Risposta
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
        st.error(f"Riprova!")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)

# 9. AIUTO
st.markdown("---")
with st.expander("💡 Hai bisogno di un aiuto? Guarda gli amici del " + str(target)):
    for i in range(1, target):
        st.write(f"🧱 **{i}** e **{target-i}**")
