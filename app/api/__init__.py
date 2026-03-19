"""API routers."""

from app.api.architect import router as architect_router
from app.api.chains import router as chains_router
from app.api.chat import router as chat_router
from app.api.custom_templates import router as custom_templates_router
from app.api.evaluate import router as evaluate_router
from app.api.execute import router as execute_router
from app.api.feedback import router as feedback_router
from app.api.keys import router as keys_router
from app.api.license import router as license_router
from app.api.quality import router as quality_router
from app.api.templates import router as templates_router
from app.api.transform import router as transform_router

__all__ = [
    "architect_router",
    "chains_router",
    "chat_router",
    "custom_templates_router",
    "evaluate_router",
    "execute_router",
    "feedback_router",
    "keys_router",
    "license_router",
    "quality_router",
    "templates_router",
    "transform_router",
]
