import os
import uvicorn
from fastapi import FastAPI, responses

import src.Utils as Utils
import src.DB as DB


DB.create_tables(drop_existing=eval(os.getenv("DROP_EXISTING_DB", True)))

app = FastAPI(
    **{
        "title": "THD(c)",
        "summary": f"Cryptocurrency trading training application DB manager",
        "version": "0.0.0",
        "openapi_tags": [
            {
                "name": "User",
                "description": "User account related endpoints",
            },
        ],
    }
)

Utils.OTEL.instrument_fastapi(app)


@app.get("/", response_class=responses.HTMLResponse)
async def base():
    """
    Default Page
    """
    return """
    <html>
        <head>
            <title>THD(c) API</title>
        </head>
        <body>
            <h1>THD(c) API is up and running!</h1>
        </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
