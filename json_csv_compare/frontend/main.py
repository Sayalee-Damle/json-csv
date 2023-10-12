import chainlit as cl
from chainlit.types import AskFileResponse
from pathlib import Path
from langchain.schema import Document

from json_csv_compare.config import cfg
import json_csv_compare.backend.json_to_csv as jc
import json_csv_compare.backend.csv_compare as c


def write_to_disc_json(file) -> Path:
    path = cfg.path_json / f"{file.name}"
    with open(path, "wb") as f:
        f.write(file.content)
    return path


def write_to_disc_csv(file, path_json) -> Path:
    path = cfg.path_csv / f"{path_json.stem}-compare.csv"
    with open(path, "wb") as f:
        f.write(file.content)
    return path


async def delete_json(file):
    path = cfg.path_json / f"{file.name}"
    Path.unlink(path)


async def ask_user_msg(question) -> AskFileResponse:
    ans = None
    while ans == None:
        ans = await cl.AskUserMessage(
            content=f"{question}", timeout=cfg.ui_timeout
        ).send()
    return ans


@cl.on_chat_start
async def start() -> cl.Message:
    path_json = await get_json()
    path_csv = cfg.path_csv / f"{path_json.stem}.csv"
    if path_json:
        json_to_csv = await jc.load_file(path_json, path_csv)
        if json_to_csv == "successful execution":
            await cl.Message(content=f"File Created at {path_csv}").send()
        else:
            await cl.Message(content=f"Some error occured").send()
            return
        path_csv_2 = await get_csv(path_json)
        missing_lines, new_lines, changed_lines = await c.compare_csv_files(path_csv, path_csv_2)
        table = await c.format_to_table(missing_lines, new_lines, changed_lines)
        await cl.Message(content=table).send()
        await delete_json(path_json)
        return


async def get_json():
    files = None
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload an json file to begin!",
            accept=["application/json"],
            max_files=1,
        ).send()
    path_json = write_to_disc_json(files[0])
    return path_json


async def get_csv(path_json):
    files = None
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload an excel file to begin!",
            accept=["text/csv"],
            max_files=1,
        ).send()
    path_csv = write_to_disc_csv(files[0], path_json)
    return path_csv
