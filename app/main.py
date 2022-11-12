import base64
import json

import pandas
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ExcelFile(BaseModel):
    file: bytes
    ext: str


@app.post("/files")
async def convert_excel_to_json(file: ExcelFile):
    spreadsheet = base64.b64decode(file.file)

    if file.ext == "xlsx":
        df = pandas.read_excel(spreadsheet, engine="openpyxl")  # type: ignore
    elif file.ext == "xls":
        df = pandas.read_excel(spreadsheet)  # type: ignore
    elif file.ext == "csv":
        df = pandas.read_csv(spreadsheet)  # type: ignore
    else:
        df = pandas.read_json(spreadsheet)  # type: ignore

    data = json.loads(df.to_json(orient="records"))  # type: ignore
    return data
