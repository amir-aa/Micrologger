from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from typing import List

app = FastAPI()

@app.post("/append_string/{file_path}")
async def append_string(file_path: str, data: str):
    """
    Append a string to a file with the current datetime at the start.
    """
    try:
        with open(file_path, "a") as file:
            file.write(f"{datetime.now()} - {data}\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error appending to file: {str(e)}")

    return {"message":"String appended successfully"}


@app.get("/fetch_lines/{file_path}")
async def fetch_lines(
    file_path: str,
    start_time: datetime = Query(..., description="Start datetime"),
    end_time: datetime = Query(..., description="End datetime"),
) -> List[str]:
    """
    Fetch lines from a file between a start and end datetime.
    """
    try:
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file.readlines() if start_time <= get_datetime_from_line(line) <= end_time]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lines from file: {str(e)}")

    return lines

def get_datetime_from_line(line: str) -> datetime:
    """
    Extract datetime from a line in the format: "YYYY-MM-DD HH:MM:SS".
    """
    datetime_str = line.split(" - ")[0]
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
