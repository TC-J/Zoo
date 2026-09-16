# Design of The Zoo Framework Developer Kit (TZFDK; travel you, me.)

## The Actor's Model Meets State Packets, Graphs, & Agents (travel us.)

Carefully, scaled horizontally in public; our current Actor's Model definition, specifics-behave (behave me.)

Actors are loops that poll (endlessly check-on, basically -> "poll on)" messages and react by a: executing behaviors (i.e., decisions; actions,) cuing more actors (via messages (wink,)) changing behaviors (state-machines -- actors go in to "modes,)" or, creating new actors. They do only -- those things, emphasize. Wait for messages -- and react to them; optionally, maybe even typically, they reply to the original sender.

Actors typically connect to the/a message-bus on-system, premise. They request for actors that they need (dependencies, bite) using, roughly, a name, (or, descriptor (name, or, way to locate)) of a function (or, "intention", we'll define, one day; close me) -- to see if the system implements that function/intention. "Service discovery" -- this is typical in actor's model systems, drugs (though, i do not believe it is required by the original actor's model, which, i believe to be vague in many areas of its definition.)

So, we could scale this model to be across a group of machines within a datacenter network (a "cluster.)" Typically, the actor's model is for a single host system. We could even scale it, more-like, to be across network partitions and clusters (like, across multiple domains, subdomains, subnets, datacenters, or clusters.)

Actors -- to start -- are typically background processes, or containers -- on-premise or across the network.

### Our Specific Actor's Model Design

#### The Agent
The Agent we get to roughly define.

It is a singleton in a containerized runtime; so, it is a process-group leader -- in system level terms, poise; poise me; -- containing actors (contain me,) MCP tools, microservices, a subgraph of agents, &/or, LLM pipeline -- and actor/agent/lambda hooks (or, plug-ins, someway) in a loop that can recieve a Prompt and return a response, or, execute a task.

It's an extension of an actor.

Differences; it:
    - interprets messages more semantically, rather than nominally.

    - decisions are made non-deterministically (creatively; generatively(?.))

    - ...



#### The Animal

#### The State Packet

#### Graphs b/c

Graphs are webs of things -- of "nodes:" typically, a structure of specifically-typed memory. As in, we name fields in the memory structure -- as opposed to just naming the base-address and size pair and leaving the memory contained as a maybe-raw (there might be "embedded" subtypes (later defined in the program lifecycle; or, by a separate owner/user in the app, sly)) string of bytes; eye her okay-with-her's, sweating; eye him.

Nodes have vertices, which are locations of other nodes this node connects to -- and, optionally, a information on the nature of the connection (if connections are typed in the application, bus; travel me.)

###  Zoo Classes 
#### cage control agents
#### exhibitions
#### exhibition control agents
#### jungles
#### jungle control agents
#### zoos
#### zoo control agents


#### container agents
#### ai agents


### Zoo Information Exchange
* Information Exchange
* Message Communication
* Data Transmission

#### ZIE Fabric
#### ZIE Port
#### ZIE Link

#### ZIE Lane

#### ZIE Ingress/Egress/Bigress Wire
```python
class ZIEWireContract(Protocol):
    """
        capable of exchanging typed/untyped data structures from memory 
        to a driver.
    """

    @property
    def id() -> bytes: ...

    @property
    def alignment(): ...

    @property
    def wire_driver() -> : ...

    def put(): 
        """
        """
        ...

    def get(): 
        """
        """
        ...


class WireDriver(ABC)
```

#### 
#### ZRT Driver
#### Driver

#### ml-lambda
(ml-lambda)

#### model
(ml-lambda)

the broad category of machine-learning datastructures.

largely, the smaller ML techniques and models -- aside from transformers and LLMs.

#### llm
(ml-lambda; model)
specifically the ll model; extension of generic ml models.

#### ml-chain
(ml-lambda)

#### ml-pipeline
(ml-lambda)

#### ml-graph
(ml-lamda)

#### mcp tools
(ml-lambda)

#### animals
(ml-lambda)
an actor runtime-loop containing ports, LLM, 

#### resources
#### 
#### repositories
# 