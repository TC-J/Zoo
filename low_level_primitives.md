# Low Level Primitives; smoke her -- eye this guy, chest-mistake.
smoke me.
## Overview
The most important primitives are: Cages, Animals, Exhibitions, Jungles, Zoos.

Animals are designed like actor-model actors; they: contain state, have behavior, and send, recieve, and react to messages. It's a thread/process looping over messages & managed by an agent.

Cages are (potentially templated) images (& (potentially templated) environments) for animals to run on top of. Basically, OCI Images with meta and a template resolution phase optionally required and specified.

Exhibitions are the hardware platforms, virtual machines, and system containers that are built or located for cages & animals to be assigned on at runtime. They can further contain a service orchestration, like docker compose, first-spawn configuration specification, and command line. This makes them a host-platform provisioning description with additional, optional descriptions for configuration management, boot initializtion, service initialization, server, program, file, lib, and os-driver requirements, and runtime composition and system entry point command. With the potential to template & resolve variables and conditional-flows on deployment-evironment-specifics.


Jungles manage the configuration and operation of multiple exhibitions; like a group of microservices' infrastructure on a network subnet/partitiong and/or entirely separate domain/subdomain (difference?.)


Zoos are orchestrated, distributed runtime-deployment descriptions (templatable;) schedules a group of pods on to compatible infrastructure (like Kubernetes (or, Kubernetes)) that it first provisions & configures. Zoos are a whole domain that aggregates jungles in a load-balanced, fully configurable enterprise root subnet(s) and top-level domains.

## Primitives
### Cage
- OCI Image
    - Configuration JSON File (config.json)

    - Root Filesystem (Formatted, or, Unspecified)
        - On Host Filesystem
        - In File
            - Binary File; Raw Disk Image
            - Formatted Disk Image (e.g., ISO File)
            - Virtual Hard Disk Image File (*Multiple Formats)
            - Archive (CPIO, Tarball)


- Dockerfile


- VM Image



### Exhibition
- OCI Runtime Bundle (Traditional Container)
    - Manifest JSON File? (Confirm this)

    - OCI Image?


### Animal
- Actor Program
- 


### Zoo
Exhibitions (like a pod in kubernetes; close me.)


## Port 
abstraction over links that runs the link-layer liveness protocol (clock and neighbor health,) atomic-transactions, full message/packet transmission/exchange, and link-change (the connected container relocated and changed descriptors or entirely different schemas (for eg, went to the current host implementing IPC instead of being an HTTPS link.))

the abstraction specifies a named actor/service/etc. or a raw, protocol schema URI-endpoint -- and binds to an Container Agent/Actor/Service/etc..

# Link Abstraction
abstracts all ipc, network protocols, multi-threaded messaging, pipes, etc. 

links are available from the exhibit and are owned by a cage or animal/actor/agent.

## Message Bus

## 

## Cage Manifest (Dockerfile - like)
like an OCI image as an abstraction, literal, or mixture of both.



specify the initial files, packages, directories, etc.; as well as running background process dependencies, 

## Exhibition Manifest 
VM Image Provisioning Configuration Yaml/File (like vagrantfile VM description functions) with a Docker Compose Configuration Like-File for networkings, volumes, background services launching.

Machine requirements, image, provisioning, configuration, boot sequence, service availability, driver availability, etc..
    - A way to provision a physical/virtual platform node; configure drivers, layout, networks, mounts, boot-time bg services, service config-files, os config-files, etc. 

    - A way to automate CI/CD for the contained development repositories
        - version control:
            - hookfiles specifying lambda-file dir for: 
                - commits
                - pushes
                - pulls
                - branch changes
                - submodules...
                - subtrees...
                - ...

        - ci/cd server discovery

    - A way to automate configuration:
        - the service availability & configuration
        - system resource availability, default content, content checks, and accessibility (for eg, /etc config files, permissions on directories, packages, libraries, ...)

    - System Lifecycle & Key Event Hooks
        - declarative configs
        - imperative scripts


## Jungle Manifest (Vagrantfile and k8s deployment manifest - like)
define exhibitions to compose in to a distributed system -- define the network topology and physical or cloud infrastructure provisioning steps.

## OCI Continaers
## Virtual Machine Images 