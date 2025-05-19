import streamlit as st
from graphviz import Digraph

def generate_cfg_string(n):
    """Generate the string for a^n b^n"""
    if n == 0:
        return 'ε'
    return 'a' * n + 'b' * n

def build_parse_tree(dot, parent_id, current_depth, max_depth):
    """Recursively build the parse tree using Graphviz"""
    if current_depth < max_depth:
        # Create nodes for a, S, and b
        a_id = f'{parent_id}a'
        s_id = f'{parent_id}S'
        b_id = f'{parent_id}b'
        
        dot.node(a_id, 'a')
        dot.node(s_id, 'S')
        dot.node(b_id, 'b')
        
        # Create edges
        dot.edge(parent_id, a_id)
        dot.edge(parent_id, s_id)
        dot.edge(parent_id, b_id)
        
        # Recurse on the new S node
        build_parse_tree(dot, s_id, current_depth + 1, max_depth)
    else:
        # Add epsilon node
        eps_id = f'{parent_id}ε'
        dot.node(eps_id, 'ε')
        dot.edge(parent_id, eps_id)

def create_parse_tree(n):
    """Create and return the parse tree visualization"""
    dot = Digraph(comment='Parse Tree')
    dot.node('S', 'S')
    
    if n == 0:
        dot.node('ε', 'ε')
        dot.edge('S', 'ε')
    else:
        build_parse_tree(dot, 'S', 0, n)
    
    return dot

def main():
    st.title("Context-Free Grammar for L(G) = {aⁿbⁿ | n ≥ 0}")
    
    st.markdown("""
    ### Context-Free Grammar (CFG)
    The CFG for L(G) = {aⁿbⁿ | n ≥ 0} is:
    ```
    S → aSb | ε
    ```
    """)
    
    # Get user input for maximum n
    max_n = st.number_input("Enter maximum value for n:", 
                          min_value=0, value=0, step=1,
                          help="Generates strings from w₀ to wₙ")
    
    # Generate language strings
    language = [generate_cfg_string(i) for i in range(max_n + 1)]
    st.subheader("Generated Language L(G)")
    st.write(language)
    
    # Parse tree visualization
    st.subheader("Parse Tree Visualization")
    selected_n = st.selectbox("Select n to visualize parse tree:", 
                            options=range(max_n + 1),
                            format_func=lambda x: f'n = {x} ({generate_cfg_string(x)})')
    
    if selected_n >= 0:
        dot = create_parse_tree(selected_n)
        st.graphviz_chart(dot.source)

if __name__ == "__main__":
    main()