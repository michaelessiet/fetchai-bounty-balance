# Solana Balance Agent

This agent gets the wallet balance of any Solana Wallet it is given. The agent is able to get the balance of SOL and any SPL token.

The agent makes use of Yuna under the hood, an all in one on-chain data aggregator that provides a simple API to get transaction history, token balances, and more.

The agent's address is `test-agent://agent1qt4ymxmpqmg04ru7akyrhxkw2cy2rncqkwpt4mfrkh6z4tmukezyv77xl04` and it's name is `Solana Balance Agent`.

### Setup

1. Add the `API_KEY` environment variable to your `.env` file. You can get an API key from [Yuna](https://yunaapi.com)

### Usage

You can use the agent by simply asking "what's the balance for `your_wallet_address_here`"

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
