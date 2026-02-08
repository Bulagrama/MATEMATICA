import streamlit as st
import random
import time

# 1. Configurazione
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS PER BOTTONI E TESTO
st.markdown("""
    <style>
    .titolo { font-size: 38px !important; text-align: center; color: #FF4B4B; font-weight: bold; margin-bottom: 5px; }
    .info-testo { font-size: 24px; text-align: center; margin: 5px 0; }
    .operazione { font-size: 45px; text-align: center; font-weight: bold; color: #333; margin: 10px 0; background: #f9f9f9; border-radius: 15px; padding: 10px; }
    .mattoncino-testo { font-size: 55px; text-align: center; letter-spacing: 4px; line-height: 1.1; margin-bottom: 20px; }
    .evidenza { color: #1f77b4; font-weight: bold; }
    .mancante { color: #ff7f0e; border-bottom: 4px solid #ff7f0e; padding: 0 10px; }

    /* BOTTONI GIGANTI */
    div[data-testid="stSegmentedControl"] button {
        min-height: 85px !important;
        min-width: 65px !important;
        font-size: 32px !important;
        font-weight: bold !important;
        background-color: #f0f2f6 !important;
        border: 2px solid #1f77b4 !important;
    }
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
    }
    div[data-testid="stSegmentedControl"] label { display: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titolo">🧱 Gioco dei Muretti</p>', unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Muretto del numero:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])

# 4. Inizializzazione Sessione
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = random.randint(1, target - 1)
    st.session_state.indovinato = False

if 'ultimo_metodo' not in st.session_state or st.session_state.ultimo_metodo != metodo:
    st.session_state.ultimo_metodo = metodo
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

mancanti_reali = target - st.session_state.parte_nota

# 5. Visualizzazione Matematica e Grafica
st.markdown(f'<p class="info-testo">Stiamo studiando il muretto del <b>{target}</b></p>', unsafe_allow_html=True)

# Rappresentazione dell'operazione con il punto di domanda
st.markdown(f'''
    <div class="operazione">
        <span style="color: blue;">{st.session_state.parte_nota}</span> 
        + 
        <span style="color: #ff7f0e;">?</span> 
        = {target}
    </div>
''', unsafe_allow_html=True)

# Rappresentazione visiva con mattoncini
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

st.markdown('<p class="info-testo">Tocca il numero che manca: 🤔</p>', unsafe_allow_html=True)

# 6. Tastiera Gigante
scelta_fatta = st.segmented_control(
    label="Scegli",
    options=[i for i in range(1, target)],
    selection_mode="single",
    key="tastiera"
)

# 7. Gestione Risposta
if scelta_fatta:
    if scelta_fatta == mancanti_reali:
        # Mostra il muretto completo
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta_fatta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success(f"ECCELLENTE! {st.session_state.parte_nota} + {scelta_fatta} = {target}")
        
        time.sleep(2.5)
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
        st.rerun()
    else:
        st.error(f"Riprova! {st.session_state.parte_nota} + {scelta_fatta} non fa {target}")
        # Mostra l'errore visivo con i mattoncini bianchi
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta_fatta}</p>', unsafe_allow_html=True)

# 8. Riepilogo
with st.expander("Vedi tutti gli amici del " + str(target)):
    for i in range(1, target):
        st.write(f"**{i}** + **{target-i}** = **{target}**")
