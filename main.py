from fastapi import FastAPI, Request, Form, Depends, HTTPException, Response,WebSocket, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from databases import Database
from sqlalchemy import MetaData, Table, Column, Integer, String
from db import db_config
import MySQLdb
from typing import List
app = FastAPI()


# Define templates and static files directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_notes(request: Request):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()

    # Fetch all notes from the database
    cursor.execute("SELECT * FROM notes")
    notes_list = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return templates.TemplateResponse("index.html", {"request": request, "notes": notes_list})


@app.post("/create/")
async def create_note(title: str = Form(...), description: str = Form(...)):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()

    # Insert a new note into the database
    cursor.execute("INSERT INTO notes (title, description) VALUES (%s, %s)", (title, description))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return {"message": "Note created successfully"}


@app.get("/detail/{note_id}")
async def read_note_detail(request: Request, note_id: int):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()

    # Fetch the specified note from the database
    cursor.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
    note = cursor.fetchone()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return templates.TemplateResponse("detail.html", {"request": request, "note": note})


@app.post("/update/{note_id}")
async def update_note(note_id: int, title: str = Form(None), description: str = Form(None)):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()

    # Update the specified note in the database
    cursor.execute("UPDATE notes SET title = %s, description = %s WHERE id = %s", (title, description, note_id))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return {"message": "Note updated successfully"}


@app.post("/delete/{note_id}")
async def delete_note(note_id: int):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()

    # Delete the specified note from the database
    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return {"message": "Note deleted successfully"}

@app.get("/indexchat/")
async def chat(request:Request):
    return templates.TemplateResponse("chatindex.html",{'request':request})


class ConnectionManager:
    #initialize list for websockets connections
    def __init__(self):
        self.active_connections: List[WebSocket] = []
 
    #accept and append the connection to the list
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
 
    #remove the connection from list
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
 
    #send personal message to the connection
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
         
    #send message to the list of connections
    async def broadcast(self, message: str, websocket: WebSocket):
        for connection in self.active_connections:
            if(connection == websocket):
                continue
            await connection.send_text(message)
            
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    #accept connections 
    await connectionmanager.connect(websocket)
    try:
        while True:
            #receive text from the user
            data = await websocket.receive_text()
            await connectionmanager.send_personal_message(f"You : {data}", websocket)
            #broadcast message to the connected user
            await connectionmanager.broadcast(f"Client #{client_id}: {data}", websocket)
             
    #WebSocketDisconnect exception will be raised when client is disconnected
    except WebSocketDisconnect:
        connectionmanager.disconnect(websocket)
        await connectionmanager.broadcast(f"Client #{client_id} left the chat")
# instance for hndling and dealing with the websocket connections
connectionmanager = ConnectionManager()
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application on the specified host and port
    uvicorn.run(app="main:app", host="127.0.0.1", reload=True, port=8001)

