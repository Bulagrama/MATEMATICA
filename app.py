import streamlit as st
import random
import time
import streamlit.components.v1 as components

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS per l'interfaccia generale
st.markdown("""
    <style>
    .header-muretto { 
        background-color: #FF4B4B; color: white; padding: 15px; 
        border-radius: 15px; text-align: center; font-size: 30px !important; font-weight: bold;
    }
    .operazione { font-size: 60px; text-align: center; font-weight: bold; margin: 15px 0; }
    .mattoncino-testo { font-size: 65px; text-align: center; letter-spacing: 8px; line-height: 1; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Impostazioni")
    target = st.number_input("Muretto del:", min_value=2, max_value=10, value=6)
    metodo = st.radio("Metodo:", ["Casuale", "Ordinato"])

# 4. Inizializzazione Sessione
if 'current_target' not in st.session_state or st.session_state.current_target != target:
    st.session_state.current_target = target
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

if 'ultimo_metodo' not in st.session_state or st.session_state.ultimo_metodo != metodo:
    st.session_state.ultimo_metodo = metodo
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

mancanti_reali = target - st.session_state.parte_nota

# 5. UI PRINCIPALE
st.markdown(f'<div class="header-muretto">IL MURETTO DEL {target}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="operazione"><span style="color: blue;">{st.session_state.parte_nota}</span> <span style="font-size: 35px; color: #666;">e</span> <span style="color: #ff7f0e;">?</span></div>', unsafe_allow_html=True)
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

# 6. TASTIERA HTML GIGANTE (Indipendente da Streamlit)
# Creiamo il codice HTML per i bottoni
bottoni_html = ""
for i in range(1, target):
    bottoni_html += f'<button class="btn-box" onclick="sendValue({i})">{i}</button>'

# Il componente HTML con Javascript per rimandare il valore a Python
html_component = f"""
<div id="container" class="container">
    {bottoni_html}
</div>

<style>
    .container {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        padding: 20px;
        font-family: sans-serif;
    }}
    .btn-box {{
        width: 120px;
        height: 120px;
        font-size: 55px;
        font-weight: bold;
        color: #1f77b4;
        background-color: white;
        border: 5px solid #1f77b4;
        border-radius: 20px;
        box-shadow: 0px 8px 0px #1a5e8f;
        cursor: pointer;
        transition: 0.1s;
    }}
    .btn-box:active {{
        box-shadow: 0px 2px 0px #1a5e8f;
        transform: translateY(6px);
    }}
</style>

<script>
    function sendValue(val) {{
        window.parent.postMessage({{
            type: 'streamlit:set_component_value',
            value: val
        }}, '*');
    }}
</script>
"""

# Visualizziamo i bottoni. L'altezza è fissa a 400 per assicurarci che si veda tutto su due righe
scelta = components.html(html_component, height=400)

# 7. LOGICA DI RISPOSTA
if scelta is not None:
    if scelta == mancanti_reali:
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"🟧" * scelta}</p>', unsafe_allow_html=True)
        st.balloons()
        st.success(f"BRAVO! {st.session_state.parte_nota} e {scelta} fanno {target}")
        
        time.sleep(2.5)
        # Aggiorna per la prossima domanda
        if metodo == "Casuale":
            st.session_state.parte_nota = random.randint(1, target - 1)
        else:
            st.session_state.ordine_attuale = (st.session_state.ordine_attuale % (target - 1)) + 1
            st.session_state.parte_nota = st.session_state.ordine_attuale
        st.rerun()
    else:
        st.error(f"Riprova! {st.session_state.parte_nota} e {scelta} non fanno {target}")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)
