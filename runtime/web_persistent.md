# Runtime Adapter — Web Persistent

## Runtime

`WEB_CHAT`

This adapter describes Web execution capabilities only. It does not select or implement Google Drive.

## Expected capabilities for the durable slice

Required for durable mode:

- conversation context;
- an external connector path capable of durable read/write to the selected provider.

Optional and not assumed:

- filesystem;
- code execution;
- background tasks;
- scheduler;
- hidden platform memory.

Do not branch on Free/Plus/Pro or vendor plan names. Branch on capabilities actually exposed by the host.

## Storage resolution

Provider resolution happens outside RuntimeAdapter.

Valid compositions include:

- `WEB_CHAT + CONTEXT_ONLY`;
- `WEB_CHAT + GoogleDriveProvider`;
- future `WEB_CHAT + TencentDocsProvider`;
- future `WEB_CHAT + NotionProvider`.

The runtime must not contain provider-specific kitchen rules.

## Degradation

If a configured durable provider cannot currently be read or written:

- continue using conversation context as best-effort working state;
- mark durability degraded;
- do not claim the latest state has been durably saved;
- retry/repair through persistence/health behavior, not through Cooking.
