# Product FAQ — CloudSync Pro

**Department:** Product
**Last Updated:** 2026-06-20
**Access Level:** All Employees / Public-facing

## What is CloudSync Pro?
CloudSync Pro is our enterprise file synchronization and collaboration platform, supporting real-time sync across desktop, mobile, and web clients.

## What plans are available?
- **Starter:** Up to 10 users, 1TB pooled storage
- **Business:** Up to 100 users, 10TB pooled storage, SSO support
- **Enterprise:** Unlimited users, custom storage, dedicated support, on-prem option

## How does file versioning work?
CloudSync Pro retains the last 100 versions of a file, or 90 days of history, whichever comes first. Enterprise plans can extend retention to 1 year.

## Is there an API?
Yes. The REST API supports file upload/download, metadata queries, webhook subscriptions for change events, and admin user management. Rate limit is 1000 requests/minute on Business and Enterprise plans.

## What happens if I exceed my storage quota?
Uploads are paused and admins receive a notification. Existing files remain accessible. You can upgrade your plan or free up space to resume uploads.

## Does it support offline mode?
Yes, desktop and mobile clients cache recently accessed files for offline editing, and changes sync automatically once connectivity is restored.

## How is data encrypted?
Data is encrypted in transit (TLS 1.3) and at rest (AES-256). Enterprise customers can bring their own encryption keys (BYOK).
