from langchain.agents import AgentOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain_ollama import ChatOllama
from langchain import hub
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.tools import get_profile_url_tavily


def look_up(name:str)->str:
    llm = ChatOllama(
                model = "llama3",
                temperature = 0.8,
                num_predict = 256,
            )
    template = """
                given the full name {name_of_the_person} i want to get me a link  to their linkedin profile page your answers should only be a url 
                """
    
    manual_prompt_template = PromptTemplate(template=template, input_variables=['name_of_the_person'])

    tools_for_agent = [
        Tool(
            name = "get_linkedin_profile_url",
            func=get_profile_url_tavily,
            description="usefull for when you need to get the linked in page url "
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executer = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    result = agent_executer.invoke(input={"input":manual_prompt_template.format_prompt(name_of_the_person=name)})
    linked_in_profile = result['output']
    return linked_in_profile

print(look_up("Rakiz kamal QA software tester "))