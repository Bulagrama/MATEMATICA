import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Sfida dei Muretti", page_icon="🏆", layout="centered")

# 2. CSS MIRATO (Inclusi i nuovi stili per i punti e la selezione)
st.markdown("""
    <style>
    .header-muretto { 
        background-color: #FF4B4B; color: white; padding: 15px; 
        border-radius: 15px; text-align: center; font-size: 30px !important; font-weight: bold;
    }
    .punti-box {
        background-color: #ffffff; border-radius: 15px; padding: 10px;
        text-align: center; font-size: 28px; font-weight: bold; color: #FFA500; 
        border: 3px solid #FFA500; margin-bottom: 15px;
    }
    .operazione { font-size: 55px; text-align: center; font-weight: bold; margin: 15px 0; }
    .mattoncino-testo { font-size: 60px; text-align: center; letter-spacing: 8px; line-height: 1; margin-bottom: 20px; }
    
    /* TASTIERA GIGANTE */
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] { display: none !important; }
    [data-testid="stMain"] div[data-testid="stRadio"] > div { display: flex !important; flex-direction: row !important; flex-wrap: wrap !important; justify-content: center !important; gap: 15px !important; }
    [data-testid="stMain"] div[data-testid="stRadio"] label { background-color: white !important; border: 4px solid #1f77b4 !important; border-radius: 15px !important; width: 95px !important; height: 95px !important; display: flex !important; align-items: center !important; justify-content: center !important; box-shadow: 0px 5px 0px #1a5e8f !important; padding: 0 !important; }
    [data-testid="stMain"] div[data-testid="stRadio"] label div[dir] { display: none !important; }
    [data-testid="stMain"] div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p { font-size: 45px !important; font-weight: bold !important; color: #1f77b4 !important; margin: 0 !important; }
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) { background-color: #1f77b4 !important; box-shadow: none !important; transform: translateY(4px) !important; }
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Impostazioni Avanzate
with st.sidebar:
    st.header("🏆 Area Sfida")
    numeri_scelti = st.multiselect(
        "Su quali muretti vuoi allenarti?",
        options=list(range(2, 11)),
        default=[6]
    )
    
    tipo_gioco = st.radio("Tipo di sfida:", ["Muretto Fisso", "Muretto a Sorpresa (Misto)"])
    st.info("Nella modalità 'Sorpresa', il muretto cambia a ogni domanda tra quelli scelti!")

# 4. Inizializzazione Session State
if 'punti' not in st.session_state: st.session_state.punti = 0
if 'domanda_id' not in st.session_state: st.session_state.domanda_id = 0
if 'target_corrente' not in st.session_state: st.session_state.target_corrente = numeri_scelti[0] if numeri_scelti else 6

# Controllo se l'utente ha svuotato la selezione
if not numeri_scelti:
    st.warning("Seleziona almeno un numero nella barra laterale!")
    st.stop()

# 5. Logica Cambio Muretto (Challenge o Misto)
if 'parte_nota' not in st.session_state or st.session_state.nuova_domanda:
    if tipo_gioco == "Muretto a Sorpresa (Misto)":
        st.session_state.target_corrente = random.choice(numeri_scelti)
    
    # Se ha fatto 10 punti in modalità fissa, passa al numero successivo
    if st.session_state.punti > 0 and st.session_state.punti % 10 == 0 and tipo_gioco == "Muretto Fisso":
        idx = (numeri_scelti.index(st.session_state.target_corrente) + 1) % len(numeri_scelti)
        st.session_state.target_corrente = numeri_scelti[idx]
        st.toast(f"LIVELLO SUPERATO! Passiamo al muretto del {st.session_state.target_corrente}", icon="🚀")

    st.session_state.parte_nota = random.randint(1, st.session_state.target_corrente - 1)
    st.session_state.nuova_domanda = False

target = st.session_state.target_corrente
mancanti_reali = target - st.session_state.parte_nota

# 6. UI Principale
st.markdown(f'<div class="punti-box">⭐ Punti: {st.session_state.punti} ⭐</div>', unsafe_allow_html=True)
st.markdown(f'<div class="header-muretto">MURETTO DEL {target}</div>', unsafe_allow_html=True)

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
scelta_radio = st.radio("Keypad", options=opzioni, index=None, key=f"k_{st.session_state.domanda_id}")

# 8. Gestione Risposta
if scelta_radio:
    scelta = int(scelta_radio)
    if scelta == mancanti_reali:
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta}</p>', unsafe_allow_html=True)
        st.session_state.punti += 1
        st.balloons()
        st.success(f"GRANDE! Hai guadagnato un punto!")
        time.sleep(2)
        st.session_state.domanda_id += 1
        st.session_state.nuova_domanda = True
        st.rerun()
    else:
        st.error(f"Riprova! {st.session_state.parte_nota} e {scelta} non fanno {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)
        # Opzionale: azzerare i punti se sbaglia
        # st.session_state.punti = 0

# 9. AIUTO
st.markdown("---")
with st.expander("💡 Guarda gli amici del " + str(target)):
    for i in range(1, target):
        st.write(f"🧱 **{i}** e **{target-i}**")
