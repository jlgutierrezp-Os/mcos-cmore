# Security Policy

## Status

MCOS/C-MORE v0.1 is local-first and uses synthetic examples only.

## Do not commit

- credentials;
- API keys;
- tokens;
- private prompts;
- private logs;
- sensitive personal records;
- private health records;
- production configuration;
- paid API credentials.

## Current activation state

```json
{
  "external_apis_active": false,
  "paid_apis_active": false,
  "mcp_server_active": false,
  "lean_adapter_active": false,
  "coq_adapter_active": false,
  "human_review_required": true
}
```

## Reporting

Open an issue for non-sensitive security concerns.

Do not paste secrets or private records into public issues.
