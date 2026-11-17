> For the complete documentation index, see [llms.txt](https://docs.n8n.io/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolcode.md).

# Custom Code Tool

Learn how to use the Custom Code Tool node in n8n. Follow technical documentation to integrate Custom Code Tool node into your workflows.

Use the Custom Code Tool node to write code that an agent[^1] can run.

On this page, you'll find the node parameters for the Custom Code Tool node and links to more resources.

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

### Description <a href="#description" id="description"></a>

Give your custom code a description. This tells the agent when to use this tool. For example:

> Call this tool to get a random color. The input should be a string with comma separated names of colors to exclude.

### Language <a href="#language" id="language"></a>

You can use JavaScript or Python.

### JavaScript / Python box <a href="#javascript-python-box" id="javascript-python-box"></a>

Write the code here.

You can access the tool input using `query`. For example, to take the input string and lowercase it:

```js
let myString = query;
return myString.toLowerCase();
```

## Templates and examples <a href="#templates-and-examples" id="templates-and-examples"></a>

[Browse Custom Code Tool node documentation integration templates](https://n8n.io/integrations/code-tool) or [search all templates](https://n8n.io/workflows/)

## Related resources <a href="#related-resources" id="related-resources"></a>

Refer to [LangChain's documentation on tools](https://langchain-ai.github.io/langgraphjs/how-tos/tool-calling/) for more information about tools in LangChain.

View n8n's [Advanced AI](/build/integrate-ai.md) documentation.

[^1]: AI agents are artificial intelligence systems capable of responding to requests, making decisions, and performing real-world tasks for users. They use large language models (LLMs) to interpret user input and make decisions about how to best process requests using the information and resources they have available.
