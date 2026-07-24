# 02 — CPU and ISA

## CPU as a state-transition machine

A minimal processor repeatedly applies:

```text
next architectural state
= F(current registers, instruction, memory input)
```

Its central components are:

- a program counter selecting the next instruction;
- instruction memory and decoding;
- a register file holding fast named state;
- an ALU for arithmetic and comparisons;
- data memory access;
- multiplexers choosing data paths;
- a control unit producing circuit signals.

## Instruction set architecture

The ISA is the machine contract between software and hardware. It defines instructions, registers, data types, addressing, exceptions, memory behaviour, and visible state.

A RISC-like instruction set may include:

```text
ADD   destination, source1, source2
ADDI  destination, source, immediate
LOAD  destination, address
STORE source, address
BRANCH condition, target
```

The compiler translates higher-level code into these instructions. Hardware translates each instruction into control signals, data movement, and gate transitions.

## Five conceptual stages

A simple processor can be understood through:

```text
IF  instruction fetch
ID  decode and register read
EX  arithmetic or address calculation
MEM memory access
WB  register write-back
```

For `addi x5, x6, 7`, the processor fetches the encoded instruction, identifies the operation and operands, reads `x6`, adds the immediate value, and writes the result into `x5`.

## Branches and control

A branch changes the program counter based on a condition. The processor selects between the sequential next address and a target address through control logic.

This simple choice becomes central in high-performance CPUs because the processor wants to fetch future instructions before the branch result is known.

## Source code to transistors

```text
C / Rust / another language
→ compiler IR
→ assembly
→ machine code
→ instruction decode
→ control signals
→ gates and wires
→ physical state changes
```

Each layer preserves the intended semantics while changing the representation and execution mechanism.

## CPU, GPU, and accelerators

A CPU favours low-latency control, irregular programs, and a small number of powerful cores. A GPU favours many regular parallel operations. Tensor accelerators further specialize dense matrix arithmetic and dataflow.

They are different scheduling and resource structures built over the same fundamentals of state, instruction, memory, and communication.

## Agent analogy

An Agent system may eventually expose an Effect-level ISA:

```text
open goal
→ structured task
→ Effect IR
→ Tool operation
→ world state update
```

The analogy is useful because an ISA is not the complete program. It is the stable contract through which many higher languages can control a machine.
