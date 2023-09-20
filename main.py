import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import openai


template = """
    I want you to be a top American patent attorney, \
    and you have both engineering and legal doctor degrees. \
    Based on the following description and any material you can gather, \
    please draft the first claim for the {patent} with more than 500 words in the language of {language} for a {language} patent.  \
    Ensure that the {language} patent office examiner will not reject this new patent due to lack of novelty, inventiveness, or missing essential technical features. please double check.\
    Please think step by step and write down the Claim 1. Don't miss any essential technical features and don't include Chinese characters. \
    
    The description is as follows:{abstract} 
    
"""

template_2nd = """
    I want you to be an American patent attorney, and you have both engineering and legal doctor degrees. \
    Please redraft the following to be more complicated to have higher sucess rate for grant for an invention patent in the language of {language}, with more than 500 words. \:
    
    {first_response}

"""


prompt = PromptTemplate(
    input_variables=["patent", "language", "abstract"],
    template=template,
)

prompt_2nd = PromptTemplate(
    input_variables=["language","first_response"],
    template=template_2nd,
)

# OPENAI_API_KEY = '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'
# llm = OpenAI(temperature=.7, openai_api_key=OPENAI_API_KEY)

OPENAI_API_KEY = 'sk-IaWRzriZOsG34UszNXxHULWR73xYKLKqFXEWwpWhs1lkaOjx'
OPENAI_API_BASE = "https://api.fe8.cn/v1"

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)


st.set_page_config(page_title="Invention Village R&D", page_icon=":book:")
st.header(":orange[Invention Village] R&D Patent System :book: :book:", divider='rainbow')
st.write("  ")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
      > Note：
      >  
      > Many R&D engineers conduct research and development based on the traditional brainstorming method, spending a lot of energy, but still the results are not good. 
      > The current R&D assistance tool combines more than 10 years of senior patent lawyers' experiences and AI intelligence. 
      > 
      > Any further queries, please just drop me a line：<1047534116@qq.com>
    """)

with col2:
    st.image(image='fourpatents.jpg', width=300, caption='The patent system added the fuel of interest to the fire of genius')

st.markdown("## Enter Your Requirements:")

col1, col2 = st.columns(2)
with col1:
    option_patent = st.selectbox(
        'Which patent would you like?',
        ('Invention', 'Utility Model'))
    
with col2:
    option_language = st.selectbox(
        'Which language would you like?',
        ('American', 'British', 'French', 'German'))

def get_abstract():
    input_text = st.text_area(label="Abstract", label_visibility='collapsed', placeholder="Your technical idea...", key="input_text")
    return input_text

abstract_input = get_abstract()

if len(abstract_input.split(" ")) > 700:
    st.write("Please enter a shorter description. The maximum length is 700 words.")
    st.stop()


if st.button("Give me Patent ideas", type="primary"):
    if abstract_input:
        prompt_with_abstract = prompt.format(patent=option_patent, language=option_language, abstract=abstract_input)
        response_1st = llm(prompt_with_abstract)
        st.subheader("Claim 1:")
        st.info(response_1st)
        
        prompt_with_abstract_2nd = prompt_2nd.format(language=option_language, first_response=response_1st)
        response_2nd = llm(prompt_with_abstract_2nd)
        st.subheader("Extended Features:")
        st.info(response_2nd)
        
    else:
        st.write("Please enter a description. The maximum length is 700 words.")
        st.stop()


st.divider()

st.title("Patents Analysis around the World")    
st.image(image='patents.png', width=700, caption='Patents Granted')


# tab1, tab2, tab3 = st.tabs(["R&D from Title", "R&D from Description", "R&D from PDF"])

# with tab1:
#    st.header("R&D from Title")
#    col1, col2 = st.columns(2)
#    with col1:
#         tab_patent = st.selectbox(
#         'Which patent would you like?',
#         ('Invention', 'Utility Model'), key="tab_patent")
    
#    with col2:
#         tab_language = st.selectbox(
#         'Which language would you like?',
#         ('American', 'British', 'French', 'German'),key="tab_language")

#    def get_abstract():
#         tab_text = st.text_area(label="Abstract", label_visibility='collapsed', placeholder="Your technical idea...", key="tab_text")
#         return tab_text

#    tab_abstract = get_abstract()

#    if len(tab_abstract.split(" ")) > 700:
#         st.write("Please enter a shorter description. The maximum length is 700 words.")
#         st.stop()
    
#    if st.button("Give me R&D tips", type="primary", key="tab_button"):
#         if tab_abstract:
#             prompt_with_abstract = prompt.format(patent=tab_patent, language=tab_language, abstract=tab_abstract)
#             response_1st = llm(tab_abstract)
#             st.subheader("R&D tips:")
#             st.info(response_1st)
#             response = openai.Image.create(
#                 prompt=" {tab_abstract}, with back and white lines",
#                 n=1,
#                 size="512x512"
#             )
#             image_url = response['data'][0]['url']
#             st.image(image_url, width=700, caption='illustrated by AI')

#             print(image_url)
            
#             # prompt_with_abstract_2nd = prompt_2nd.format(language=tab_language, first_response=response_1st)
#             # response_2nd = llm(prompt_with_abstract_2nd)
#             # st.subheader("Claim 1:")
#             # st.info(response_2nd)
#         else:
#             st.write("Please enter a description. The maximum length is 700 words.")
#             st.stop()

# with tab2:
#    st.header("R&D from Description")
#    st.header("to be established")

# with tab3:
#    st.header("R&D from PDF")
#    uploaded_files = st.file_uploader("Choose a pdf file", accept_multiple_files=True)
#    for uploaded_file in uploaded_files:
#       bytes_data = uploaded_file.read()
#       st.write("filename:", uploaded_file.name)
#       st.write(bytes_data)



