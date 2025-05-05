import os
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto
from yuna import get_wallet_balance, BalanceRequest, BalanceResponse

agent = Agent()

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Solana-Balance-Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=30),
)

@proto.on_message(
    BalanceRequest, replies={BalanceResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: BalanceRequest):
    ctx.logger.info(f"Received wallet balance request for address: {msg.address}")
    try:
        balance = await get_wallet_balance(msg.address)
        ctx.logger.info(f"Successfully fetched wallet balance for {msg.address}")
        await ctx.send(sender, BalanceResponse(balance=balance))
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))

agent.include(proto, publish_manifest=True)

### Health check related code
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.
    For example, check if the agent can connect to the Solana RPC API.
    """
    try:
        import asyncio
        asyncio.run(get_wallet_balance("AtTjQKXo1CYTa2MuxPARtr382ZyhPU5YX4wMMpvaa1oy"))
        return True
    except Exception:
        return False

class HealthCheck(Model):
    pass

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

class AgentHealth(Model):
    agent_name: str
    status: HealthStatus

health_protocol = QuotaProtocol(
    storage_reference=agent.storage, name="HealthProtocol", version="0.1.0"
)

@health_protocol.on_message(HealthCheck, replies={AgentHealth})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    status = HealthStatus.UNHEALTHY
    try:
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name="Solana Balance Agent", status=status))

agent.include(health_protocol, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
