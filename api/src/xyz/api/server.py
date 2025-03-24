import argparse
import random

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from xyz.core import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    GREETING_ENDPOINT,
    ROOT_ENDPOINT,
    configure_logging,
    get_logger,
)

# Set up logger for this module
logger = get_logger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    logger.debug(f"Request headers: {request.headers}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


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
    logger.debug("Root endpoint accessed")
    return {
        "message": "Welcome to the Witty Greeter API! Try /greet/YourName to get a personalized greeting."
    }


@app.get(GREETING_ENDPOINT)
async def greet(name: str):
    logger.info(f"Greeting requested for: {name}")
    greeting = random.choice(GREETINGS).format(name)
    logger.debug(f"Generated greeting: {greeting}")
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
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="Log to the specified file",
    )

    args = parser.parse_args()

    # Configure logging based on arguments
    log_level = "DEBUG" if args.debug else "INFO"
    configure_logging(level=log_level, log_file=args.log_file)

    if args.debug:
        logger.debug("Debug logging enabled")

    logger.debug(f"Arguments: {args}")
    logger.info(f"Starting server on {args.host}:{args.port}")

    uvicorn.run(
        "xyz.api.server:app",
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
        log_level=log_level.lower(),
    )


if __name__ == "__main__":
    run()
