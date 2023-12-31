# -*- coding: utf-8 -*-
"""emplay.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MRGZ3T_xoyLbAs1EMYTe_3v6GIo-E8ia
"""

!pip install python-dotenv
!pip install openai

!pip install langchain[llms]

import os
import openai

from langchain.llms import OpenAI

llm = OpenAI(openai_api_key="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")

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key =  os.getenv('OPENAI_API_KEY')

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

!pip install pypdf

from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("/content/drive/MyDrive/demo.pdf")
pages = loader.load_and_split()

pages[0]

import pandas as pd

df=pd.DataFrame(pages,columns=['descr','employe'])
df.head()

len(pages)

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

from langchain.chains import SequentialChain

llm = ChatOpenAI(openai_api_key="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")

# prompt template 1: translate to english
first_prompt = ChatPromptTemplate.from_template(

    "Translate the following review to english:"
    "\n\n{descr}"


    )
# chain 1: input= Review and output= English_Review
chain_one = LLMChain(llm=llm, prompt=first_prompt,
                     output_key="English_Review"
                    )

second_prompt = ChatPromptTemplate.from_template(

    "Translate the following review to spanish:"
    "\n\n{descr}"

    )
# chain 1: input= Review and output= English_Review
chain_two = LLMChain(llm=llm, prompt=second_prompt,
                     output_key="spainesh_Review"
                    )

third_prompt = ChatPromptTemplate.from_template(
    "Can you summarize the following review in 1 sentence:"
    "\n\n{English_Review}"
)
# chain 2: input= English_Review and output= summary
chain_three = LLMChain(llm=llm, prompt=third_prompt,
                     output_key="summary"
                    )

fourth_prompt = ChatPromptTemplate.from_template(
    "Translate the name to raghul sharma:"
    "\n\n{descr}"
)
chain_four = LLMChain(llm=llm,prompt=fourth_prompt,
                      output_key="name"
                      )

overall_chain = SequentialChain(
    chains=[chain_one, chain_two, chain_three,chain_four],
    input_variables=["descr"],
    output_variables=["English_Review","spainesh_Review","summary","name"],
    verbose=True
)

review=df.descr[2]
overall_chain(review)