# Security and implementation roadmap

## Current implementation
The first runnable milestone contains chat, cloud/local provider fallback, SQLite message history, user-approved memory CRUD, and a simple emotional-style adapter.

## Before exposing the API beyond a trusted LAN
1. Add user authentication and per-device pairing.
2. Replace wildcard CORS with exact origins.
3. Disable cleartext HTTP; use HTTPS with certificate validation.
4. Add rate limiting, request-size limits, and encrypted secret storage.
5. Add deletion/export controls for chat and memory.

## Before adding computer-control tools
- Register tools by fixed name and validated JSON schema.
- Require user confirmation for file writes/deletes, purchases, messages, account changes, and other consequential actions.
- Show the exact target and action before confirmation.
- Use narrow file/folder allowlists; never accept arbitrary shell strings from model output.
- Add execution timeouts, cancellation, audit logs, and post-action verification.
- Keep microphone, camera, and screen capture off until the user explicitly starts them.
