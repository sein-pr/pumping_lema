import streamlit as st
import math
import random
import time

st.set_page_config(layout="wide")

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_decomposition(p, n):
    max_y = min(n, p - 1)
    max_y = max(1, max_y)  # Ensure minimum y-length of 1
    y_length = random.randint(1, max_y)
    max_x = n - y_length
    x_length = random.randint(0, max(0, max_x))
    z_length = p - x_length - y_length
    return x_length, y_length, z_length

def create_segment(text, color):
    return f'<span style="background-color: {color}; padding: 4px 8px; border-radius: 4px; margin: 2px; display: inline-block;">{text}</span>'

def animate_segments(parts, colors, animation_delay=0.05):
    html = """
    <div style="display: flex; gap: 2px; margin: 10px 0; flex-wrap: wrap;">
    """
    
    for i, (text, color) in enumerate(zip(parts, colors)):
        html += create_segment(text, color)
    html += "</div>"
    return html

# Inject global CSS
st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .segment-animate {
        animation: fadeIn 0.5s ease forwards;
        opacity: 0;
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        margin: 2px;
    }
    .segment {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        margin: 2px;
    }
    .formula {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

if 'decomposition' not in st.session_state:
    st.session_state.decomposition = None
if 'show_proof' not in st.session_state:
    st.session_state.show_proof = False
if 'k_value' not in st.session_state:
    st.session_state.k_value = 2

with st.sidebar:
    st.markdown("""
    <h2 style='color: #2c3e50;'>Group 3 Assignment 2</h2>
    <h3>Group Members</h3>
    <ol>
        <li>Muwana Sein</li>
        <li>Justino Iipumbu Herman David</li>
        <li>Kahimbi Sandrina Simulya</li>
        <li>Renathe Mwengere Kayunde</li>
        <li>Zianah Ningiree Tjitendero</li>
        <li>Laina Ndasilohenda Iileka</li>
    </ol>
    <div style='margin-top: 20px; text-align: center;'>
        <p><strong>Computer Theory</strong></p>
        <p>Dr Nalina Suresh</p>
        <p>&copy; 2025 UNAM, Group 3</p>
    </div>
    """, unsafe_allow_html=True)

st.title("Pumping Lemma Visualizer")
st.markdown("### Language: L = {a<sup>p</sup> | p is prime}", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
n = col1.number_input("Pumping length (n)", min_value=1, step=1)
p = col2.number_input("Prime number (≥ n)", min_value=2, step=1)
k = col3.number_input("Pumping factor (k)", min_value=0, value=2, step=1)

if st.button("Start Proof"):
    st.session_state.show_proof = False
    st.session_state.k_value = k  # Store the k value
    error = None
    if not is_prime(p):
        error = "Please enter a valid prime number"
    elif p < n:
        error = "Prime number must be ≥ pumping length"
    
    if error:
        st.error(error)
    else:
        try:
            st.session_state.decomposition = generate_decomposition(p, n)
            st.session_state.show_proof = True
        except ValueError as e:
            st.error(f"Invalid decomposition: {str(e)}")
        st.rerun()

if st.session_state.show_proof and st.session_state.decomposition:
    x_length, y_length, z_length = st.session_state.decomposition
    k = st.session_state.k_value  # Use the stored k value
    
    with st.expander("Step 1: Assume L is regular → Pumping Lemma applies", expanded=True):
        st.markdown(f"Assume L is regular, then Pumping Lemma applies with pumping length **{n}**")
        time.sleep(0.5)
        
    with st.expander("Step 2: Choose string s", expanded=True):
        st.markdown(f"Choose string s = a<sup>{p}</sup> (prime length)", unsafe_allow_html=True)
        parts = ['a'] * p
        colors = ['#3498db'] * p
        st.markdown(animate_segments(parts, colors), unsafe_allow_html=True)
        time.sleep(0.5)
    
    with st.expander("Step 3: Random Decomposition s = xyz", expanded=True):
        with st.spinner("Decomposing string..."):
            time.sleep(1)
            parts = ['a'] * x_length + ['a'] * y_length + ['a'] * z_length
            colors = ['#3498db'] * x_length + ['#e67e22'] * y_length + ['#2ecc71'] * z_length
            st.markdown(animate_segments(parts, colors), unsafe_allow_html=True)
            st.markdown(f"""
                - Randomly selected decomposition:
                - x: {x_length}a's (blue)
                - y: {y_length}a's (orange)
                - z: {z_length}a's (green)
            """)
            st.markdown(f"""
            <div class="formula">
                s = xyz = a<sup>{x_length}</sup> · a<sup>{y_length}</sup> · a<sup>{z_length}</sup>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)
    
    with st.expander("Step 4: Pump y", expanded=True):
        with st.spinner("Pumping y..."):
            time.sleep(1)
            pumped = ['a'] * x_length + ['a'] * (y_length * k) + ['a'] * z_length
            pumped_colors = ['#3498db'] * x_length + ['#e67e22'] * (y_length * k) + ['#2ecc71'] * z_length
            st.markdown(animate_segments(pumped, pumped_colors), unsafe_allow_html=True)
            st.markdown(f"""
            <div class="formula">
                xy<sup>{k}</sup>z = a<sup>{x_length}</sup> · (a<sup>{y_length}</sup>)<sup>{k}</sup> · a<sup>{z_length}</sup> = a<sup>{x_length + y_length*k + z_length}</sup>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)
    
    with st.expander("Step 5: Contradiction", expanded=True):
        with st.spinner("Analyzing results..."):
            time.sleep(1)
            new_length = x_length + y_length * k + z_length
            st.markdown(f"""
            Contradiction! Pumped string length ({new_length}) is composite:
            - {new_length} = {x_length} + {k}*{y_length} + {z_length} = {new_length}
            - {new_length} is {'prime' if is_prime(new_length) else 'not prime'} → L is {'regular' if is_prime(new_length) else 'not regular'}
            """)
            if not is_prime(new_length):
                st.balloons()