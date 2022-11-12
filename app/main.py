import base64
import json

import pandas
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

app = FastAPI()


class ExcelFile(BaseModel):
    file: bytes
    ext: str


@app.post("/files")
async def convert_excel_to_json(file: ExcelFile):
    spreadsheet = base64.b64decode(file.file)

    if file.ext == "xlsx":
        df = pandas.read_excel(spreadsheet, engine="openpyxl")
    elif file.ext == "xls":
        df = pandas.read_excel(spreadsheet)
    elif file.ext == "csv":
        df = pandas.read_csv(spreadsheet)
    else:
        df = pandas.read_json(spreadsheet)

    data = json.loads(df.to_json(orient="records"))
    return data
