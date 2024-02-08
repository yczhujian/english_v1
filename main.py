import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

st.set_page_config(page_title="Invention Village R&D", page_icon=":book:")
# st.header(":orange[Invention Village] R&D Patent System :book: :book:", divider='rainbow')
st.header(":orange[Invention Village] R&D Patent System :book: :book:")
st.write("  ")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
      > Note：
      >  
      > Many R&D engineers conduct research and development based on the traditional brainstorming method, spending a lot of energy, but still the results are not good. 
      > The current R&D assistance tool combines more than 10 years of senior patent lawyers' experiences and AI intelligence. 
      > 
      > Any further queries, please just drop me a line：<carrycenter@gmail.com>
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
        ('American', 'British', 'French', 'German', 'Chinese'))


chat = ChatOpenAI(openai_api_key="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", temperature=0, model="gpt-4")

template = """
    I want you to be a top American patent attorney, \
    and you have both engineering and legal doctor degrees. \
    Based on the following description and any material you can gather, \
    please draft the first claim with more than 200 words and less than 500 words for the {patent} in the language of {language} for a {language} patent.  \
    Ensure that the {language} patent office examiner will not reject this new patent due to lack of novelty, inventiveness, or missing essential technical features. please double check.\
    Please think step by step and write down the Claim 1 but don't indicate with the word "Claim", the wording should be concise enough and does not contain duplicate contents. Don't miss any essential technical features and the content should be complete, please double check. \
    
    ** example **
    A lateral shock absorber comprising:
    a protective fender pivoted to a base of a child car safety seat and pivotally switchable between a folded state and an unfolded state relative to the base; and\
    a locking mechanism for selectively engaging with the protective fender to restrain the protective fender from switching to the unfolded state or disengaging \
    from the protective fender to allow the protective fender to switch to the unfolded state when the protective fender is located in the folded state, \
    the locking mechanism comprising a locking assembly and an abutting block, the locking assembly being driven to a locking state for engaging with\
    the protective fender when the abutting block is pressed downwardly, and the locking assembly being driven to a releasing state for disengaging \
    from the protective fender when the abutting block is not pressed.
    
    ** example **
    The technical description is as follows:{abstract}
    
    
"""

template_2nd = """
    I want you to be a top R&D researcher. \
    Please proceed to draft extended 10 technical ideas with more inventive features to improve inventinveness of the patent as the example below with less than 500 words based on the following content in the language of {language}\:
    
    {first_response}
    
    
    Don't repeat any content in the {first_response} and the content should be complete, please think step by step and double check. \
    
    ** example **

    Further to the basic R&D idea, wherein:
    the locking mechanism further comprises an abutting component connected to the abutting block, and \
    the abutting component is driven by the abutting block to drive the locking assembly to the locking state for \
    engaging with the protective fender when the abutting block is pressed downwardly.

    Further to the basic R&D idea, wherein
    the locking mechanism further comprises a resilient component for driving the abutting component to drive the locking assembly \
    to the releasing state for disengaging from the protective fender when the abutting block is not pressed.
    
    Further to the basic R&D idea,, wherein
    the locking mechanism is a seesaw mechanism, and the resilient component is a torsional spring abutting against the abutting component \
    and the base and configured to drive an end of the abutting component near the locking assembly to pivot downwardly.
    ** example **
    
    Do not directly imitate the above example, just refer to the form of the example. The content you write needs to be based on the {abstract} and {first_response}, aiming to improve the patent non-obviousness of {first_response}. 

"""



template_3rd = """
    I want you to be an American patent attorney, and you have both engineering and legal doctor degrees. \
    Based on the the {first_response} and  {second_response}, please draft in {language} the technical effects and the problems solved by them against the prior art, so as to be used in the future patent application documents\
    to make this patent to have higher sucess rate for grant for an invention patent, with more than 500 words. :
    
"""

def get_abstract():
    input_text = st.text_area(label="Abstract", label_visibility='collapsed', placeholder="Your technical idea...", key="input_text")
    return input_text

abstract_input = get_abstract()

if len(abstract_input.split(" ")) > 700:
    st.write("Please enter a shorter description. The maximum length is 700 words.")
    st.stop()


# OPENAI_API_KEY = 'sk-IaWRzriZOsG34UszNXxHULWR73xYKLKqFXEWwpWhs1lkaOjx'
# OPENAI_API_BASE = "https://api.fe8.cn/v1"
# llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)


if st.button("Please give me R&D ideas", type="primary"):
    if abstract_input:
        prompt1 = ChatPromptTemplate.from_template(template=template)
        chain1 = prompt1 | chat | StrOutputParser()
        response1 = chain1.invoke({"patent":option_patent,"language":option_language,"abstract":abstract_input})
        st.subheader("Basic R&D idea:")
        st.info(response1)
        
        prompt2 = ChatPromptTemplate.from_template(template_2nd)
        chain2 = prompt2 | chat | StrOutputParser()
        response2 = chain2.invoke({"abstract":abstract_input, "first_response":response1, "language":option_language})
        st.subheader("Extended R&D ideas:")
        st.info(response2)
        
        prompt3 = ChatPromptTemplate.from_template(template_3rd)
        chain3 = prompt3 | chat | StrOutputParser()
        response3 = chain3.invoke({"first_response":"response1", "second_response":"response2", "language":"Chinese"})
        st.subheader("Problems Solved by this R&D activity:")
        st.info(response3)
    else:
        st.write("Please enter a description. The maximum length is 700 words.")
        st.stop()


st.divider()

st.title("Patents Analysis around the World")    
st.image(image='patents.png', width=700, caption='Patents Granted')


