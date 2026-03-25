/**
 * open-collections-maintainer - You are tha maintainer of the open collections project, your purpose is to keep up to date postman collections for projets that don't publish themselves. you weekly observer these projects documentation and you update workspaces and collections. 
 *
 * This agent uses Mastra's Agent class with the Astro adapter to connect
 * to the Astro messaging service via gRPC.
 *
 * Environment variables (automatically injected by 'astro dev'):
 *   GRPC_SERVER_ADDR - injected by Astro messaging service
 *   OLLAMA_BASE_URL - injected by ollama model base URL
 *   OLLAMA_HOST - injected by ollama model host
 *   OLLAMA_MODEL - injected by ollama model model name
 *   OLLAMA_PORT - injected by ollama model port
 *   OLLAMA_URL - injected by ollama model URL
 */

import { Agent } from '@mastra/core/agent';
import { Mastra } from '@mastra/core/mastra';
import { Memory } from '@mastra/memory';
import { LibSQLStore } from '@mastra/libsql';
import { Observability } from '@mastra/observability';
import { OtelExporter } from '@mastra/otel-exporter';
import { serve } from '@astropods/adapter-mastra';

const memory = new Memory({
  storage: new LibSQLStore({
    id: 'memory',
    url: ':memory:',
  }),
});

function resolveOtlpTracesEndpoint(): string {
  const raw = process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318';
  try {
    const url = new URL(raw);
    if (!url.pathname || url.pathname === '/') {
      url.pathname = '/v1/traces';
    }
    return url.toString();
  } catch {
    return `${raw.replace(/\/+$/, '')}/v1/traces`;
  }
}

const observability = new Observability({
  configs: {
    otel: {
      serviceName: 'open-collections-maintainer',
      exporters: [
        new OtelExporter({
          provider: {
            custom: {
              endpoint: resolveOtlpTracesEndpoint(),
              protocol: 'http/protobuf',
            },
          },
        }),
      ],
    },
  },
});

const agent = new Agent({
  id: 'open-collections-maintainer',
  name: 'Open Collections Maintainer',
  instructions: 'You are Open Collections Maintainer, a helpful AI assistant. You are tha maintainer of the open collections project, your purpose is to keep up to date postman collections for projets that don\'t publish themselves. you weekly observer these projects documentation and you update workspaces and collections. ',
  model: 'ollama/llama3.1:8b',
  memory,
  // Ensure traces include stable Astro metadata by default.
  // The collector endpoint is injected by `ast dev`.
  defaultOptions: {
    tracingOptions: {
      tags: ['astro', 'agent:open-collections-maintainer'],
      metadata: {
        agent_id: 'open-collections-maintainer',
      },
    },
  },
});

// Instantiate Mastra so it registers agents/observability plugins at startup.
// `serve(agent)` handles request serving; this constructor call wires runtime integration.
new Mastra({
  agents: {
    'open-collections-maintainer': agent,
  },
  observability,
});

serve(agent);
