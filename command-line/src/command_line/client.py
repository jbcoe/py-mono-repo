import argparse
import sys

import requests
from xyz.core import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_PROTOCOL, GREETING_ENDPOINT


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
    else:
        url = f"{protocol}://{host}:{port}{GREETING_ENDPOINT.format(name=name)}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        return data.get("greeting", f"Hello, {name}!")
    except requests.exceptions.ConnectionError:
        return f"Error: Could not connect to the server at {url.split('/greet')[0]}. Is it running?"
    except requests.exceptions.Timeout:
        return f"Error: Request timed out. The server at {url.split('/greet')[0]} is taking too long to respond."
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP error occurred: {e}"
    except requests.exceptions.RequestException as e:
        return f"Error: An error occurred: {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"


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

    args = parser.parse_args()

    if not args.name:
        parser.print_help()
        print("\nError: Please provide a name")
        sys.exit(1)

    greeting = get_greeting(
        args.name,
        host=args.host,
        port=args.port,
        protocol=args.protocol,
        server_url=args.server,
    )

    print(greeting)


if __name__ == "__main__":
    main()
