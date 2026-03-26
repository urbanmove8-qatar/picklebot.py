# 🥒 Picklebot.py

[![PyPI version](https://img.shields.io/pypi/v/picklebot.py.svg)](https://pypi.org/project/picklebot.py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Picklebot.py** is a modern, asynchronous API wrapper for [Picklechat.net](https://picklechat.net), designed to move away from clunky, "old school" Flask-based implementations.

## ✨ Features
* **Asynchronous:** Built on `aiohttp` for high-performance bot interactions.
* **Rate-Limit Aware:** Automatically handles the 100 req/min limit with smart backoff.
* **Type-Safe:** Uses Pydantic for robust data validation and IDE autocomplete.
* **Simple:** No more manual JSON parsing or raw HTTP requests.

## 🚀 Installation
```bash
pip install picklebot.py
```

## 🛠️ Quick Start
```python
import asyncio
from picklebot import Picklebot

async def main():
    # Initialize your bot
    bot = Picklebot(token="YOUR_BOT_TOKEN", bot_id="YOUR_BOT_ID")
    
    # Send a message
    response = await bot.send_message(
        room_id="room_123", 
        text="Hello from Picklebot.py! 🥒"
    )
    
    print(f"Sent message with ID: {response.messageId}")
    
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 📜 Legal
This is a community-led library and is not officially affiliated with PickleChat®. By using this library, you agree to abide by the [![Picklechat Developer Terms of Service.](https://picklechat.net/developer-tos)](https://picklechat.net/developer-tos).