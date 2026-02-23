"""Email service using Resend for transactional emails."""

import logging

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"


async def send_verification_email(to_email: str, token: str) -> bool:
    """Send email verification link. Returns True on success."""
    settings = get_settings()

    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY not set — skipping verification email to %s", to_email)
        return False

    verify_url = f"{settings.frontend_url}/verify-email?token={token}"

    html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 480px; margin: 0 auto; padding: 2rem;">
      <h2 style="color: #1a1a2e;">Verify your email</h2>
      <p style="color: #555; line-height: 1.6;">
        Thanks for signing up for <strong>mycontext AI</strong>.
        Click the button below to verify your email address:
      </p>
      <a href="{verify_url}"
         style="display: inline-block; padding: 12px 28px; background: #38bda0;
                color: white; text-decoration: none; border-radius: 6px;
                font-weight: 600; margin: 1rem 0;">
        Verify Email
      </a>
      <p style="color: #888; font-size: 0.85rem; margin-top: 1.5rem;">
        If the button doesn't work, copy this link into your browser:<br/>
        <a href="{verify_url}" style="color: #38bda0; word-break: break-all;">{verify_url}</a>
      </p>
      <p style="color: #aaa; font-size: 0.78rem; margin-top: 2rem;">
        If you didn't sign up for mycontext AI, you can safely ignore this email.
      </p>
    </div>
    """

    payload = {
        "from": settings.email_from,
        "to": [to_email],
        "subject": "Verify your email — mycontext AI",
        "html": html,
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                RESEND_API_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {settings.resend_api_key}",
                    "Content-Type": "application/json",
                },
                timeout=10.0,
            )
        if resp.status_code in (200, 201):
            logger.info("Verification email sent to %s", to_email)
            return True
        logger.error("Resend API error %s: %s", resp.status_code, resp.text)
        return False
    except Exception:
        logger.exception("Failed to send verification email to %s", to_email)
        return False
