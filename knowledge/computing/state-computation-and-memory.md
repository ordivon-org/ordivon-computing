# State, Computation, and Memory

## Information is physical state

A bit is not an abstract symbol floating outside the machine. It is represented by a physical state that can be distinguished and restored: voltage ranges in logic, charge in DRAM, transistor arrangements in SRAM, or stored charge levels in flash.

Computation is therefore a controlled state transition:

```text
next state = F(current state, input, timing)
```

Logic gates implement local transitions. Registers and memory preserve selected states across time. Clocks, synchronization, power, and cooling make those transitions usable at scale.

## Storage is a hierarchy

No single storage technology simultaneously provides the best latency, capacity, energy cost, density, persistence, and price. Systems therefore compose layers:

```text
registers
→ caches
→ DRAM / HBM
→ SSD
→ remote storage
```

Each layer keeps the current working set close enough to computation while preserving a larger backing state elsewhere.

## Virtual memory separates logical and physical placement

Virtual memory gives a process a stable logical address space while the operating system maps pages to physical memory. Page tables, TLBs, demand paging, shared pages, and copy-on-write let logical identity persist even when physical placement changes.

This pattern generalizes beyond byte-addressed memory:

```text
stable logical object
+ dynamic physical placement
+ page-in / page-out
+ locality-aware working set
```

## Model and Agent memory

A model system has several distinct memory forms:

| Layer | Typical lifetime | Function |
|---|---|---|
| Parameters | model version | learned statistical structure |
| KV cache | one active sequence | reusable inference state |
| Context | one cognitive episode | active working information |
| Task state | hours to days | progress, identities, waits, and attempts |
| Knowledge | long-lived | reusable explanations and models |
| Artifacts | long-lived | durable outputs and evidence |
| World state | external | the reality the Agent observes and changes |

Treating all of these as “context” loses their different identities, costs, and recovery semantics.

## Agent Context Virtual Memory

An Agent can be understood as operating over a logical cognitive address space. Relevant semantic pages are loaded into the model context; the larger task state remains in files, databases, artifacts, and runtime objects.

```text
logical task memory
→ select current working set
→ load into model context
→ reason and act
→ persist new facts and artifacts
```

Context thrashing occurs when the active working set is larger than the context or when relevant state is repeatedly evicted and reconstructed. Stable identities, summaries tied to source versions, and task-local artifacts reduce this cost.

## Design consequence

Persistent facts belong in durable state layers. Context acts as fast cognitive memory. A strong Agent system makes movement between the two explicit, just as a strong memory hierarchy makes movement between cache, memory, and storage explicit.

See the walkthrough chapters on [physical reality](../../studies/2026-computing-stack-walkthrough/00-physical-reality.md), [transistors and memory](../../studies/2026-computing-stack-walkthrough/01-transistors-and-memory.md), and [cache and virtual memory](../../studies/2026-computing-stack-walkthrough/04-cache-and-virtual-memory.md).
