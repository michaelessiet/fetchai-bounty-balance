import json

def format_tokens_to_markdown(json_data):
    """
    Format token data from JSON into a Markdown document.

    Args:
        json_data (str or dict): JSON data containing token information

    Returns:
        str: Formatted Markdown string
    """
    # Parse JSON if it's a string
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    # Start building the Markdown document
    markdown = "# Token Holdings\n\n"

    # Check if tokens exist in the data
    if "tokens" not in data or not data["tokens"]:
        return markdown + "No tokens found."

    # Add a table header
    markdown += "| Token | Symbol | Balance | USD Value | Blockchain |\n"
    markdown += "|-------|--------|---------|-----------|------------|\n"

    # Add each token to the table
    for token in data["tokens"]:
        # Format the balance with appropriate precision
        balance = token.get("balance", 0)
        if isinstance(balance, (int, float)):
            if balance < 0.001 and balance > 0:
                balance_str = f"{balance:.8f}"
            else:
                balance_str = f"{balance:,.6f}".rstrip('0').rstrip('.') if '.' in f"{balance:,.6f}" else f"{balance:,.0f}"
        else:
            balance_str = str(balance)

        # Format USD value
        usd_value = token.get("usd", 0)
        usd_str = f"${usd_value:,.2f}" if isinstance(usd_value, (int, float)) else str(usd_value)

        # Add row to table
        markdown += f"| {token.get('currency', 'Unknown')} | {token.get('symbol', '-')} | {balance_str} | {usd_str} | {token.get('blockchain', '-').capitalize()} |\n"

    # Add detailed token information
    markdown += "\n## Token Details\n\n"

    for i, token in enumerate(data["tokens"]):
        markdown += f"### {i+1}. {token.get('currency', 'Unknown')} ({token.get('symbol', '-')})\n\n"
        markdown += f"- **Blockchain:** {token.get('blockchain', '-').capitalize()}\n"
        markdown += f"- **Contract Address:** `{token.get('address', '-')}`\n"
        markdown += f"- **Balance:** {balance_str} {token.get('symbol', '')}\n"
        markdown += f"- **USD Value:** {usd_str}\n"
        markdown += f"- **Decimals:** {token.get('decimals', '-')}\n"

        # Add token icon if available
        if "icon" in token and token["icon"]:
            markdown += f"- **Icon:** ![{token.get('symbol', 'Token')} Icon](https://{token['icon']})\n"

        markdown += "\n"

    return markdown

# Example usage:
# token_data = '''{"tokens":[{"address":"0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7","currency":"USDt","symbol":"USDT","balance":4.958888,"usd":4.96,"icon":"api.yunaapi.com/v1/assets/tokenassets?blockchain=avalanche&contractAddress=0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7","decimals":6,"blockchain":"solana"}]}'''
# markdown_output = format_tokens_to_markdown(token_data)
# print(markdown_output)
