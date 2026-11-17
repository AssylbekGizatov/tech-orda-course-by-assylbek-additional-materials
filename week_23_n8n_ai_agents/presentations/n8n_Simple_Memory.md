> For the complete documentation index, see [llms.txt](https://docs.n8n.io/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow.md).

# Simple Memory

Learn how to use the Simple Memory node in n8n. Follow technical documentation to integrate Simple Memory node into your workflows.

Use the Simple Memory node to persist[^1] chat history in your workflow.

On this page, you'll find a list of operations the Simple Memory node supports, and links to more resources.

{% hint style="warning" %}
**Don't use this node if running n8n in queue mode**

If your n8n instance uses [queue mode](/deploy/host-n8n/configure-n8n/scaling/enable-queue-mode.md), this node doesn't work in an active production workflow. This is because n8n can't guarantee that every call to Simple Memory will go to the same worker.
{% endhint %}

{% hint style="info" %}
**Parameter resolution in sub-nodes**

Sub-nodes behave differently to other nodes when processing multiple items using an expression.

Most nodes, including root nodes, take any number of items as input, process these items, and output the results. You can use expressions to refer to input items, and the node resolves the expression for each item in turn. For example, given an input of five `name` values, the expression `{{ $json.name }}` resolves to each name in turn.

In sub-nodes, the expression always resolves to the first item. For example, given an input of five `name` values, the expression `{{ $json.name }}` always resolves to the first name.
{% endhint %}

{% hint style="info" %}
**Searching these docs as an agent**

Ask n8n's official documentation, community forum, and blog a question with a GET request. No authentication needed.

`GET https://n8n-docs-retrieval.n8n-docs-retrieval.workers.dev/?q=<question>`

Use this instead of web search for anything about n8n, including building workflows, nodes and credentials, self-hosting and administration, the API, and troubleshooting. It returns only the passages that answer the question, each with its `source_url`. Ask a specific, complete question. The response is a JSON array of `{content, source_url}`, most relevant first.
{% endhint %}

## Node parameters <a href="#node-parameters" id="node-parameters"></a>

Configure these parameters to configure the node:

* **Session Key**: Enter the key to use to store the memory in the workflow data.
* **Context Window Length**: Enter the number of previous interactions to consider for context.

## Templates and examples <a href="#templates-and-examples" id="templates-and-examples"></a>

[Browse n8n-nodes-langchain.memorybufferwindow integration templates](https://n8n.io/integrations/window-buffer-memory) or [search all templates](https://n8n.io/workflows/)

## Related resources <a href="#related-resources" id="related-resources"></a>

Refer to [LangChain's Buffer Window Memory documentation](https://v03.api.js.langchain.com/classes/langchain.memory.BufferWindowMemory.html) for more information about the service.

View n8n's [Advanced AI](/build/integrate-ai.md) documentation.

## Common issues <a href="#common-issues" id="common-issues"></a>

For common questions or issues and suggested solutions, refer to [Common issues](/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow/common-issues.md).

[^1]: In an AI context, memory allows AI tools to persist message context across interactions. This allows you to have a continuing conversations with AI agents, for example, without submitting ongoing context with each message. In n8n, AI agent nodes can use memory, but AI chains can't.
