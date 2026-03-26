import asyncio
import aiohttp
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class PickleError(Exception):
    """Base exception for Picklebot.py"""
    pass

class MessageResponse(BaseModel):
    success: bool
    messageId: str

class Picklebot:
    def __init__(self, token: str, bot_id: str):
        self.token = token
        self.bot_id = bot_id
        self.base_url = "https://api.picklechat.net"
        self.headers = {
            "Bot-Token": self.token,
            "Content-Type": "application/json"
        }
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self.headers)
        return self._session

    async def close(self):
        if self._session:
            await self._session.close()

    async def _request(self, method: str, endpoint: str, data: Any = None) -> Dict:
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"
        
        async with session.request(method, url, json=data) as response:
            # Handle Rate Limiting (Section 3.1 of TOS)
            if response.status == 429:
                # 2026 Standard: Exponential backoff or header-based wait
                retry_after = int(response.headers.get("Retry-After", 5))
                await asyncio.sleep(retry_after)
                return await self._request(method, endpoint, data)
            
            if response.status >= 400:
                error_text = await response.text()
                raise PickleError(f"API Error {response.status}: {error_text}")
                
            return await response.json()

    # --- Messaging ---
    async def send_message(self, room_id: str, text: str) -> MessageResponse:
        endpoint = f"/bots/{self.bot_id}/messages"
        payload = {"roomId": room_id, "text": text}
        data = await self._request("POST", endpoint, payload)
        return MessageResponse(**data)

    async def edit_message(self, message_id: str, room_id: str, text: str):
        endpoint = f"/bots/{self.bot_id}/messages/{message_id}"
        payload = {"roomId": room_id, "text": text}
        return await self._request("PATCH", endpoint, payload)

    async def delete_message(self, message_id: str, room_id: str):
        endpoint = f"/bots/{self.bot_id}/messages/{message_id}"
        payload = {"roomId": room_id}
        return await self._request("DELETE", endpoint, payload)

    # --- Commands ---
    async def register_command(self, name: str, description: str):
        endpoint = f"/bots/{self.bot_id}/commands"
        payload = {"name": name, "description": description}
        return await self._request("POST", endpoint, payload)

    # --- Buttons ---
    async def attach_buttons(self, message_id: str, room_id: str, buttons: List[Dict]):
        """
        Buttons list format: [{"id": "ok", "label": "✅ OK", "style": "success"}]
        """
        endpoint = f"/bots/{self.bot_id}/buttons"
        payload = {"messageId": message_id, "roomId": room_id, "buttons": buttons}
        return await self._request("POST", endpoint, payload)
