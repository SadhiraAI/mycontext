# Post-Launch Roadmap

Features to add after the initial production deployment.

---

## 1. Multi-Factor Authentication (MFA)

**Priority**: High (add within first month)

**Implementation plan**:
- Install `pyotp` for TOTP (Time-based One-Time Password) generation
- Add `mfa_secret` and `mfa_enabled` columns to the `User` model
- New endpoints:
  - `POST /api/auth/mfa/setup` -- generate secret + QR code URI
  - `POST /api/auth/mfa/verify` -- verify TOTP code and enable MFA
  - `POST /api/auth/mfa/disable` -- disable MFA (requires current code)
- Update login flow: if MFA enabled, return a partial token, then require
  `POST /api/auth/mfa/challenge` with TOTP code to get the full JWT
- Generate 10 recovery codes (bcrypt-hashed, stored in DB) for account recovery
- Frontend: QR code display (use `qrcode` npm package or inline SVG), code input screen

**Libraries**:
- Backend: `pyotp>=2.9.0`, `qrcode>=7.4`
- Frontend: built-in -- just display the QR image from backend

---

## 2. Payment Portal (Stripe)

**Priority**: Medium (add when ready to monetize)

**Implementation plan**:
- Create Stripe account at https://stripe.com (free until you process payments)
- Install `stripe>=8.0.0` Python SDK
- Pricing tiers:
  - **Free**: 40 free templates, basic features
  - **Pro** ($X/month): All 85 templates, chain orchestration, priority support
  - **Enterprise** (custom): Current license key system + team features
- New endpoints:
  - `POST /api/billing/create-checkout` -- create Stripe Checkout session
  - `POST /api/billing/webhook` -- Stripe webhook for payment events
  - `GET /api/billing/subscription` -- get current subscription status
  - `POST /api/billing/portal` -- create Stripe Customer Portal session
- Add `stripe_customer_id` and `subscription_tier` columns to User model
- Stripe Checkout handles the entire payment UI (PCI compliant, no card handling)
- Use Stripe webhooks to update subscription status in your DB

**Environment variables needed**:
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_PRO_MONTHLY=price_...
STRIPE_PRICE_PRO_YEARLY=price_...
```

---

## 3. Error Tracking (Sentry)

**Priority**: Medium

- Sign up at https://sentry.io (free tier: 5K events/month)
- Install `sentry-sdk[fastapi]`
- Add `SENTRY_DSN` env var
- Auto-captures unhandled exceptions with full stack traces
- Frontend: add `@sentry/react` for JS error tracking

---

## 4. Email Notifications

**Priority**: Low (add when user base grows)

- Use Resend (https://resend.com) -- free tier: 3K emails/month
- Welcome email on signup
- Password reset flow
- License activation confirmation
