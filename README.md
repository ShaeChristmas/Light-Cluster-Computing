# Light Cluster Computing - Research Repository

## Overview
Collation of all of the information for the Light Cluster Computing Honours Project. All work was completed by Shaine Christmas at Deakin University (Student ID: 219206645)

The aim of the project is to research gaps in localised offloading technologies, specifically focusing on distribution of computations to low power devices.

The current stage of the project has 60% of the final Thesis document written, in addition to having a simple Prototype that uses a RESTful system to test the architecture on higher power devices. Implementation has occured across 3 RaspberryPi devices, with the client being any other device on the network.


## Main Research Files

### Paper Review.txt
This file contains research on the majority of the papers references within the Literature review. A template for how to assess and review papers is at the beginning of the document.

## API
API for testing the architecture of the end system. At this stage, three parts are implemented:
- Device Information sending and recieving.
- Device availability sending and recieving.
- Matrix Multiplication sending and recieving requests.
    Note: All devices running the API can act as a Leader or Follower Device. Clients request matricies to multiply using HTTP requests to the API. For implementation, see [Client.py](/Light-Cluster-Computing/Client%20Device/Client.py)

## Basic Device Code
Currently implements the device code for ZeroConf service advertisment and discovery. Note: Currently ServiceInfo is not advertised, but the service can be discovered.

## Client Device
Basic Python Client for the API device. This code currently implements all of the API endpoints, and can be expanded to implement future API or Prototype endpoints.

## Diagrams
Diagrams created for the Thesis Document. Figures are stored in PNG format, and for cases where code was used to form diagrams, code source is also included for ease of later editting. For example, the Sequence Diagram is collated using [Sequencediagram.org](https://sequencediagram.org/)

Sources used for Figure creation are as follows:
- [Sequencediagram.org](https://sequencediagram.org/)
- [Lucidchart](https://lucid.app/)

### Final Comments
This project is still a WIP, so if any bugs are encountered, please file a bug report.