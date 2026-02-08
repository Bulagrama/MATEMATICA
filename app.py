import streamlit as st
import random
import time

# 1. Configurazione della pagina
st.set_page_config(page_title="Il Gioco dei Muretti", page_icon="🧱", layout="centered")

# 2. Stile CSS per rendere tutto grande e accessibile
st.markdown("""
    <style>
    .titolo { font-size: 50px !important; text-align: center; color: #FF4B4B; font-weight: bold; margin-bottom: 10px; }
    .stButton>button { font-size: 30px !important; width: 100%; height: 60px; border-radius: 15px; background-color: #f0f2f6; }
    .mattoncino-testo { font-size: 70px; text-align: center; letter-spacing: 5px; line-height: 1.2; }
    .info-testo { font-size: 28px; text-align: center; margin-top: 10px; }
    .evidenza { color: #1f77b4; font-weight: bold; font-size: 35px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titolo">🧱 Il Gioco dei Muretti</p>', unsafe_allow_html=True)

# 3. Impostazioni nella sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    # Il muretto minimo è il 2 (1+1)
    target = st.number_input("Muretto del numero:", min_value=2, max_value=10, value=6)
    st.write("---")
    st.write("💡 In questa modalità lo zero non è presente.")

# 4. Inizializzazione della sessione
# Cambiato il range per escludere lo zero: parte_nota va da 1 a target-1
if 'parte_nota' not in st.session_state or st.session_state.get('current_target') != target:
    st.session_state.parte_nota = random.randint(1, target - 1)
    st.session_state.current_target = target
    st.session_state.messaggio_errore = False
    st.session_state.ultima_scelta_errata = None
    st.session_state.indovinato = False

# 5. Logica di gioco
mancanti_reali = target - st.session_state.parte_nota

st.markdown(f'<p class="info-testo">Siamo nel muretto del <span class="evidenza">{target}</span></p>', unsafe_allow_html=True)
st.markdown(f'<p class="info-testo">Abbiamo <span class="evidenza">{st.session_state.parte_nota}</span> mattoncini blu:</p>', unsafe_allow_html=True)

# Visualizzazione dei mattoncini attuali
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

st.markdown(f'<p class="info-testo">Quanti ne mancano per arrivare a <b>{target}</b>?</p>', unsafe_allow_html=True)

# 6. Pulsantiera numerica (Parte da 1)
# Creiamo colonne solo per i numeri da 1 a target-1
cols = st.columns(target) # target colonne per ospitare comodamente i bottoni
scelta = None
for i in range(1, target):
    if cols[i-1].button(str(i), key=f"btn_{i}"):
        scelta = i

# 7. Gestione Risposta
if scelta is not None:
    if scelta == mancanti_reali:
        st.session_state.indovinato = True
        st.session_state.messaggio_errore = False
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success(f"BRAVISSIMO! {st.session_state.parte_nota} + {scelta} = {target}")
        
        time.sleep(3) 
        # Nuovo muretto senza zero
        st.session_state.parte_nota = random.randint(1, target - 1)
        st.session_state.indovinato = False
        st.rerun()
    else:
        st.session_state.messaggio_errore = True
        st.session_state.ultima_scelta_errata = scelta
        st.session_state.indovinato = False

# Messaggio di errore
if st.session_state.messaggio_errore and not st.session_state.indovinato:
    st.error(f"Riprova! Se ne aggiungi {st.session_state.ultima_scelta_errata} non arrivi a {target}.")
    st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * st.session_state.ultima_scelta_errata}</p>', unsafe_allow_html=True)

# 8. Tabella di aiuto (Senza lo zero)
with st.expander("Aiuto: guarda i muretti del " + str(target)):
    for i in range(1, target):
        st.write(f"{i} + {target-i} = {target} | {'🟦'*i}{'🟧'*(target-i)}")
