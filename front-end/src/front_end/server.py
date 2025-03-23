from fastapi import FastAPI
import random
import uvicorn
import argparse
from xyz.core import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    ROOT_ENDPOINT,
    GREETING_ENDPOINT,
)

app = FastAPI()

GREETINGS = [
    "Hello there, {}! You look particularly radiant today.",
    "Greetings, {}! Your digital presence brightens our server.",
    "Well, well, well, if it isn't the legendary {}!",
    "Welcome back, {}! We've missed your HTTP requests.",
    "Oh my, {}! What a pleasant surprise to see you in our API logs.",
    "{}, fancy meeting you here in this corner of the internet!",
    "Ahoy, {}! Ready to navigate the seas of our API together?",
    "Look who decided to send a GET request today - it's {}!",
    "The incomparable {} has graced us with their presence!",
    "A wild {} appears! *Server used greeting. It's super effective!*",
]


@app.get(ROOT_ENDPOINT)
async def root():
    return {
        "message": "Welcome to the Witty Greeter API! Try /greet/YourName to get a personalized greeting."
    }


@app.get(GREETING_ENDPOINT)
async def greet(name: str):
    greeting = random.choice(GREETINGS).format(name)
    return {"greeting": greeting}


def run():
    """Entry point for the application."""
    parser = argparse.ArgumentParser(description="Run the Witty Greeter API server.")
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Host IP to bind the server to (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to run the server on (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--no-reload", action="store_true", help="Disable auto-reload on code changes"
    )

    args = parser.parse_args()

    uvicorn.run(
        "front_end.server:app",
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
    )


if __name__ == "__main__":
    run()
