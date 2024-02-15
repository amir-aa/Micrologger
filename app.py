from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from typing import List
from cryptor import *
app = FastAPI()

@app.post("/append/{file_path}")
async def append_log(file_path: str, data: dict):
    """Append a log to a file with the current datetime at the start."""
    try:
        with open(file_path,"a+") as file:
            txt=data["data"]
            iv=""
            if "cipher" in data.keys():
                if  "rc4" in str(data["cipher"]).lower():
                    txt=rc4_encrypt(txt,str(data["key"]).encode()).hex()
                if str(data["cipher"]).lower()=="aes":
                    cipher=aes_encrypt(txt,str(data["key"]).encode())
                    txt=cipher[0].hex()
                    iv=cipher[1].hex()
                    

            file.write(f"{datetime.now()} - {txt}\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error appending to file: {str(e)}")
    if len(iv)>1:
        return{"message":"Log appended successfully","IV":iv}
    return {"message":"Log appended successfully"}


@app.get("/fetch_lines/{file_path}")
async def fetch_lines(
    file_path: str,
    start_time: datetime = Query(..., description="Start datetime"),
    end_time: datetime = Query(..., description="End datetime"),
) -> List[str]:
    """Fetch lines from a file between a start and end datetime."""
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
    return datetime.strptime(datetime_str,"%Y-%m-%d %H:%M:%S.%f")

@app.get("/decrypt/{algorithm}")
async def decr(algorithm:str,cipher:dict):
    if "rc4" in algorithm.lower():
        return {"decrypted": rc4_decrypt(bytes.fromhex(cipher["cipher"]),cipher["key"])}
    elif "aes" in algorithm.lower():
        return {"decrypted": aes_decrypt(bytes.fromhex(cipher["cipher"]),cipher["key"],bytes.fromhex(cipher["iv"]))}