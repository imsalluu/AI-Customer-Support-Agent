from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.customers import router as customers_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.tickets import router as tickets_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.products import router as products_router
from app.api.v1.orders import router as orders_router
from app.api.v1.agent_config import router as agent_config_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.channels import router as channels_router
from app.api.v1.billing import router as billing_router
from app.api.v1.chat_widget import router as widget_router
from app.api.v1.webhooks import router as webhooks_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(customers_router)
api_router.include_router(conversations_router)
api_router.include_router(tickets_router)
api_router.include_router(knowledge_router)
api_router.include_router(products_router)
api_router.include_router(orders_router)
api_router.include_router(agent_config_router)
api_router.include_router(analytics_router)
api_router.include_router(channels_router)
api_router.include_router(billing_router)
api_router.include_router(widget_router)
api_router.include_router(webhooks_router)
