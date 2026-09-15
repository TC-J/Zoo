# High Level Semantics; Close Her
Cages, Animals, Exhibitions, Jungles, Zoos.

Animals are designed like actor-model actors; they: contain state, have behavior, and send, recieve, and react to messages. It's a thread/process looping over messages & managed by an agent.

Cages are (potentially templated) images (& (potentially templated) environments) for animals to run on top of. Basically, OCI Images with meta and a template resolution phase optionally required and specified.

Exhibitions are the hardware platforms, virtual machines, and system containers that are built or located for cages & animals to be assigned on at runtime. They can further contain a service orchestration, like docker compose, first-spawn configuration specification, and command line. This makes them a host-platform provisioning description with additional, optional descriptions for configuration management, boot initializtion, service initialization, server, program, file, lib, and os-driver requirements, and runtime composition and system entry point command. With the potential to template & resolve variables and conditional-flows on deployment-evironment-specifics.


Jungles manage the configuration and operation of multiple exhibitions; like a group of microservices' infrastructure on a network subnet/partitiong and/or entirely separate domain/subdomain (difference?.)


Zoos are orchestrated, distributed runtime-deployments; a scheduled group of pods on to infrastructure (like Kubernetes (or, Kubernetes))

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