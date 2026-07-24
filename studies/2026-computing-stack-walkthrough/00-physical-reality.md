# 00 — Physical Reality

## Information has a physical carrier

Every bit, parameter, Token state, file, and task ultimately exists through distinguishable physical states. Digital abstraction makes those states reliable and composable, but it does not remove their energy, timing, distance, or material cost.

A computing system begins with five physical functions:

```text
switching
storage
communication
power delivery
heat removal
```

Transistors switch and restore signals. Capacitors, transistor arrangements, and charge states preserve information. Wires and optical links move it. Power supplies enable transitions. Cooling removes the resulting heat.

## Computation and movement

A numerical operation changes state locally. Most useful computation also requires operands to reach the execution unit and results to reach their next consumer.

```text
total work
= state transition
+ data movement
+ synchronization
```

Distance matters. Moving data across a register file, across a chip, to HBM, to another accelerator, or across a data-centre network has progressively different latency and energy costs.

This is why the “von Neumann bottleneck” is broader than a historical CPU design issue: computation frequently waits for or spends energy on moving state.

## Physical hierarchy

```text
material
→ transistor
→ logic circuit
→ functional unit
→ die
→ package
→ server
→ rack
→ cluster
→ data centre
```

Modern accelerators depend on the complete hierarchy. Advanced packages place compute dies, memory stacks, and interconnect close together because the package itself has become part of the computer architecture.

## A Token’s physical path

A single generated Token may require:

1. reading input and KV state from memory;
2. loading model weights;
3. performing many multiply–accumulate operations;
4. communicating across devices;
5. writing new KV state;
6. sampling from the final logits;
7. sending bytes back through the serving stack.

The semantic unit “one Token” therefore corresponds to a large physical trajectory through memory, arithmetic units, links, and software queues.

## Agent workloads

Current accelerators are optimized mainly for regular model computation. Agent workloads add sparse and heterogeneous activity:

- file and database access;
- network calls and browser interaction;
- long-lived task state;
- waiting on people or services;
- multiple model and tool phases;
- recovery after interruption.

A future Agent-native machine is therefore likely to remain heterogeneous: dense model accelerators combined with CPUs, persistent storage, networks, and event-driven control systems.

## Anchors

- Information is embodied in physical state.
- Computation is state transition.
- Data movement is part of the algorithmic cost.
- Physical distance, power, timing, and heat shape every higher abstraction.
