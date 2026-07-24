# 06 — Distributed AI Computing

## Why one accelerator is insufficient

Large models exceed a single device’s memory, training-time compute budget, or serving capacity. Distributed execution combines devices through an explicit communication topology.

Each process commonly has a **rank** within a **world size** and participates in communication groups.

## Collective operations

Important collectives include:

- broadcast — one rank sends the same data to all;
- reduce — combine values at one destination;
- all-reduce — combine values and distribute the result to all;
- all-gather — collect shards from every rank;
- reduce-scatter — reduce and leave each rank with a shard;
- all-to-all — exchange different data among all ranks.

These operations are the distributed equivalents of shared data movement and synchronization.

## Parallelism strategies

### Data parallelism

Each worker holds a model replica, processes a different mini-batch, and combines gradients. It increases throughput while replicating model and optimizer state.

### Sharded data parallelism

ZeRO/FSDP-style methods shard optimizer state, gradients, and eventually parameters across workers, reconstructing state when required.

### Tensor parallelism

Individual matrix operations are partitioned across devices. Column and row partitioning divide output features or reduction dimensions and require all-gather or all-reduce communication.

### Pipeline parallelism

Groups of layers form stages. Micro-batches flow through the stages, creating overlap while introducing pipeline bubbles and scheduling complexity.

### Expert parallelism

Mixture-of-experts models place experts on different devices. Routers send Tokens to selected experts, often requiring all-to-all communication and careful load balancing.

Large systems combine dimensions:

```text
data × tensor × pipeline × expert parallelism
```

## Topology awareness

Communication inside one accelerator package, one server, one rack, or across a network has different bandwidth and latency. Parallel groups should place frequent and high-volume collectives on the strongest links.

## Training step

A distributed training step may contain:

```text
input sharding
→ forward compute
→ activation communication
→ backward compute
→ gradient collectives
→ optimizer update
→ checkpoint
```

The exposed step time includes compute, communication that cannot be overlapped, pipeline bubbles, load imbalance, and runtime overhead.

## Inference

Serving can replicate complete models for request parallelism or shard one model across devices. Prefill and decode may be placed on separate worker pools, transferring KV state between them. Long contexts make state placement and transfer first-class scheduling decisions.

## Agent correspondence

- independent Tasks resemble data parallel work;
- tightly coupled subproblems resemble tensor parallelism;
- staged research–build–test flows resemble pipeline parallelism;
- specialist routing resembles expert parallelism.

The analogy emphasizes the same constraint: useful parallelism comes from true independence, while synchronization and state transfer determine the remaining cost.
