import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Il Gioco dei Muretti", page_icon="🧱", layout="centered")

# 2. CSS Avanzato per Mobile e Griglia Bottoni
st.markdown("""
    <style>
    .titolo { font-size: 35px !important; text-align: center; color: #FF4B4B; font-weight: bold; }
    
    /* Forza i bottoni a stare in griglia anche su cellulare */
    [data-testid="column"] {
        display: inline-block !important;
        width: 18% !important; /* Circa 5 bottoni per riga */
        min-width: 60px !important;
        margin: 5px !important;
    }
    
    .stButton>button { 
        font-size: 25px !important; 
        width: 100% !important; 
        height: 60px !important; 
        border-radius: 10px !important;
        background-color: #f0f2f6 !important;
        border: 2px solid #d1d1d1 !important;
    }

    .mattoncino-testo { font-size: 50px; text-align: center; letter-spacing: 3px; line-height: 1.1; }
    .info-testo { font-size: 22px; text-align: center; margin-top: 10px; }
    .evidenza { color: #1f77b4; font-weight: bold; font-size: 28px; }
    
    /* Nasconde i margini inutili su mobile */
    .main .block-container { padding: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titolo">🧱 Gioco dei Muretti</p>', unsafe_allow_html=True)

# 3. Impostazioni nella sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Muretto del numero:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])
    st.write("---")
    if st.button("🔄 Ricomincia"):
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

# 5. Logica e Visualizzazione
mancanti_reali = target - st.session_state.parte_nota

st.markdown(f'<p class="info-testo">Muretto del <span class="evidenza">{target}</span></p>', unsafe_allow_html=True)
st.markdown(f'<p class="info-testo">Hai <span class="evidenza">{st.session_state.parte_nota}</span> mattoncini blu:</p>', unsafe_allow_html=True)

st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)
st.markdown('<p class="info-testo">Quanti ne mancano? 🤔</p>', unsafe_allow_html=True)

# 6. Griglia di bottoni compatta
# Creiamo un numero sufficiente di colonne per farle andare a capo automaticamente
scelta = None
cols = st.columns(5) # Griglia fissa a 5 colonne per mobile
for i in range(1, target):
    # Usa l'operatore modulo per distribuire i bottoni nelle colonne
    if cols[(i-1) % 5].button(str(i), key=f"btn_{i}"):
        scelta = i

# 7. Risposta
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
    st.error(f"Sbagliato! {st.session_state.parte_nota} + {st.session_state.ultima_scelta_errata} non fa {target}")
    st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * st.session_state.ultima_scelta_errata}</p>', unsafe_allow_html=True)
