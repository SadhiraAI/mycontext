---
sidebar_position: 4
title: Open Source (No License)
description: All 88 cognitive patterns are open source and ship in every install. There are no license keys or tiers. Migration notes for the deprecated license API.
---

# Open Source — No License Required

mycontext-ai is fully open source under the MIT license. **All 88 cognitive patterns** — core and advanced — ship in every `pip install mycontext-ai`, run offline with your own LLM API key, and require **no license key and no activation**.

```python
# Every pattern imports and runs directly — no activation step
from mycontext.templates.enterprise.decision import DecisionFramework

result = DecisionFramework().execute(
    provider="openai",
    decision="Should we expand to Southeast Asia next year?",
)
```

:::info Folder names are taxonomy only
The SDK still groups patterns under `mycontext.templates.free.*` and
`mycontext.templates.enterprise.*`. These are **organizational namespaces**, not
access tiers — both ship in the package and both are free to use.
:::

## Migrating from the old license API

Earlier releases gated the advanced patterns behind a license key. That gating
has been removed. The following functions are kept as **deprecated no-op shims**
for one release so existing imports do not break — they now emit a
`DeprecationWarning` and otherwise do nothing useful:

| Function | Old behavior | Now |
|----------|--------------|-----|
| `mycontext.activate_license(key)` | Stored a key, unlocked patterns | No-op, returns `True`, warns |
| `mycontext.deactivate_license()` | Removed the key | No-op, warns |
| `mycontext.is_enterprise_active()` | Reported license status | Always returns `True`, warns |

**Action required:** delete any `activate_license(...)` / `is_enterprise_active()`
calls from your code. The `include_enterprise` argument that some intelligence
functions accepted is also ignored — all patterns are always available.

```python
# Before
import mycontext
mycontext.activate_license("MC-ENT-...")
response, meta = smart_execute("Analyze this...", include_enterprise=True)

# After
from mycontext.intelligence import smart_execute
response, meta = smart_execute("Analyze this...")  # all 88 patterns considered
```

These shims will be removed in a future release — migrate now.
