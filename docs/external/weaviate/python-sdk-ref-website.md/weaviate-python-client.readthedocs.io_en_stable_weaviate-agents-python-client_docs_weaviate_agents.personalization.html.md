---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html"
title: "weaviate_agents.personalization — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- [Weaviate Agents](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/modules.html)
- [weaviate\_agents](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.html)
- weaviate\_agents.personalization
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate-agents-python-client/docs/weaviate_agents.personalization.rst.txt)

* * *

# weaviate\_agents.personalization [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html\#module-weaviate_agents.personalization "Link to this heading")

_class_ weaviate\_agents.personalization.PersonalizationAgent( _client_, _reference\_collection_, _agents\_host=None_, _vector\_name=None_, _timeout=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent "Link to this definition")

Bases: `_BaseAgent`\[ [`WeaviateClient`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")\]

An agent for personalizing search results and queries based on persona interactions.

Warning

Weaviate Agents - Personalization Agent is an early stage alpha product. The API is subject to
breaking changes. Please ensure you are using the latest version of the client.

For more information, see the [Weaviate Agents - Personalization Agent Docs](https://weaviate.io/developers/agents/personalization)

Initialize the base agent.

Parameters:

- **client** ( [_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")) – A Weaviate client instance, either sync or async.

- **agents\_host** ( _str_ _\|_ _None_) – Optional host URL for the agents service. If not provided,
will use the default agents host.

- **reference\_collection** ( _str_)

- **vector\_name** ( _str_ _\|_ _None_)

- **timeout** ( _int_ _\|_ _None_)


add\_interactions( _interactions_, _create\_persona\_if\_not\_exists=True_, _remove\_previous\_interactions=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.add_interactions) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.add_interactions "Link to this definition")

Add interactions for personas to the Personalization Agent.

Parameters:

- **interactions** ( _list_ _\[_ [_PersonaInteraction_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteraction "weaviate_agents.personalization.classes.persona.PersonaInteraction") _\]_) – List of interactions to add. Each interaction can specify
replace\_previous\_interactions=True to replace that specific
item’s interaction history.

- **create\_persona\_if\_not\_exists** ( _bool_) – Whether to create personas that don’t exist yet

- **remove\_previous\_interactions** ( _bool_) – Whether to remove previous interactions for all items
in the current batch. Setting this to True is equivalent
to setting replace\_previous\_interactions=True for every
interaction in the batch. Use with caution as it affects
all items in the current batch.


Return type:

None

add\_persona( _persona_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.add_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.add_persona "Link to this definition")

Add a persona to the Personalization Agent’s persona collection.

Parameters:

- **persona** ( [_Persona_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona "weaviate_agents.personalization.classes.persona.Persona")) – The persona to add. The persona must have a persona\_id and properties that match the user properties

- **created.** ( _defined when the Personalization Agent was_)


Return type:

None

_classmethod_ connect( _client_, _reference\_collection_, _agents\_host=None_, _vector\_name=None_, _timeout=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.connect) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.connect "Link to this definition")

Connect to an existing Personalization Agent for a collection.

Parameters:

- **client** ( [_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")) – The Weaviate client

- **reference\_collection** ( _str_) – The name of the collection to connect to

- **agents\_host** ( _str_ _\|_ _None_) – Optional host URL for the agents service

- **vector\_name** ( _str_ _\|_ _None_) – Optional name of the vector field to use

- **timeout** ( _int_ _\|_ _None_) – Optional timeout for the request


Returns:

An instance of the Personalization Agent

Return type:

[_PersonalizationAgent_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent "weaviate_agents.personalization.personalization_agent.PersonalizationAgent")

_classmethod_ create( _client_, _reference\_collection_, _user\_properties=None_, _agents\_host=None_, _vector\_name=None_, _timeout=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.create) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.create "Link to this definition")

Create a new Personalization Agent for a collection.

Parameters:

- **client** ( [_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")) – The Weaviate client

- **reference\_collection** ( _str_) – The name of the collection to personalize

- **user\_properties** ( _dict_ _\[_ _str_ _,_ [_DataType_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.DataType "weaviate.collections.classes.config.DataType") _\]_ _\|_ _None_) – Optional dictionary of user properties and their data types

- **agents\_host** ( _str_ _\|_ _None_) – Optional host URL for the agents service

- **vector\_name** ( _str_ _\|_ _None_) – Optional name of the vector field to use

- **timeout** ( _int_ _\|_ _None_) – Optional timeout for the request


Returns:

A new instance of the Personalization Agent

Return type:

[_PersonalizationAgent_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent "weaviate_agents.personalization.personalization_agent.PersonalizationAgent")

delete\_persona( _persona\_id_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.delete_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.delete_persona "Link to this definition")

Delete a persona by persona\_id from the Personalization Agent’s persona collection.

Parameters:

**persona\_id** ( _UUID_) – The ID of the persona to delete

Return type:

None

_classmethod_ exists( _client_, _reference\_collection_, _agents\_host=None_, _timeout=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.exists) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.exists "Link to this definition")

Check if a persona collection exists for a given reference collection.

Parameters:

- **client** ( [_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")) – The Weaviate client

- **reference\_collection** ( _str_) – The name of the collection to check

- **agents\_host** ( _str_ _\|_ _None_) – Optional host URL for the agents service

- **timeout** ( _int_ _\|_ _None_) – Optional timeout for the request


Returns:

True if the persona collection exists, False otherwise

Return type:

bool

get\_interactions( _persona\_id_, _interaction\_type_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.get_interactions) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.get_interactions "Link to this definition")

Get interactions for a specific persona filtered by interaction type.

Parameters:

- **persona\_id** ( _UUID_) – The ID of the persona to get interactions for

- **interaction\_type** ( _str_) – The type of interaction to filter by (e.g. “positive”, “negative”)


Returns:

List of matching interactions for the persona

Return type:

list\[ [_PersonaInteractionResponse_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteractionResponse "weaviate_agents.personalization.classes.persona.PersonaInteractionResponse")\]

get\_objects( _persona\_id_, _limit=10_, _recent\_interactions\_count=100_, _exclude\_interacted\_items=True_, _decay\_rate=0.1_, _exclude\_items=\[\]_, _use\_agent\_ranking=True_, _explain\_results=True_, _instruction=None_, _filters=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.get_objects) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.get_objects "Link to this definition")

Get Personalized objects for a specific persona.

Parameters:

- **persona\_id** ( _UUID_) – The ID of the persona to get objects for

- **limit** ( _int_) – The maximum number of objects to return

- **recent\_interactions\_count** ( _int_) – The number of recent interactions to consider

- **exclude\_interacted\_items** ( _bool_) – Whether to exclude items that have been interacted with

- **decay\_rate** ( _float_) – The decay rate for the personalization algorithm

- **exclude\_items** ( _list_ _\[_ _str_ _\]_) – List of items to exclude from the results

- **use\_agent\_ranking** ( _bool_) – Whether to use agent ranking for the results

- **explain\_results** ( _bool_) – Whether to explain the results

- **instruction** ( _str_ _\|_ _None_) – Optional instruction to guide the personalization process

- **filters** ( [_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters") _\|_ _None_) – Optional filters to apply to the results


Return type:

[_PersonalizationAgentGetObjectsResponse_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationAgentGetObjectsResponse "weaviate_agents.personalization.classes.response.PersonalizationAgentGetObjectsResponse")

get\_persona( _persona\_id_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.get_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.get_persona "Link to this definition")

Get a persona by persona\_id from the Personalization Agent’s persona collection.

Parameters:

**persona\_id** ( _UUID_) – The ID of the persona to retrieve

Returns:

The retrieved persona

Return type:

[_Persona_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona "weaviate_agents.personalization.classes.persona.Persona")

has\_persona( _persona\_id_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.has_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.has_persona "Link to this definition")

Check if a persona exists in the Personalization Agent’s persona collection.

Parameters:

**persona\_id** ( _UUID_) – The ID of the persona to check

Returns:

True if the persona exists, False otherwise

Return type:

bool

query( _persona\_id_, _strength=0.5_, _overfetch\_factor=1.5_, _recent\_interactions\_count=100_, _decay\_rate=0.1_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.query) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.query "Link to this definition")Parameters:

- **persona\_id** ( _UUID_)

- **strength** ( _float_)

- **overfetch\_factor** ( _float_)

- **recent\_interactions\_count** ( _int_)

- **decay\_rate** ( _float_)


Return type:

_PersonalizedQuery_

update\_persona( _persona_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.update_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.PersonalizationAgent.update_persona "Link to this definition")

Update an existing persona in the Personalization Agent’s persona collection.

Parameters:

**persona** ( [_Persona_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona "weaviate_agents.personalization.classes.persona.Persona")) – The persona to update. The persona must have a persona\_id and properties that match
the user properties defined when the Personalization Agent was created.

Return type:

None

## Subpackages [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html\#subpackages "Link to this heading")

- [weaviate\_agents.personalization.classes package](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html)
  - [`Persona`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona)
    - [`Persona.persona_id`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona.persona_id)
    - [`Persona.properties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona.properties)
  - [`PersonaInteraction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteraction)
    - [`PersonaInteraction.created_at`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteraction.created_at)
    - [`PersonaInteraction.item_id`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteraction.item_id)
    - [`PersonaInteraction.persona_id`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteraction.persona_id)
    - [`PersonaInteraction.replace_previous_interactions`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteraction.replace_previous_interactions)
    - [`PersonaInteraction.weight`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteraction.weight)
  - [`PersonaInteractionResponse`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteractionResponse)
    - [`PersonaInteractionResponse.created_at`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteractionResponse.created_at)
    - [`PersonaInteractionResponse.item_id`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteractionResponse.item_id)
    - [`PersonaInteractionResponse.weight`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteractionResponse.weight)
  - [`PersonalizationAgentGetObjectsResponse`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationAgentGetObjectsResponse)
    - [`PersonalizationAgentGetObjectsResponse.objects`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationAgentGetObjectsResponse.objects)
    - [`PersonalizationAgentGetObjectsResponse.ranking_rationale`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationAgentGetObjectsResponse.ranking_rationale)
    - [`PersonalizationAgentGetObjectsResponse.usage`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationAgentGetObjectsResponse.usage)
  - [`PersonalizedObject`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedObject)
    - [`PersonalizedObject.original_rank`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedObject.original_rank)
    - [`PersonalizedObject.personalized_rank`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedObject.personalized_rank)
    - [`PersonalizedObject.properties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedObject.properties)
    - [`PersonalizedObject.uuid`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedObject.uuid)
    - [`PersonalizedObject.model_dump()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedObject.model_dump)
  - [`Usage`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Usage)
    - [`Usage.details`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Usage.details)
    - [`Usage.request_tokens`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Usage.request_tokens)
    - [`Usage.requests`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Usage.requests)
    - [`Usage.response_tokens`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Usage.response_tokens)
    - [`Usage.total_tokens`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Usage.total_tokens)
  - [`PersonalizedQueryResponse`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedQueryResponse)
    - [`PersonalizedQueryResponse.objects`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedQueryResponse.objects)
    - [`PersonalizedQueryResponse.usage`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizedQueryResponse.usage)
  - [`GetObjectsRequest`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest)
    - [`GetObjectsRequest.decay_rate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.decay_rate)
    - [`GetObjectsRequest.exclude_interacted_items`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.exclude_interacted_items)
    - [`GetObjectsRequest.exclude_items`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.exclude_items)
    - [`GetObjectsRequest.explain_results`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.explain_results)
    - [`GetObjectsRequest.filters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.filters)
    - [`GetObjectsRequest.instruction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.instruction)
    - [`GetObjectsRequest.limit`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.limit)
    - [`GetObjectsRequest.persona_id`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.persona_id)
    - [`GetObjectsRequest.recent_interactions_count`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.recent_interactions_count)
    - [`GetObjectsRequest.use_agent_ranking`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.GetObjectsRequest.use_agent_ranking)
  - [`PersonalizationRequest`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationRequest)
    - [`PersonalizationRequest.collection_name`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationRequest.collection_name)
    - [`PersonalizationRequest.create`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationRequest.create)
    - [`PersonalizationRequest.headers`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationRequest.headers)
    - [`PersonalizationRequest.item_collection_vector_name`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationRequest.item_collection_vector_name)
    - [`PersonalizationRequest.persona_properties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationRequest.persona_properties)
  - [`BM25QueryParameters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters)
    - [`BM25QueryParameters.auto_limit`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.auto_limit)
    - [`BM25QueryParameters.filters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.filters)
    - [`BM25QueryParameters.include_vector`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.include_vector)
    - [`BM25QueryParameters.limit`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.limit)
    - [`BM25QueryParameters.offset`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.offset)
    - [`BM25QueryParameters.query`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.query)
    - [`BM25QueryParameters.query_method`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.query_method)
    - [`BM25QueryParameters.query_properties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.query_properties)
    - [`BM25QueryParameters.rerank`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.rerank)
    - [`BM25QueryParameters.return_metadata`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.return_metadata)
    - [`BM25QueryParameters.return_properties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.return_properties)
    - [`BM25QueryParameters.return_references`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.BM25QueryParameters.return_references)
  - [`HybridQueryParameters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters)
    - [`HybridQueryParameters.alpha`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.alpha)
    - [`HybridQueryParameters.auto_limit`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.auto_limit)
    - [`HybridQueryParameters.filters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.filters)
    - [`HybridQueryParameters.fusion_type`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.fusion_type)
    - [`HybridQueryParameters.include_vector`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.include_vector)
    - [`HybridQueryParameters.limit`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.limit)
    - [`HybridQueryParameters.max_vector_distance`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.max_vector_distance)
    - [`HybridQueryParameters.offset`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.offset)
    - [`HybridQueryParameters.query`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.query)
    - [`HybridQueryParameters.query_method`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.query_method)
    - [`HybridQueryParameters.query_properties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.query_properties)
    - [`HybridQueryParameters.rerank`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.rerank)
    - [`HybridQueryParameters.return_metadata`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.return_metadata)
    - [`HybridQueryParameters.return_properties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.return_properties)
    - [`HybridQueryParameters.return_references`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.return_references)
    - [`HybridQueryParameters.target_vector`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.target_vector)
    - [`HybridQueryParameters.vector`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.HybridQueryParameters.vector)
  - [`NearTextQueryParameters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters)
    - [`NearTextQueryParameters.auto_limit`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.auto_limit)
    - [`NearTextQueryParameters.certainty`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.certainty)
    - [`NearTextQueryParameters.distance`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.distance)
    - [`NearTextQueryParameters.filters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.filters)
    - [`NearTextQueryParameters.include_vector`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.include_vector)
    - [`NearTextQueryParameters.limit`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.limit)
    - [`NearTextQueryParameters.move_away`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.move_away)
    - [`NearTextQueryParameters.move_to`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.move_to)
    - [`NearTextQueryParameters.offset`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.offset)
    - [`NearTextQueryParameters.query`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.query)
    - [`NearTextQueryParameters.query_method`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.query_method)
    - [`NearTextQueryParameters.rerank`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.rerank)
    - [`NearTextQueryParameters.return_metadata`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.return_metadata)
    - [`NearTextQueryParameters.return_properties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.return_properties)
    - [`NearTextQueryParameters.return_references`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.return_references)
    - [`NearTextQueryParameters.target_vector`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.NearTextQueryParameters.target_vector)
  - [`QueryRequest`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.QueryRequest)
    - [`QueryRequest.decay_rate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.QueryRequest.decay_rate)
    - [`QueryRequest.overfetch_factor`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.QueryRequest.overfetch_factor)
    - [`QueryRequest.persona_id`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.QueryRequest.persona_id)
    - [`QueryRequest.query_parameters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.QueryRequest.query_parameters)
    - [`QueryRequest.recent_interactions_count`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.QueryRequest.recent_interactions_count)
    - [`QueryRequest.strength`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.QueryRequest.strength)

### weaviate\_agents.personalization.personalization\_agent [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html\#module-weaviate_agents.personalization.personalization_agent "Link to this heading")

_class_ weaviate\_agents.personalization.personalization\_agent.PersonalizationAgent( _client_, _reference\_collection_, _agents\_host=None_, _vector\_name=None_, _timeout=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent "Link to this definition")

Bases: `_BaseAgent`\[ [`WeaviateClient`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")\]

An agent for personalizing search results and queries based on persona interactions.

Warning

Weaviate Agents - Personalization Agent is an early stage alpha product. The API is subject to
breaking changes. Please ensure you are using the latest version of the client.

For more information, see the [Weaviate Agents - Personalization Agent Docs](https://weaviate.io/developers/agents/personalization)

Initialize the base agent.

Parameters:

- **client** ( [_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")) – A Weaviate client instance, either sync or async.

- **agents\_host** ( _str_ _\|_ _None_) – Optional host URL for the agents service. If not provided,
will use the default agents host.

- **reference\_collection** ( _str_)

- **vector\_name** ( _str_ _\|_ _None_)

- **timeout** ( _int_ _\|_ _None_)


_classmethod_ create( _client_, _reference\_collection_, _user\_properties=None_, _agents\_host=None_, _vector\_name=None_, _timeout=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.create) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.create "Link to this definition")

Create a new Personalization Agent for a collection.

Parameters:

- **client** ( [_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")) – The Weaviate client

- **reference\_collection** ( _str_) – The name of the collection to personalize

- **user\_properties** ( _dict_ _\[_ _str_ _,_ [_DataType_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.DataType "weaviate.collections.classes.config.DataType") _\]_ _\|_ _None_) – Optional dictionary of user properties and their data types

- **agents\_host** ( _str_ _\|_ _None_) – Optional host URL for the agents service

- **vector\_name** ( _str_ _\|_ _None_) – Optional name of the vector field to use

- **timeout** ( _int_ _\|_ _None_) – Optional timeout for the request


Returns:

A new instance of the Personalization Agent

Return type:

[_PersonalizationAgent_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent "weaviate_agents.personalization.personalization_agent.PersonalizationAgent")

_classmethod_ connect( _client_, _reference\_collection_, _agents\_host=None_, _vector\_name=None_, _timeout=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.connect) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.connect "Link to this definition")

Connect to an existing Personalization Agent for a collection.

Parameters:

- **client** ( [_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")) – The Weaviate client

- **reference\_collection** ( _str_) – The name of the collection to connect to

- **agents\_host** ( _str_ _\|_ _None_) – Optional host URL for the agents service

- **vector\_name** ( _str_ _\|_ _None_) – Optional name of the vector field to use

- **timeout** ( _int_ _\|_ _None_) – Optional timeout for the request


Returns:

An instance of the Personalization Agent

Return type:

[_PersonalizationAgent_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent "weaviate_agents.personalization.personalization_agent.PersonalizationAgent")

add\_persona( _persona_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.add_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.add_persona "Link to this definition")

Add a persona to the Personalization Agent’s persona collection.

Parameters:

- **persona** ( [_Persona_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona "weaviate_agents.personalization.classes.persona.Persona")) – The persona to add. The persona must have a persona\_id and properties that match the user properties

- **created.** ( _defined when the Personalization Agent was_)


Return type:

None

update\_persona( _persona_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.update_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.update_persona "Link to this definition")

Update an existing persona in the Personalization Agent’s persona collection.

Parameters:

**persona** ( [_Persona_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona "weaviate_agents.personalization.classes.persona.Persona")) – The persona to update. The persona must have a persona\_id and properties that match
the user properties defined when the Personalization Agent was created.

Return type:

None

get\_persona( _persona\_id_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.get_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.get_persona "Link to this definition")

Get a persona by persona\_id from the Personalization Agent’s persona collection.

Parameters:

**persona\_id** ( _UUID_) – The ID of the persona to retrieve

Returns:

The retrieved persona

Return type:

[_Persona_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.Persona "weaviate_agents.personalization.classes.persona.Persona")

delete\_persona( _persona\_id_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.delete_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.delete_persona "Link to this definition")

Delete a persona by persona\_id from the Personalization Agent’s persona collection.

Parameters:

**persona\_id** ( _UUID_) – The ID of the persona to delete

Return type:

None

has\_persona( _persona\_id_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.has_persona) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.has_persona "Link to this definition")

Check if a persona exists in the Personalization Agent’s persona collection.

Parameters:

**persona\_id** ( _UUID_) – The ID of the persona to check

Returns:

True if the persona exists, False otherwise

Return type:

bool

add\_interactions( _interactions_, _create\_persona\_if\_not\_exists=True_, _remove\_previous\_interactions=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.add_interactions) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.add_interactions "Link to this definition")

Add interactions for personas to the Personalization Agent.

Parameters:

- **interactions** ( _list_ _\[_ [_PersonaInteraction_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteraction "weaviate_agents.personalization.classes.persona.PersonaInteraction") _\]_) – List of interactions to add. Each interaction can specify
replace\_previous\_interactions=True to replace that specific
item’s interaction history.

- **create\_persona\_if\_not\_exists** ( _bool_) – Whether to create personas that don’t exist yet

- **remove\_previous\_interactions** ( _bool_) – Whether to remove previous interactions for all items
in the current batch. Setting this to True is equivalent
to setting replace\_previous\_interactions=True for every
interaction in the batch. Use with caution as it affects
all items in the current batch.


Return type:

None

get\_interactions( _persona\_id_, _interaction\_type_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.get_interactions) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.get_interactions "Link to this definition")

Get interactions for a specific persona filtered by interaction type.

Parameters:

- **persona\_id** ( _UUID_) – The ID of the persona to get interactions for

- **interaction\_type** ( _str_) – The type of interaction to filter by (e.g. “positive”, “negative”)


Returns:

List of matching interactions for the persona

Return type:

list\[ [_PersonaInteractionResponse_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonaInteractionResponse "weaviate_agents.personalization.classes.persona.PersonaInteractionResponse")\]

get\_objects( _persona\_id_, _limit=10_, _recent\_interactions\_count=100_, _exclude\_interacted\_items=True_, _decay\_rate=0.1_, _exclude\_items=\[\]_, _use\_agent\_ranking=True_, _explain\_results=True_, _instruction=None_, _filters=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.get_objects) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.get_objects "Link to this definition")

Get Personalized objects for a specific persona.

Parameters:

- **persona\_id** ( _UUID_) – The ID of the persona to get objects for

- **limit** ( _int_) – The maximum number of objects to return

- **recent\_interactions\_count** ( _int_) – The number of recent interactions to consider

- **exclude\_interacted\_items** ( _bool_) – Whether to exclude items that have been interacted with

- **decay\_rate** ( _float_) – The decay rate for the personalization algorithm

- **exclude\_items** ( _list_ _\[_ _str_ _\]_) – List of items to exclude from the results

- **use\_agent\_ranking** ( _bool_) – Whether to use agent ranking for the results

- **explain\_results** ( _bool_) – Whether to explain the results

- **instruction** ( _str_ _\|_ _None_) – Optional instruction to guide the personalization process

- **filters** ( [_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters") _\|_ _None_) – Optional filters to apply to the results


Return type:

[_PersonalizationAgentGetObjectsResponse_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.classes.html#weaviate_agents.personalization.classes.PersonalizationAgentGetObjectsResponse "weaviate_agents.personalization.classes.response.PersonalizationAgentGetObjectsResponse")

_classmethod_ exists( _client_, _reference\_collection_, _agents\_host=None_, _timeout=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.exists) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.exists "Link to this definition")

Check if a persona collection exists for a given reference collection.

Parameters:

- **client** ( [_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")) – The Weaviate client

- **reference\_collection** ( _str_) – The name of the collection to check

- **agents\_host** ( _str_ _\|_ _None_) – Optional host URL for the agents service

- **timeout** ( _int_ _\|_ _None_) – Optional timeout for the request


Returns:

True if the persona collection exists, False otherwise

Return type:

bool

query( _persona\_id_, _strength=0.5_, _overfetch\_factor=1.5_, _recent\_interactions\_count=100_, _decay\_rate=0.1_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate_agents/personalization/personalization_agent.html#PersonalizationAgent.query) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html#weaviate_agents.personalization.personalization_agent.PersonalizationAgent.query "Link to this definition")Parameters:

- **persona\_id** ( _UUID_)

- **strength** ( _float_)

- **overfetch\_factor** ( _float_)

- **recent\_interactions\_count** ( _int_)

- **decay\_rate** ( _float_)


Return type:

_PersonalizedQuery_

Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate-agents-python-client/docs/weaviate_agents.personalization.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)