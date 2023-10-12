from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from pathlib import Path
from langchain.schema.messages import HumanMessage
from langchain.chains.openai_functions import create_structured_output_chain

import json_csv_compare.backend.templates as t
from json_csv_compare.config import cfg 
from json_csv_compare.log_factory import logger

def prompt_factory(system_template, human_template):
    system_message_prompt = SystemMessagePromptTemplate.from_template(template= system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(template= human_template)
    messages = [system_message_prompt, human_message_prompt] 
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    return chat_prompt

def chain_factory_python_load() -> LLMChain:
    return create_structured_output_chain(
        str,
        cfg.llm,
        prompt_factory(t.system_template_converter,t.human_template_converter),
        verbose=cfg.verbose_llm,
    )

async def load_file(path: Path, path_save: Path):
    chain = chain_factory_python_load()
    loader = await chain.arun({'json': path, 'path': path_save})
    return python_executor(loader)

def python_executor(code):
    python_executor_dir = cfg.python_executor
    
    if not python_executor_dir.exists():
        python_executor_dir.mkdir(exist_ok=True, parents=True)

    executor_path = python_executor_dir / f"code_execution.py"
    with open(executor_path, 'w') as f:
        f.write(code)
    try:
        exec(open(executor_path).read())
        succesful_msg = "successful execution"
        logger.info(succesful_msg)
        return succesful_msg
    except:
        error_msg = "execution failed"
        logger.exception(error_msg)
        return error_msg



    
if __name__ == "__main__":
    import asyncio
    path = Path(f"C:/Users/Sayalee/Downloads/EmployeeData.json")
    load_csv = asyncio.run(load_file(path, cfg.path_csv / f'{path.stem}.csv'))
    logger.info(load_csv)
    #py_file = asyncio.run(python_executor(load_csv))
    #logger.info(py_file)