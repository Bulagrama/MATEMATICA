import streamlit as st

# Configurazione pagina
st.set_page_config(page_title="Il Muretto dei Numeri", page_icon="🧱")

st.title("🧱 Impara i Muretti dei Numeri")
st.write("Scegli un numero e scopri tutte le combinazioni (i mattoncini) che lo compongono!")

# Sidebar per la selezione
target = st.sidebar.number_input("Quale muretto vuoi studiare?", min_value=1, max_value=20, value=6)

st.header(f"Il Muretto del {target}")

# Logica per generare le coppie
coppie = []
for i in range(1, target):
    coppie.append((i, target - i))

# Visualizzazione interattiva
cols = st.columns(len(coppie))

for idx, (a, b) in enumerate(coppie):
    with cols[idx % 3]: # Organizza in colonne per non allungare troppo la pagina
        st.info(f"**{a}** + **{b}**")
        # Rappresentazione visiva con "mattoncini" (emoji)
        st.text("🧱" * a)
        st.text("🧱" * b)
        st.divider()

# Area Pratica
st.sidebar.markdown("---")
st.sidebar.subheader("Mettiti alla prova!")
test_val = st.sidebar.number_input(f"Se ho {target}, e una parte è 2, l'altra è...", value=0)

if test_val == (target - 2):
    st.sidebar.success("Corretto! 🎉")
elif test_val != 0:
    st.sidebar.error("Riprova! 🧐")
