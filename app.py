import streamlit as st

# -------------------- CIPHER FUNCTIONS --------------------
def rail_fence_encrypt(message):
    message = message.replace(" ", "")
    rail1 = []
    rail2 = []
    for i in range(len(message)):
        if i % 2 == 0:
            rail1.append(message[i])
        else:
            rail2.append(message[i])
    return ''.join(rail1 + rail2)

def row_transposition_encrypt(message, key_input):
    message = message.replace(" ", "")
    key = [int(k) for k in key_input]
    rows = len(key)
    cols = (len(message) + rows - 1) // rows
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    i = 0
    for r in range(rows):
        for c in range(cols):
            if i < len(message):
                grid[r][c] = message[i]
                i += 1
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
    encrypted = ''
    for idx, _ in key_order:
        for ch in grid[idx]:
            if ch:
                encrypted += ch
    return encrypted

# -------------------- PAGE STYLE --------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e1f5fe, #e8f5e9);
}
.title {
    font-size: 42px;
    color: #004d40;
    font-weight: bold;
}
.result-box {
    background-color: #ffffff;
    padding: 1em;
    border-radius: 10px;
    margin-top: 10px;
    border-left: 5px solid #00796b;
    font-size: 18px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------- UI TITLE --------------------
st.markdown('<div class="title">🔐 Cipher Encryptor</div>', unsafe_allow_html=True)
st.write("Encrypt your messages using classic cipher techniques in a stylish UI.")

# -------------------- INPUT FORM --------------------
with st.form("cipher_form"):
    message = st.text_input("✍️ Enter your message to encrypt:")
    cipher_type = st.radio("🔧 Choose cipher type:", ["Rail Fence Cipher", "Row Transposition Cipher"])

    key_input = ""
    if cipher_type == "Row Transposition Cipher":
        key_input = st.text_input("🔢 Enter numeric key (e.g., 431256):")

    submitted = st.form_submit_button("🚀 Encrypt")

# -------------------- ENCRYPTION LOGIC --------------------
if submitted:
    if not message.strip():
        st.error("⚠️ Please enter a message.")

    elif cipher_type == "Rail Fence Cipher":
        cipher = rail_fence_encrypt(message)
        with st.expander("📦 Encrypted Output"):
            st.markdown(f'<div class="result-box">🔐 <b>Encrypted (Rail Fence):</b><br>{cipher}</div>', unsafe_allow_html=True)

    elif cipher_type == "Row Transposition Cipher":
        if not key_input.strip().isdigit():
            st.error("❌ Key must contain only digits like 431256.")
        else:
            cipher = row_transposition_encrypt(message, key_input)
            with st.expander("📦 Encrypted Output"):
                st.markdown(f'<div class="result-box">🔐 <b>Encrypted (Row Transposition):</b><br>{cipher}</div>', unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("---")

