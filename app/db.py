import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

async def supabase_request(method: str, path: str, params=None, json=None):
    url = f"{SUPABASE_URL}/rest/v1/{path}"

    async with httpx.AsyncClient() as client:
        r = await client.request(
            method,
            url,
            headers=HEADERS,
            params=params,
            json=json
        )

        if r.status_code >= 400:
            raise Exception(f"{r.status_code}: {r.text}")

        if r.text:
            return r.json()

        return {}
