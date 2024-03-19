from fastapi import FastAPI,HTTPException
from pydantic import BaseModel  
from typing import List 

# Create a FastAPI application
app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    publication_year: int
    ISBN: str
# Define a route at the root web address ("/")
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}




if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application on the specified host and port
    uvicorn.run(app, host="127.0.0.1", port=8000)