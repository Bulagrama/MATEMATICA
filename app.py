import streamlit as st
import random
import time
import streamlit.components.v1 as components

# 1. Configurazione della pagina
st.set_page_config(page_title="Muretti", page_icon="🧱", layout="centered")

# 2. CSS per l'interfaccia Streamlit
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
    st.session_state.scelta = None

if 'ultimo_metodo' not in st.session_state or st.session_state.ultimo_metodo != metodo:
    st.session_state.ultimo_metodo = metodo
    st.session_state.ordine_attuale = 1
    st.session_state.parte_nota = 1 if metodo == "Ordinato" else random.randint(1, target - 1)

mancanti_reali = target - st.session_state.parte_nota

# 5. UI PRINCIPALE
st.markdown(f'<div class="header-muretto">MURETTO DEL {target}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="operazione"><span style="color: blue;">{st.session_state.parte_nota}</span> <span style="font-size: 35px; color: #666;">e</span> <span style="color: #ff7f0e;">?</span></div>', unsafe_allow_html=True)
st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}</p>', unsafe_allow_html=True)

# 6. TASTIERA HTML GIGANTE (Iniezione di codice puro)
# Creiamo i bottoni come una stringa HTML
bottoni_html = ""
for i in range(1, target):
    bottoni_html += f'<button class="btn-gigante" onclick="sendValue({i})">{i}</button>'

html_code = f"""
<style>
    .container {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        padding: 10px;
    }}
    .btn-gigante {{
        width: 100px;
        height: 100px;
        font-size: 45px;
        font-weight: bold;
        color: #1f77b4;
        background-color: white;
        border: 4px solid #1f77b4;
        border-radius: 20px;
        box-shadow: 0px 6px 0px #1a5e8f;
        cursor: pointer;
    }}
    .btn-gigante:active {{
        box-shadow: 0px 2px 0px #1a5e8f;
        transform: translateY(4px);
    }}
</style>
<div class="container">
    {bottoni_html}
</div>
<script>
    function sendValue(value) {{
        // Invia il valore scelto a Python tramite l'URL
        window.parent.postMessage({{type: 'streamlit:set_component_value', value: value}}, '*');
    }}
</script>
"""

# Visualizziamo i bottoni e catturiamo la risposta
risposta_html = components.html(html_code, height=300)

# 7. LOGICA DI RISPOSTA (Simulata con un trucco di state per gestire l'input HTML)
# Dato che st.components.html è asincrono, usiamo un trucco:
scelta = risposta_html

if scelta:
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
        st.rerun()
    else:
        st.error("Riprova!")
        st.markdown(f'<p class="mattoncino-testo">{"🟦" * st.session_state.parte_nota}{"⬜" * scelta}</p>', unsafe_allow_html=True)
