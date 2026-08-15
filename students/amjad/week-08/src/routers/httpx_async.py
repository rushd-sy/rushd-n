import asyncio

from fastapi import APIRouter
import httpx

router = APIRouter()


@router.get("/with_async")
async def async_test() -> dict:
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get("https://api.github.com/repos/fastapi/fastapi")
            for _ in range(10)
        ]
        responses = await asyncio.gather(*tasks)
    return {"responses": [response.json() for response in responses]}


@router.get("/without_async")
async def without_async_test() -> dict:
    responses = []
    for _ in range(10):
        response = httpx.get("https://api.github.com/repos/fastapi/fastapi")
        responses.append(response)
    return {"responses": [response.json() for response in responses]}
