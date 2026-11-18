# City Backend 
Define the logic for the agents. Using fastapi to comunicate to the frontend via websocket

## Requirments 

- uv package manager 
- python 3.13

## Instalation 
From the root of the backend run 
```bash
uv venv --python 3.13 
source .venv/bin/activate
uv sync
deactivate # this is to get out of the venv 
```
Now you could run all the other commands 

## Commands
> [!WARNING]
> You need to first run `chmod +x -R bin` to give execute permision to bash scripts

All commands are run from the root of the backend, from a terminal:
| Command               | Action                                           |
| :-------------------- | :----------------------------------------------- |
| `bin/dev`             | Start development server                         |
