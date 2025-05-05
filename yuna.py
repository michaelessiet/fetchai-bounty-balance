import os
import logging
import requests
import json
from uagents import Model, Field
from utils import format_tokens_to_markdown

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.environ.get("API_KEY")

YUNA_BASE_URL = "https://api.yunaapi.com/v1"

# Set headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

class BalanceRequest(Model):
    address: str = Field(
        description="Solana wallet address to check",
    )

class BalanceResponse(Model):
    balance: str = Field(
        description="Formatted Solana wallet balance",
    )

async def get_wallet_balance(address: str) -> str:
    """
    Get the balance for a Solana address using the Yuna API

    Args:
        address: Solana wallet address

    Returns:
        Formatted balance string
    """
    try:
        logger.info(f"Getting balance for address: {address}")

        # Make the API request
        response = requests.get(f"{YUNA_BASE_URL}/balance?address={address}&blockchain=solana", headers=headers)
        response.raise_for_status()

        # Parse the response
        result = response.json()

        if "error" in result:
            error_msg = f"Error: {result['error']['message']}"
            logger.error(error_msg)
            return error_msg

        if len(result) != 0:
            return format_tokens_to_markdown(result)
        else:
            error_msg = "No balance found"
            logger.error(error_msg)
            return error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except json.JSONDecodeError as e:
        error_msg = f"JSON decode error: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return error_msg
