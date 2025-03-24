import argparse
import sys

import requests
from xyz.core import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_PROTOCOL,
    GREETING_ENDPOINT,
    configure_logging,
    get_logger,
)

# Set up logger for this module
logger = get_logger(__name__)


def get_greeting(
    name,
    host=DEFAULT_HOST,
    port=DEFAULT_PORT,
    protocol=DEFAULT_PROTOCOL,
    server_url=None,
):
    """Get a witty greeting from the server for the given name."""
    if server_url:
        url = f"{server_url}{GREETING_ENDPOINT.format(name=name)}"
        logger.info(f"Using custom server URL: {server_url}")
    else:
        url = f"{protocol}://{host}:{port}{GREETING_ENDPOINT.format(name=name)}"
        logger.info(f"Connecting to server at {protocol}://{host}:{port}")

    logger.debug(f"Making request to: {url}")

    try:
        response = requests.get(url, timeout=5)
        logger.debug(f"Response status code: {response.status_code}")
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        logger.debug(f"Response data: {data}")
        return data.get("greeting", f"Hello, {name}!")
    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to the server at {url.split('/greet')[0]}. Is it running?"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except requests.exceptions.Timeout:
        error_msg = f"Request timed out. The server at {url.split('/greet')[0]} is taking too long to respond."
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error occurred: {e}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except requests.exceptions.RequestException as e:
        error_msg = f"Request error occurred: {e}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Unexpected error occurred: {e}"
        logger.error(error_msg, exc_info=True)
        return f"Error: {error_msg}"


def main():
    parser = argparse.ArgumentParser(
        description="Get a witty greeting from the server."
    )
    parser.add_argument("name", nargs="?", default=None, help="Your name")
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Server hostname or IP (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Server port (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--protocol",
        default=DEFAULT_PROTOCOL,
        choices=["http", "https"],
        help=f"Protocol to use (default: {DEFAULT_PROTOCOL})",
    )
    parser.add_argument(
        "--server",
        "-s",
        default=None,
        help="Full server URL (overrides host, port, and protocol if provided)",
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

    if not args.name:
        parser.print_help()
        logger.error("No name provided")
        print("\nError: Please provide a name")
        sys.exit(1)

    logger.info(f"Getting greeting for user: {args.name}")

    greeting = get_greeting(
        args.name,
        host=args.host,
        port=args.port,
        protocol=args.protocol,
        server_url=args.server,
    )

    logger.info(f"Received greeting: {greeting}")
    print(greeting)


if __name__ == "__main__":
    main()
