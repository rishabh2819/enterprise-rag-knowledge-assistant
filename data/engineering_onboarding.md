# Engineering Onboarding Guide

**Department:** Engineering
**Last Updated:** 2026-02-18
**Access Level:** Engineering Team

## Week 1: Setup
- Get laptop provisioned via IT, install standard toolchain (see internal wiki: dev-environment-setup)
- Request access to GitHub org, Jira, and internal VPN
- Complete mandatory security training module

## Week 1-2: Codebase Orientation
- Clone core repositories: `platform-api`, `web-client`, `infra-terraform`
- Read the Architecture Decision Records (ADR) folder in `platform-api/docs/adr`
- Shadow a teammate on an on-call shift walkthrough (non-live)

## Team Structure
- Platform Team: core API, auth, billing
- Client Team: web + mobile apps
- Infra Team: Kubernetes, CI/CD, observability
- Data Team: analytics pipeline, ML infra

## Development Workflow
1. Create a branch from `main` following `feature/JIRA-ID-short-desc` naming
2. Open a draft PR early for visibility
3. All PRs require 1 approval and passing CI before merge
4. Squash-merge to main; deploys happen automatically to staging

## On-Call Expectations
- Rotations are weekly, opt-in after 3 months tenure
- Primary on-call must acknowledge pages within 15 minutes
- Postmortems required for any Sev1/Sev2 incident within 48 hours

## Useful Links
- Internal wiki: wiki.company-internal.example
- Runbooks: runbooks.company-internal.example
- Design system: design.company-internal.example
