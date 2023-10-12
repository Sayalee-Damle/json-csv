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
from json_csv_compare.backend.config import cfg 
from json_csv_compare.log_factory import logger

import csv
import difflib

def compare_csv_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        csv_reader1 = csv.reader(file1)
        csv_reader2 = csv.reader(file2)

        lines1 = list(csv_reader1)
        lines2 = list(csv_reader2)

        differ = difflib.Differ()
        missing_lines = []
        changed_lines = []
        new_lines = []

        f = True
        
        l = 1
        #while f == True:
            
        diff = list(differ.compare(lines1[l], lines2[l]))
        #print(diff)
        #if l == max(len(lines1)-1, len(lines2)-1):
            #f = False
        
        line_num = 0
        for line in diff:
            line_num += 1
            if line.startswith('  '):
                continue
            elif line.startswith('- '):
                missing_lines.append(line_num)
            elif line.startswith('+ '):
                new_lines.append(line_num)
            elif line.startswith('? '):
                changed_lines.append(line_num)

    print("Missing Lines:")
    for line_num in missing_lines:
        print(f"Line {line_num} from File 1: {','.join(lines1[line_num - 1])}")

    print("\nChanged Lines:")
    for line_num in changed_lines:
        print(f"Line {line_num} from File 1: {','.join(lines1[line_num - 1])}")
        print(f"Line {line_num} from File 2: {','.join(lines2[line_num - 1])}")

    print("\nNew Lines:")
    for line_num in new_lines:
        print(f"Line {line_num} from File 2: {','.join(lines2[line_num - 1])}")

    return missing_lines, new_lines, changed_lines

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
        prompt_factory(t.system_template_change_output_format,t.human_template_change_output_format),
        verbose=cfg.verbose_llm,
    )

if __name__ == "__main__":
    file1_path = r"C:/tmp/files/EmployeeData.csv"
    file2_path = r"C:/tmp/files/EmployeeData2.csv"
    compare_csv_files(file1_path, file2_path)
