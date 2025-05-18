import streamlit as st
import time
import json

# Custom CSS for animations and styling
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.grammar-box {
    border: 2px solid #4CAF50;
    border-radius: 5px;
    padding: 20px;
    margin: 10px 0;
    background-color: #E8F5E9;
    animation: fadeIn 1s ease-in;
}

.parse-tree {
    border: 2px solid #2196F3;
    border-radius: 5px;
    padding: 20px;
    margin: 10px 0;
    background-color: #E3F2FD;
    animation: fadeIn 1s ease-in;
}

.stAlert {
    animation: fadeIn 0.5s ease-in;
}

.input-highlight {
    background-color: #FFEB3B;
    padding: 2px 5px;
    border-radius: 3px;
    transition: background-color 0.3s;
}

.node-highlight {
    fill: #FFEB3B !important;
    stroke: #FFC107 !important;
    stroke-width: 3px !important;
}

</style>
""", unsafe_allow_html=True)

def generate_string(n):
    if n == 0:
        return "ε"
    return f"a{generate_string(n-1)}b"

def create_parse_tree(input_string):
    n = len(input_string)//2 if input_string != "ε" else 0
    steps = []
    input_chars = list(input_string.replace('ε', ''))
    char_index = 0

    def build_tree(parent_id, level, depth):
        nonlocal char_index
        node_id = f"S{level}_{depth}"
        steps.append({
            'type': 'node',
            'id': node_id,
            'label': 'S',
            'parent': parent_id,
            'input_index': None
        })
        
        if level == 0:
            epsilon_id = f"ε_{depth}"
            steps.append({
                'type': 'node',
                'id': epsilon_id,
                'label': 'ε',
                'parent': node_id,
                'input_index': None
            })
            return node_id
        
        # Process 'a'
        a_id = f"a{level}_{depth}"
        steps.append({
            'type': 'node',
            'id': a_id,
            'label': 'a',
            'parent': node_id,
            'input_index': char_index
        })
        char_index += 1
        
        # Process inner S
        s_child = build_tree(node_id, level-1, depth+1)
        
        # Process 'b'
        b_id = f"b{level}_{depth}"
        steps.append({
            'type': 'node',
            'id': b_id,
            'label': 'b',
            'parent': node_id,
            'input_index': char_index
        })
        char_index += 1
        
        return node_id

    build_tree(None, n, 0)
    return steps, input_chars

# Streamlit app
st.title("Context-Free Grammar for L(G) = { aⁿbⁿ | n ≥ 0 } 🌳")
st.markdown('<div class="grammar-box">', unsafe_allow_html=True)
st.header("Context-Free Grammar (CFG) 📜")
st.latex(r"S \rightarrow aSb \ | \ \varepsilon")
st.markdown('</div>', unsafe_allow_html=True)

# User input
n = st.sidebar.slider("Select value of n:", 0, 10, 0)

# Generate strings
strings = [generate_string(i) for i in range(n+1)]
st.markdown('<div class="grammar-box">', unsafe_allow_html=True)
st.header("Generated Strings 💬")
cols = st.columns(3)
for i, s in enumerate(strings):
    with cols[i%3]:
        st.markdown(f'<div class="st-emotion-cache-1kyxreq">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Parse tree visualization
if n > 0:
    st.markdown('<div class="parse-tree">', unsafe_allow_html=True)
    st.header("Parse Tree Visualization 🌴")
    selected_string = st.selectbox("Select string to visualize:", strings[1:])
    
    with st.spinner('Generating parse tree...'):
        time.sleep(0.5)
        steps, input_chars = create_parse_tree(selected_string)
        input_display = "".join(input_chars) if selected_string != "ε" else "ε"

        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .node circle {{ fill: #fff; stroke: steelblue; stroke-width: 2px; }}
                .node text {{ font: 14px sans-serif; user-select: none; }}
                .link {{ fill: none; stroke: #ccc; stroke-width: 1.5px; }}
                .hidden {{ opacity: 0; }}
            </style>
        </head>
        <body>
            <div id="input-display" style="margin-bottom: 20px; font-size: 18px;">
                Input: {' '.join([ `<span id="char-${i}">${ch}</span>` for i, ch in enumerate(input_chars)])}
            </div>
            <div id="tree-container"></div>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <script>
                const steps = {json.dumps(steps)};
                const inputChars = {json.dumps(input_chars)};
                const width = 1200;
                const height = 600;
                const duration = 800;

                const svg = d3.select("#tree-container")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .call(d3.zoom().on("zoom", (event) => {{
                        g.attr("transform", event.transform);
                    }}))
                    .append("g");

                const treeLayout = d3.tree().size([height, width - 160]);
                let nodes = [];
                let links = [];

                function updateTree() {{
                    const root = d3.stratify()
                        .id(d => d.id)
                        .parentId(d => d.parent)
                        (nodes);
                    
                    treeLayout(root);
                    
                    // Update links
                    const linkPaths = svg.selectAll(".link")
                        .data(root.links(), d => d.target.id);
                    
                    linkPaths.enter()
                        .append("path")
                        .attr("class", "link hidden")
                        .merge(linkPaths)
                        .attr("d", d3.linkHorizontal()
                            .x(d => d.y)
                            .y(d => d.x));
                    
                    // Update nodes
                    const nodeGroups = svg.selectAll(".node")
                        .data(root.descendants(), d => d.id);
                    
                    const newNodeGroups = nodeGroups.enter()
                        .append("g")
                        .attr("class", "node hidden")
                        .attr("transform", d => `translate(${d.y},${d.x})`);
                    
                    newNodeGroups.append("circle")
                        .attr("r", 16);
                    
                    newNodeGroups.append("text")
                        .attr("dy", 5)
                        .style("text-anchor", "middle")
                        .text(d => d.data.label);
                    
                    nodeGroups.merge(newNodeGroups)
                        .transition()
                        .duration(duration)
                        .attr("transform", d => `translate(${d.y},${d.x})`);
                }}

                function animateStep(index) {{
                    if (index >= steps.length) return;
                    
                    const step = steps[index];
                    nodes.push({{ 
                        id: step.id, 
                        parent: step.parent, 
                        label: step.label 
                    }});
                    
                    // Highlight input character
                    if (step.input_index !== null) {{
                        d3.selectAll("#input-display span")
                            .classed("input-highlight", false);
                        d3.select(`#char-${{step.input_index}}`)
                            .classed("input-highlight", true);
                    }}
                    
                    updateTree();
                    
                    // Animate node appearance
                    svg.selectAll(`#${{step.id}}`)
                        .classed("hidden", false)
                        .raise()
                        .select("circle")
                        .classed("node-highlight", true)
                        .transition()
                        .duration(duration)
                        .style("opacity", 1)
                        .on("end", () => {{
                            d3.select(`#${{step.id}} circle`)
                                .classed("node-highlight", false);
                            animateStep(index + 1);
                        }});
                }}

                // Initial empty tree
                updateTree();
                setTimeout(() => animateStep(0), 500);
            </script>
        </body>
        </html>
        """
        st.components.v1.html(html_code, height=650, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("Please select n > 0 in the sidebar to see parse tree visualization ⚠️")