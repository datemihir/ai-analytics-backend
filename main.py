from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import uvicorn
import os
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Your FastAPI backend is working!"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read the file contents into a DataFrame
        contents = await file.read()
        file_ext = file.filename.split(".")[-1]

        if file_ext.lower() == "csv":
            df = pd.read_csv(io.BytesIO(contents))
        elif file_ext.lower() in ["xlsx", "xls"]:
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return JSONResponse(status_code=400, content={"error": "Unsupported file type."})

        # Run basic analysis
        summary = df.describe(include="all").fillna("").to_dict()
        columns = df.columns.tolist()
        shape = df.shape

        result = {
            "filename": file.filename,
            "columns": columns,
            "shape": {"rows": shape[0], "columns": shape[1]},
            "summary": summary
        }

        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
