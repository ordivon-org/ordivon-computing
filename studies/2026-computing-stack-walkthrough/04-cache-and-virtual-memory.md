# 04 — Cache and Virtual Memory

## Why caches exist

Processor execution is much faster than access to large off-chip memory. Caches keep recently used memory lines near the core.

Two forms of locality make this effective:

- **temporal locality** — recently used data is likely to be used again;
- **spatial locality** — nearby addresses are likely to be used together.

A cache lookup interprets an address through tag, set index, and line offset. Direct-mapped, fully associative, and set-associative organizations exchange lookup complexity for conflict behaviour.

## Writes and replacement

A write-through cache immediately propagates changes to the next level. A write-back cache marks a line dirty and writes it later when evicted. Replacement policies choose which resident line makes room for a new one.

Modern systems commonly use several levels:

```text
L1 → L2 → shared last-level cache → DRAM
```

Average access time depends on hit latency, miss probability, and the cost of reaching lower levels.

## Multicore coherence

Each core may cache a copy of the same memory line. Coherence protocols coordinate ownership and visibility so that writes eventually produce a consistent view of that line.

False sharing occurs when independent variables occupy the same cache line. Cores then exchange ownership even though the program’s logical data is independent.

Coherence answers how copies of one location relate. Memory consistency answers which order of different operations programs may observe. Atomics, acquire/release operations, and fences establish the ordering needed by concurrent algorithms.

## DRAM organization

DRAM is organized into channels, ranks, banks, rows, and columns. Accessing data in an already open row can be much cheaper than activating a different row. Controllers reorder requests and prefetch data to exploit locality and hide latency.

## Virtual memory

Programs use virtual addresses. The MMU translates them through page tables to physical memory. A TLB caches recent translations. A page fault transfers control to the operating system, which can allocate memory, load data, establish sharing, or reject the access.

Virtual memory provides:

- a stable per-process address space;
- relocation and isolation;
- demand allocation;
- shared mappings;
- copy-on-write;
- memory-mapped files.

## Context as a working set

Model context resembles a high-speed working set rather than permanent memory. Task artifacts, files, databases, and runtime state act as backing storage. The system chooses which semantic pages to load for the current reasoning step.

```text
large logical task state
→ select relevant pages
→ load context
→ reason
→ persist updated facts
```

When the active task repeatedly reloads and discards essential information, context thrashing appears.

## Workspace analogy

A versioned Workspace provides a stable logical state identity while physical files and worktrees implement it. Branching, copy-on-write, and later integration let several Attempts explore from one base without immediately mutating shared state.
