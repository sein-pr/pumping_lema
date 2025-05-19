import streamlit as st
from nltk import CFG, ChartParser, Tree
from PIL import Image
import pydot
from io import BytesIO

# CFG for L(G) = { a^n b^n | n >= 0 }
def get_cfg():
    return CFG.fromstring("""
        S -> 'a' S 'b' | ''
    """)

def generate_string(depth):
    def expand(d):
        if d == 0:
            return ''
        return 'a' + expand(d - 1) + 'b'
    return expand(depth)

def generate_parse_tree(grammar, sentence):
    parser = ChartParser(grammar)
    try:
        trees = list(parser.parse(list(sentence)))
        return trees[0] if trees else None
    except:
        return None

def tree_to_image(tree: Tree):
    dot_string = tree._repr_dot_()
    graph = pydot.graph_from_dot_data(dot_string)[0]
    png_bytes = graph.create(format='png')
    image = Image.open(BytesIO(png_bytes))
    return image

def get_derivation_steps(tree: Tree):
    steps = []
    def expand(node: Tree):
        steps.append(tree.copy(deep=True))
        for child in node:
            if isinstance(child, Tree):
                expand(child)
    expand(tree)
    return steps

# Streamlit UI
st.set_page_config(page_title="CFG Visualizer", layout="centered")
st.title("Context-Free Grammar Visualizer: L(G) = { aⁿbⁿ | n ≥ 0 }")

st.markdown("""
### Grammar:
```
S -> a S b | ε
```
This grammar generates strings like ε, ab, aabb, aaabbb, etc.
""")

n = st.slider("Select n for aⁿbⁿ", min_value=0, max_value=10, value=2)

cfg = get_cfg()
string = generate_string(n)
st.write(f"**Generated string:** `{string or 'ε'}`")

if st.button("Show Parse Tree"):
    tree = generate_parse_tree(cfg, string)
    if tree:
        img = tree_to_image(tree)
        st.image(img, caption="Parse Tree")
    else:
        st.error("Unable to generate parse tree.")

if st.button("Animate Parse Tree"):
    tree = generate_parse_tree(cfg, string)
    if tree:
        steps = get_derivation_steps(tree)
        for step in steps:
            img = tree_to_image(step)
            st.image(img)
            st.sleep(1)
    else:
        st.error("Unable to animate parse tree.")
