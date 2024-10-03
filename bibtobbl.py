import streamlit as st
import os
import subprocess
from streamlit_ace import st_ace


def generate_bbl_page():
    st.title('ACES Reference structure and ordering.')  # 1. List available .bst files from the 'bst' folder

    # Ensure the 'bst' folder exists
    bst_folder = 'bst'
    if not os.path.exists(bst_folder):
        st.error(f"Folder '{bst_folder}' not found. Please create the folder and add .bst files.")
    else:
        bst_files = [f for f in os.listdir(bst_folder) if f.endswith('.bst')]
        if not bst_files:
            st.error("No .bst files found in the 'bst' folder.")
        else:
            selected_bst = st.selectbox('Choose a file', bst_files)

            # 2. Ace Editor to input .bib content
            st.subheader('Paste your Input:')
            bib_content = st_ace(language='latex', theme='github', height=200)

            # 3. Button to generate .bbl file
            if st.button('Generate References with Order'):
                if bib_content:
                    # Save the .bib content to a temporary .bib file
                    with open('temp.bib', 'w') as f:
                        f.write(bib_content)

                    # 4. Create a LaTeX file (testbib.tex) for processing the bibliography
                    tex_content = f"""
                    \\documentclass{{article}}

                    \\usepackage{{cite}}

                    \\begin{{document}}

                    pdflatex testbib.tex

                    \\cite{{*}}  % Citing all references
                    \\bibliographystyle{{bst/{selected_bst}}}
                    \\bibliography{{temp}}

                    \\end{{document}}
                    """

                    with open('testbib.tex', 'w') as tex_file:
                        tex_file.write(tex_content)

                    # 5. Run the necessary commands to generate the .bbl file
                    # 1st command: Run pdflatex
                    pdflatex_command = ['pdflatex', 'testbib']
                    bibtex_command = ['bibtex', 'testbib']

                    try:
                        subprocess.run(pdflatex_command, check=True)
                        subprocess.run(bibtex_command, check=True)

                        # 6. Read and display the generated .bbl file
                        with open('testbib.bbl', 'r') as bbl_file:
                            bbl_content = bbl_file.read()

                        # Show the .bbl content in markdown
                        st.subheader('Generated Output:')
                        st.markdown(f"```\n{bbl_content}\n```")
                    except subprocess.CalledProcessError as e:
                        st.error(f"An error occurred while running commands:\n{e}")
                else:
                    st.warning("Please paste BibTeX content before generating the .bbl file.")