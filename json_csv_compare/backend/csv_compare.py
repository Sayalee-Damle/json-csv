import filecmp
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

import csv
import difflib


async def compare_csv_files(file1_path, file2_path):
    with open(file1_path, "r") as file1, open(file2_path, "r") as file2:
        csv_reader1 = csv.reader(file1)
        csv_reader2 = csv.reader(file2)

        lines1 = list(csv_reader1)
        lines2 = list(csv_reader2)

        differ = difflib.Differ()
        missing_lines = []
        changed_lines = []
        new_lines = []

        f = True
        diff = {}
        l = 55
        print(lines1[l])
        print(lines2[l])
        print(lines1[l] != lines2[l])
        #print(len(lines2))
        return diff
        while l != max(len(lines1), len(lines2)):
            if lines1[l] != lines2[l]:
                diff['line_number'+str(l)] = (lines1[l], lines2[l])
            l+=1
    return diff


def prompt_factory(system_template, human_template):
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        template=system_template
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        template=human_template
    )
    messages = [system_message_prompt, human_message_prompt]
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    return chat_prompt


def chain_factory_python_load() -> LLMChain:
    return create_structured_output_chain(
        str,
        cfg.llm,
        prompt_factory(
            t.system_template_change_output_format,
            t.human_template_change_output_format,
        ),
        verbose=cfg.verbose_llm,
    )


async def format_to_table(changed_lines):
    chain = chain_factory_python_load()
    table = await chain.arun({"changed_lines": changed_lines})
    return table


if __name__ == "__main__":
    import asyncio

    file1_path = r"C:/tmp/CSVfiles/EmployeeData.csv"
    file2_path = r"C:/tmp/files/EmployeeData2.csv"
    changed_lines = asyncio.run(compare_csv_files(file1_path, file2_path))
    logger.info(changed_lines)
    #logger.info(asyncio.run(format_to_table(changed_lines)))
