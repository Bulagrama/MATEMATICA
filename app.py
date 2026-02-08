import streamlit as st
import random

# 1. Configurazione della pagina
st.set_page_config(page_title="Il Gioco dei Muretti", page_icon="🧱", layout="centered")

# 2. Stile CSS per rendere tutto grande e leggibile
st.markdown("""
    <style>
    .titolo { font-size: 50px !important; text-align: center; color: #FF4B4B; font-weight: bold; }
    .stButton>button { font-size: 30px !important; width: 100%; height: 60px; border-radius: 10px; }
    .mattoncino-testo { font-size: 60px; text-align: center; letter-spacing: 5px; }
    .info-testo { font-size: 25px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titolo">🧱 Il Gioco dei Muretti</p>', unsafe_allow_html=True)

# 3. Impostazioni del gioco nella sidebar
with st.sidebar:
    st.header("Impostazioni")
    target = st.number_input("Scegli il muretto del...", min_value=2, max_value=10, value=6)
    st.write("---")
    st.write("Questo gioco aiuta i bambini a trovare le coppie amiche dei numeri.")

# 4. Inizializzazione della sessione di gioco
if 'parte_nota' not in st.session_state or st.session_state.get('current_target') != target:
    st.session_state.parte_nota = random.randint(0, target)
    st.session_state.current_target = target
    st.session_state.indovinato = False

# 5. Area di gioco centrale
mancanti_reali = target - st.session_state.parte_nota

st.markdown(f'<p class="info-testo">Siamo nel muretto del <b>{target}</b></p>', unsafe_allow_html=True)
st.markdown(f'<p class="info-testo">Abbiamo già messo <b>{st.session_state.parte_nota}</b> mattoncini blu:</p>', unsafe_allow_html=True)

# Visualizzazione grafica dei mattoncini esistenti
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

st.markdown('<p class="info-testo">Quanti mattoncini arancioni 🟧 mancano per finire?</p>', unsafe_allow_html=True)

# 6. Bottoni per la risposta (Pulsantiera gigante)
col_bottone = st.columns(target + 1)
scelta = None

for i in range(target + 1):
    if col_bottone[i].button(str(i)):
        scelta = i

# 7. Verifica della risposta
if scelta is not None:
    if scelta == mancanti_reali:
        st.session_state.indovinato = True
    else:
        st.error(f"Oh no! Se aggiungi {scelta}, non arrivi a {target}. Riprova!")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)

# 8. Messaggio di vittoria e reset
if st.session_state.indovinato:
    st.balloons()
    st.success(f"BRAVISSIMO! {st.session_state.parte_nota} + {mancanti_reali} fa proprio {target}!")
    st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * mancanti_reali}</p>', unsafe_allow_html=True)
    
    if st.button("Fai un altro muretto! ➡️"):
        st.session_state.parte_nota = random.randint(0, target)
        st.session_state.indovinato = False
        st.rerun()

# 9. Riepilogo visivo (I muretti amici)
with st.expander("Vedi tutti i muretti del " + str(target)):
    for i in range(target + 1):
        st.write(f"{i} + {target-i} = {target} | {'🟦'*i}{'🟧'*(target-i)}")
