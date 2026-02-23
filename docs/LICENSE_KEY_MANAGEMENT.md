# License Key Management Guide

> mycontext AI — Enterprise License Keys

---

## Table of Contents

1. [How Licensing Works](#1-how-licensing-works)
2. [Key Format](#2-key-format)
3. [Database Schema](#3-database-schema)
4. [Production — Generate & Manage Keys](#4-production--generate--manage-keys)
5. [Local Development — Generate & Manage Keys](#5-local-development--generate--manage-keys)
6. [User Activation Flow](#6-user-activation-flow)
7. [Admin Operations](#7-admin-operations)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. How Licensing Works

mycontext AI has two tiers:

| Tier | Patterns | Price | How activated |
|------|----------|-------|---------------|
| **Free** | 16 cognitive patterns | $0 | Default for all signups |
| **Enterprise** | All 85 cognitive patterns | Paid | User enters a license key in Settings |

The flow:

```
Admin generates key in database
         │
         ▼
Admin sends key to customer (email, invoice, etc.)
         │
         ▼
Customer logs into mycontext AI
         │
         ▼
Settings → License → pastes key → clicks "Activate"
         │
         ▼
Backend validates key → marks key as redeemed → upgrades user
         │
         ▼
User now sees all 85 patterns (enterprise_license = true)
```

Each key can only be redeemed **once** by **one user**.

---

## 2. Key Format

```
MC-ENT-A3F8B1C9D2E74F0681B2C5D8A1E3F7B9
```

- Prefix: `MC-ENT-` (MyContext Enterprise)
- Body: 32 uppercase hex characters (128-bit cryptographically random)
- Generated with: `secrets.token_hex(16)` (Python) or `encode(gen_random_bytes(16), 'hex')` (PostgreSQL)

---

## 3. Database Schema

### `license_keys` table

| Column | Type | Description |
|--------|------|-------------|
| `id` | CHAR(36) | UUID primary key |
| `key` | VARCHAR(64) | The license key string (unique, indexed) |
| `label` | VARCHAR(255) | Admin label (e.g., customer name) — nullable |
| `is_valid` | BOOLEAN | `true` = active, `false` = revoked |
| `redeemed_by` | CHAR(36) | FK to `users.id` — filled when activated |
| `created_at` | TIMESTAMP | When the key was generated |
| `redeemed_at` | TIMESTAMP | When the key was activated — nullable |

### `users` table (relevant field)

| Column | Type | Description |
|--------|------|-------------|
| `enterprise_license` | BOOLEAN | `true` if user has enterprise access |

When a key is activated, **both** tables are updated: the key is marked as redeemed, and the user's `enterprise_license` flag is set to `true`.

---

## 4. Production — Generate & Manage Keys

Production uses **Neon PostgreSQL**. All operations are done via the Neon SQL Editor.

**Dashboard:** https://console.neon.tech → select your database → SQL Editor

### Generate a single key

```sql
INSERT INTO license_keys (id, key, label, is_valid, created_at)
VALUES (
  gen_random_uuid()::text,
  'MC-ENT-' || upper(encode(gen_random_bytes(16), 'hex')),
  'customer-name',
  true,
  now()
);
```

### Generate multiple keys at once

```sql
-- Generate 10 unassigned keys
INSERT INTO license_keys (id, key, label, is_valid, created_at)
SELECT
  gen_random_uuid()::text,
  'MC-ENT-' || upper(encode(gen_random_bytes(16), 'hex')),
  'unassigned',
  true,
  now()
FROM generate_series(1, 10);
```

### View all keys

```sql
SELECT key, label, is_valid,
       CASE
         WHEN redeemed_by IS NOT NULL THEN 'REDEEMED'
         WHEN NOT is_valid THEN 'REVOKED'
         ELSE 'AVAILABLE'
       END AS status,
       redeemed_by, created_at, redeemed_at
FROM license_keys
ORDER BY created_at DESC;
```

### View only available (unredeemed) keys

```sql
SELECT key, label, created_at
FROM license_keys
WHERE redeemed_by IS NULL AND is_valid = true
ORDER BY created_at;
```

### View redeemed keys with user emails

```sql
SELECT lk.key, lk.label, u.email, lk.redeemed_at
FROM license_keys lk
JOIN users u ON u.id = lk.redeemed_by
WHERE lk.redeemed_by IS NOT NULL
ORDER BY lk.redeemed_at DESC;
```

### Label a key for a customer

```sql
UPDATE license_keys
SET label = 'acme-corp'
WHERE key = 'MC-ENT-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX';
```

### Revoke a key

```sql
UPDATE license_keys
SET is_valid = false
WHERE key = 'MC-ENT-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX';
```

Note: Revoking a key does **not** automatically downgrade the user. To also remove enterprise access:

```sql
-- Revoke the key
UPDATE license_keys SET is_valid = false
WHERE key = 'MC-ENT-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX';

-- Downgrade the user who redeemed it
UPDATE users SET enterprise_license = false
WHERE id = (
  SELECT redeemed_by FROM license_keys
  WHERE key = 'MC-ENT-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
);
```

### Grant enterprise directly (no key needed)

Useful for your own account or special cases:

```sql
UPDATE users SET enterprise_license = true
WHERE email = 'your-email@example.com';
```

### Check total key statistics

```sql
SELECT
  count(*) AS total_keys,
  count(*) FILTER (WHERE redeemed_by IS NULL AND is_valid) AS available,
  count(*) FILTER (WHERE redeemed_by IS NOT NULL) AS redeemed,
  count(*) FILTER (WHERE NOT is_valid) AS revoked
FROM license_keys;
```

---

## 5. Local Development — Generate & Manage Keys

Local development uses **SQLite** (`mycontext.db` in the project root).

### Using the CLI script

```bash
cd C:\Users\dpokh\Desktop\mycontext

# Generate 1 key
python scripts/manage_licenses.py generate --label "dev-test"

# Generate 5 keys
python scripts/manage_licenses.py generate --count 5 --label "batch-test"

# List all keys and their status
python scripts/manage_licenses.py list

# Revoke a key
python scripts/manage_licenses.py revoke MC-ENT-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Grant enterprise directly by email (no key needed)
python scripts/manage_licenses.py grant-email your-email@example.com
```

### Important

- Local keys only exist in your local `mycontext.db` SQLite file
- They **cannot** be used on the production site (`mycontext.sadhiraai.com`)
- Production and development are completely separate databases
- Use the local CLI for testing the license flow during development

---

## 6. User Activation Flow

### What the user does

1. Logs into mycontext AI
2. Goes to **Settings** → **License** tab
3. Pastes their license key (e.g., `MC-ENT-A3F8...`)
4. Clicks **Activate**
5. Sees confirmation: "Enterprise license activated!"
6. All 85 patterns are now accessible

### What happens in the backend

The activation endpoint (`POST /api/license/activate`) does this:

1. Validates the user is logged in
2. Checks if user already has enterprise (skips if yes)
3. Looks up the key in `license_keys` table
4. Verifies: key exists, `is_valid = true`, `redeemed_by IS NULL`
5. Sets `redeemed_by = user.id` and `redeemed_at = now()`
6. Sets `users.enterprise_license = true`
7. Returns success response

### Error cases

| Scenario | Error message |
|----------|--------------|
| Key not found | "Invalid license key." |
| Key already used | "This license key has already been redeemed." |
| Key revoked | "This license key has been revoked." |
| Already enterprise | "Enterprise license is already active." |

---

## 7. Admin Operations

### Distributing keys to customers

1. Generate key(s) in Neon SQL Editor
2. Label them with the customer's name
3. Send the key via email, invoice, or your sales process
4. Customer activates in Settings → License

### Monitoring usage

Run this periodically in Neon to see who has activated:

```sql
SELECT u.email, u.enterprise_license, u.created_at AS signup_date,
       lk.key, lk.label, lk.redeemed_at
FROM users u
LEFT JOIN license_keys lk ON lk.redeemed_by = u.id
ORDER BY u.created_at DESC;
```

### Checking license status via API

```
GET /api/license/status
Authorization: Bearer <token>
```

Returns:

```json
{
  "enterprise_license": true,
  "activated_at": "2026-02-22T21:30:00+00:00"
}
```

---

## 8. Troubleshooting

### "Invalid license key" but key exists

- Check for extra spaces or line breaks when copying the key
- Verify the key is in the **production** Neon database (not local SQLite)
- Confirm `is_valid = true` in the database

### User activated but still sees Free

- Have the user log out and log back in (the JWT token caches the license state)
- Verify in the database: `SELECT enterprise_license FROM users WHERE email = '...'`

### Key shows "redeemed" but user didn't activate

- Someone else may have used the key (keys are not tied to emails until redeemed)
- Check `redeemed_by` to find which user redeemed it

### Need to transfer a license to a different user

```sql
-- Reset the old key
UPDATE license_keys SET redeemed_by = NULL, redeemed_at = NULL
WHERE key = 'MC-ENT-XXXX...';

-- Downgrade the old user
UPDATE users SET enterprise_license = false
WHERE email = 'old-user@example.com';

-- The key is now available for the new user to activate
```
