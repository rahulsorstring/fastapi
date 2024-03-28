from fastapi import FastAPI,HTTPException
from pydantic import BaseModel  
from typing import List 

# Create a FastAPI application
app = FastAPI()

items = []
class Item(BaseModel):
    name: str
    description: str




# Define a route at the root web address ("/")
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/items/",response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# Update an item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    items[item_id] = item
    return item
# Delete an item
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = items.pop(item_id)
    return deleted_item

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application on the specified host and port
    uvicorn.run(app="main:app", host="127.0.0.1", reload=True, port=8000)

