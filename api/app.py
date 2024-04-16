from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/get_data')
async def get_data():
        return {'body' : 'renderizar esse texto.'}

if __name__== '__main__': 
        uvicorn.run(app, host='0.0.0.0', port = 7777)