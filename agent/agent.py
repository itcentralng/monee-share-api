from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from agent.model import Command
from lib._openai import model
from templates.prompt_templates import (
    format_user_text_template,
)


def format_user_request(user_request: str) -> Command:

    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=Command)

    prompt = PromptTemplate(
        template=format_user_text_template,
        input_variables=["user_query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # And a user_query intended to prompt a language model to populate the data structure.
    prompt_and_model = prompt | model
    try:
        output = prompt_and_model.invoke({"user_query": user_request})
        response = parser.invoke(output)
    except Exception as error:
        print(error)
        response = {"error": "failed to parse user query"}
    return response
