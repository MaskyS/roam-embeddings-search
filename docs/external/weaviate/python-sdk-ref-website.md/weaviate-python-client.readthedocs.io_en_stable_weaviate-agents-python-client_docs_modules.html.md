---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html"
title: "Weaviate Agents — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- Weaviate Agents
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate-agents-python-client/docs/modules.rst.txt)

* * *

# Weaviate Agents [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html\#weaviate-agents "Link to this heading")

Weaviate Agents are pre-built agentic services designed to simplify common tasks when working with Large Language Models (LLMs) and your Weaviate instance. They are experts in performing Weaviate-specific data operations, streamlining AI development and data engineering workflows.

Warning

Weaviate Agents are currently only available for users of [Weaviate Cloud (WCD)](https://weaviate.io/developers/wcs/). They require a connection to a WCD instance and are not available for self-hosted Weaviate clusters at this time.

## Available agents [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html\#available-agents "Link to this heading")

The Weaviate Agents framework currently includes the following:

- [Query Agent](https://weaviate.io/developers/agents/query): Designed to answer natural language questions by intelligently querying the data stored within your Weaviate database.

- [Transformation Agent](https://weaviate.io/developers/agents/transformation): Enhances your data by manipulating it based on specific user instructions. This can involve tasks like summarizing, extracting information, or reformatting data stored in Weaviate.

- [Personalization Agent](https://weaviate.io/developers/agents/personalization): Customizes outputs based on persona-specific information. This agent can learn user behavior and provide recommendations tailored to individual preferences.


## Installation [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html\#installation "Link to this heading")

To use the Weaviate Agents, you need to install the main weaviate-client package with the optional \[agents\] extra dependency. Run the following command:

```
pip install -U "weaviate-client[agents]"

```

This ensures you have both the core client and the necessary components for interacting with the agents.

**Troubleshooting: Force pip to install the latest version**

If you suspect you don’t have the latest agent features, or if instructed to use a specific version, you can try explicitly upgrading or installing the `weaviate-agents` package itself:

- To upgrade to the latest available `weaviate-agents` version:


> ```
> pip install -U weaviate-agents
>
> ```

- To install a specific `weaviate-agents` version:


> ```
> pip install -U weaviate-agents==<version_number>
>
> ```
>
> _(Replace \`<version\_number>\` with the desired version, e.g., \`0.5.0\`)_


## Official documentation [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html\#official-documentation "Link to this heading")

For the most comprehensive and up-to-date information, examples, and guides on Weaviate Agents, please refer to the main Weaviate documentation website:

- [Weaviate Agents - Official documentation](https://weaviate.io/developers/agents)


## Client API reference [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html\#client-api-reference "Link to this heading")

Detailed documentation for the Python client classes and functions corresponding to these agents can be found below:

- [weaviate\_agents](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.html)
  - [Subpackages](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.html#subpackages)
  - [weaviate\_agents.base](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.html#module-weaviate_agents.base)
  - [weaviate\_agents.utils](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.html#weaviate-agents-utils)

## Support [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html\#support "Link to this heading")

- Use our [Forum](https://forum.weaviate.io/) for support or any other question.

- Use our [Slack Channel](https://weaviate.io/slack) for discussions or any other question.

- Use the `weaviate` tag on [StackOverflow](https://stackoverflow.com/questions/tagged/weaviate) for questions.

- For bugs or problems, submit a GitHub [issue](https://github.com/weaviate/weaviate-python-client/issues).


Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate-agents-python-client/docs/modules.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate-agents-python-client/docs/modules.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate-agents-python-client/docs/modules.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate-agents-python-client/docs/modules.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate-agents-python-client/docs/modules.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate-agents-python-client/docs/modules.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate-agents-python-client/docs/modules.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate-agents-python-client/docs/modules.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate-agents-python-client/docs/modules.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate-agents-python-client/docs/modules.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate-agents-python-client/docs/modules.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate-agents-python-client/docs/modules.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate-agents-python-client/docs/modules.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate-agents-python-client/docs/modules.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate-agents-python-client/docs/modules.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate-agents-python-client/docs/modules.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate-agents-python-client/docs/modules.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate-agents-python-client/docs/modules.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate-agents-python-client/docs/modules.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate-agents-python-client/docs/modules.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate-agents-python-client/docs/modules.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate-agents-python-client/docs/modules.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate-agents-python-client/docs/modules.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate-agents-python-client/docs/modules.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate-agents-python-client/docs/modules.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate-agents-python-client/docs/modules.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate-agents-python-client/docs/modules.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate-agents-python-client/docs/modules.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate-agents-python-client/docs/modules.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate-agents-python-client/docs/modules.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate-agents-python-client/docs/modules.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate-agents-python-client/docs/modules.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate-agents-python-client/docs/modules.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate-agents-python-client/docs/modules.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate-agents-python-client/docs/modules.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate-agents-python-client/docs/modules.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate-agents-python-client/docs/modules.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate-agents-python-client/docs/modules.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate-agents-python-client/docs/modules.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate-agents-python-client/docs/modules.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate-agents-python-client/docs/modules.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate-agents-python-client/docs/modules.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate-agents-python-client/docs/modules.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate-agents-python-client/docs/modules.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate-agents-python-client/docs/modules.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate-agents-python-client/docs/modules.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate-agents-python-client/docs/modules.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate-agents-python-client/docs/modules.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate-agents-python-client/docs/modules.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate-agents-python-client/docs/modules.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate-agents-python-client/docs/modules.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate-agents-python-client/docs/modules.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate-agents-python-client/docs/modules.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate-agents-python-client/docs/modules.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate-agents-python-client/docs/modules.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate-agents-python-client/docs/modules.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate-agents-python-client/docs/modules.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate-agents-python-client/docs/modules.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate-agents-python-client/docs/modules.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate-agents-python-client/docs/modules.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate-agents-python-client/docs/modules.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate-agents-python-client/docs/modules.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate-agents-python-client/docs/modules.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate-agents-python-client/docs/modules.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate-agents-python-client/docs/modules.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate-agents-python-client/docs/modules.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate-agents-python-client/docs/modules.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate-agents-python-client/docs/modules.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate-agents-python-client/docs/modules.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate-agents-python-client/docs/modules.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate-agents-python-client/docs/modules.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate-agents-python-client/docs/modules.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate-agents-python-client/docs/modules.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate-agents-python-client/docs/modules.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate-agents-python-client/docs/modules.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate-agents-python-client/docs/modules.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate-agents-python-client/docs/modules.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate-agents-python-client/docs/modules.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate-agents-python-client/docs/modules.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate-agents-python-client/docs/modules.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate-agents-python-client/docs/modules.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate-agents-python-client/docs/modules.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate-agents-python-client/docs/modules.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate-agents-python-client/docs/modules.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate-agents-python-client/docs/modules.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate-agents-python-client/docs/modules.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate-agents-python-client/docs/modules.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate-agents-python-client/docs/modules.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate-agents-python-client/docs/modules.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate-agents-python-client/docs/modules.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate-agents-python-client/docs/modules.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate-agents-python-client/docs/modules.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate-agents-python-client/docs/modules.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate-agents-python-client/docs/modules.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate-agents-python-client/docs/modules.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate-agents-python-client/docs/modules.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate-agents-python-client/docs/modules.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate-agents-python-client/docs/modules.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate-agents-python-client/docs/modules.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate-agents-python-client/docs/modules.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate-agents-python-client/docs/modules.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate-agents-python-client/docs/modules.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate-agents-python-client/docs/modules.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate-agents-python-client/docs/modules.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate-agents-python-client/docs/modules.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate-agents-python-client/docs/modules.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate-agents-python-client/docs/modules.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate-agents-python-client/docs/modules.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate-agents-python-client/docs/modules.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate-agents-python-client/docs/modules.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate-agents-python-client/docs/modules.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate-agents-python-client/docs/modules.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate-agents-python-client/docs/modules.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate-agents-python-client/docs/modules.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate-agents-python-client/docs/modules.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)