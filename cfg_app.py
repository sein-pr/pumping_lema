import streamlit as st
from graphviz import Digraph
import tempfile
import os

# Function to generate strings in the language L(G) = { a^n b^n | n ≥ 0 }
def generate_strings(n):
    return ['a' * i + 'b' * i for i in range(n + 1)]

# Function to generate a parse tree using Graphviz
def draw_parse_tree(word):
    dot = Digraph(comment=f"Parse Tree for '{word}'")
    counter = [0]

    def add_node(parent, label):
        node_id = str(counter[0])
        dot.node(node_id, label)
        if parent is not None:
            dot.edge(parent, node_id)
        counter[0] += 1
        return node_id

    def build_tree(symbol, idx, parent):
        node = add_node(parent, symbol)
        if symbol == "S":
            if idx < len(word) and word[idx] == 'a':
                idx += 1
                build_tree("S", idx, node)
                if idx < len(word):
                    idx += 1
            else:
                add_node(node, 'ε')
        return idx

    build_tree("S", 0, None)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        dot.render(tmpfile.name, format='png', cleanup=True)
        return tmpfile.name + ".png"

# Streamlit app
def main():
    st.title("CFG Generator for L(G) = { aⁿ bⁿ | n ≥ 0 }")
    st.markdown("**Grammar:** S → aSb | ε")

    max_n = st.slider("Select maximum n (number of strings):", 0, 10, 3)
    strings = generate_strings(max_n)

    st.subheader("Generated Strings in L(G):")
    for i, s in enumerate(strings):
        st.write(f"w{i}: '{s}'")

    st.subheader("Parse Tree Viewer (Bonus Marks)")
    selected_string = st.selectbox("Choose a string to visualize:", strings)

    if st.button("Show Parse Tree"):
        img_path = draw_parse_tree(selected_string)
        if os.path.exists(img_path):
            st.image(img_path, caption=f"Parse Tree for '{selected_string}'", use_column_width=True)
        else:
            st.error("Could not generate parse tree.")

    st.info("Developed using Python + Streamlit + Graphviz")

if __name__ == "__main__":
    main()
