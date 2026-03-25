# open-collections-maintainer

You are tha maintainer of the open collections project, your purpose is to keep up to date postman collections for projets that don't publish themselves. you weekly observer these projects documentation and you update workspaces and collections. 

## Quick start

```bash
# Install dependencies
bun install

# Start the agent locally
ast dev
```

## Project structure

```
open-collections-maintainer/
├── agent/
│   └── index.ts          # Agent entry point
├── astropods.yml             # Agent specification
├── Dockerfile            # Agent container
├── .env                  # Environment variables (set via ast configure; not committed)
└── package.json
```

## Configuration

The agent is configured in `astropods.yml`. Key sections:

### Model

Self-hosted **ollama** provider running `llama3.1:8b`.

### Interfaces
- **Web** — HTTP/SSE endpoint (playground available at `localhost:3000` during dev)

