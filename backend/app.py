from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware



async def homepage(request):
    return JSONResponse({'hello': 'world'})

async def henlo(request):
    return JSONResponse({'hello': 'https://www.google.com/aclk?sa=l&ai=DChcSEwjV6LCpj7qAAxWhU38AHf4mAcQYABAFGgJvYQ&ase=2&sig=AOD64_1UiI8piHMFBpzrhNhgySdX-dbRJQ&ctype=5&nis=5&adurl&ved=2ahUKEwiqwqOpj7qAAxVVO94AHQ-LA0YQvhd6BQgBEIYB'})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/hi', henlo)
])


app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["http://localhost:3000"], allow_headers=["http://localhost:3000"], allow_methods=["*"]
)