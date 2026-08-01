# 05 — Content Type, HTML, and Active Interpretation

## Data becomes dangerous when type changes

A server, browser, parser, and Agent may receive identical bytes but assign
different types:

```text
inert image or text
HTML document
script
style sheet
JSON or XML
archive
serialized object
model instruction
```

The type controls which grammar and capabilities become available.

## Declared and effective MIME type

HTTP Content-Type is intended to declare response media type. The WHATWG MIME
Sniffing Standard exists because servers have historically supplied incorrect
or missing types and browsers attempted to preserve compatibility by examining
content. Divergent sniffing behavior produced security implications when one
party intended low-privilege data and the browser treated it as active HTML or
script. [R09]

This is an indispensable compatibility/security tension:

```text
render legacy misconfigured content
vs.
respect the server's intended privilege boundary
```

## `nosniff` and explicit media types

For content that should remain inert, applications should send a correct media
type and use controls such as `X-Content-Type-Options: nosniff` where the Fetch
and MIME rules apply. RFC 9205 recommends explicit media types and shows
`nosniff`, restrictive Content Security Policy, cache, and referrer controls for
HTTP APIs whose content is not intended to become active in browsers. [R17]

These controls reduce type promotion. They do not protect against a compromised
same-origin script that already has permission to read and execute application
logic.

## Character encoding precedes tokenization

HTML bytes are decoded into characters before tokenization. The HTML Standard
states that invalid byte sequences must follow the Encoding Standard's precise
error behavior because differences can produce script injection vulnerabilities.
[R08]

The pipeline is:

```text
bytes
→ encoding selection
→ decoder and error recovery
→ character stream
→ HTML tokenizer
→ tree construction
→ script and active-content behavior
```

A sanitizer operating on characters decoded one way cannot safely authorize a
browser that decodes the original bytes another way.

## HTML error recovery is specified behavior

HTML accepts malformed historical content through detailed tokenizer and tree-
construction algorithms. Error recovery is not random, but it is complex and
context-sensitive. Security filters that approximate HTML with regular
expressions or a different parser can construct a tree different from the
browser's tree.

The relevant semantic object is the DOM and execution context produced by the
target browser parser, not the filter's token list.

## Parser states and embedded languages

HTML contains transitions into:

- script data;
- raw text;
- escapable raw text;
- attribute values;
- URLs;
- CSS;
- JavaScript;
- SVG and MathML integration points;
- templates and inert fragments.

Escaping correct for one context can be unsafe in another. “HTML-escape user
input” is incomplete unless the destination context is named.

## Mutation and re-parsing

Content can be parsed, serialized, mutated, and parsed again by:

- browser DOM APIs;
- sanitizers;
- template engines;
- rich-text editors;
- server-side DOM libraries;
- client frameworks;
- Agent-generated transformations.

A representation safe in one parse can become active after reserialization or
insertion into a different context.

## Multipart and nested content

Web requests and responses can contain multipart structures, archives, encoded
attachments, embedded documents, and format-specific metadata. Each nested layer
adds another parser and type boundary.

An antivirus, gateway, application, browser, and downstream processor can inspect
different nested objects or apply different decompression limits. The top-level
Content-Type does not describe every embedded interpreter.

## Content type versus model interpretation

Agent systems add a parallel type system:

```text
application sees text/plain evidence
model sees imperative natural language
Host may treat model output as candidate action
Tool may execute the resulting structured call
```

The bytes remain inert to the browser but active to the cognitive loop.

Therefore:

```text
browser-inert
≠ Agent-inert
```

Prompt injection is a semantic type confusion between evidence and instruction,
amplified when instruction selection is connected to authority.

## Attack-chain classes

### Upload becomes active content

```text
server accepts user-controlled file as low-privilege data
→ sends missing or incorrect media type
→ user agent sniffs active type
→ content executes in a privileged origin context
```

### Decoder differential

```text
filter decodes bytes using interpretation A
→ validates character stream A
→ browser decodes using interpretation B
→ browser tokenizer sees active syntax absent from A
```

### Sanitizer/browser tree differential

```text
sanitizer builds tree S
→ removes nodes considered active
→ output is serialized
→ browser builds different tree B
→ active context reappears
```

### Agent evidence/instruction confusion

```text
external document is valid inert content
→ model interprets embedded text as instruction
→ Host admits Tool proposal without Task-bound authority check
→ legitimate Tool produces world Effect
```

## Defensive principles

- Declare correct media types.
- Use `nosniff` and restrictive content policies for inert Web/API content.
- Standardize on UTF-8 and standards-defined decoder behavior.
- Parse and sanitize with a browser-compatible tree model.
- Escape or encode for the exact output context.
- Avoid parse/serialize cycles across different parser implementations.
- Isolate user-controlled active content on separate origins.
- Treat archives and nested formats as explicit recursive parser boundaries.
- Mark model-visible external content as evidence, not trusted instruction.
- Require separate Effect authorization after cognitive interpretation.

## Evidence requirements

Record:

- raw content digest and transfer decoding;
- declared and effective media type;
- encoding source and decoder revision;
- parser and sanitizer revisions;
- resulting DOM or typed structure;
- execution origin and browser context;
- model-visible representation and instruction labels;
- final Tool call and world Effect.

## Ordivon implication

World may own browser/provider content observations and resulting external
Effects. Runtime owns local parser and sanitizer executions. Host owns Context
classification and Effect admission. Security evaluates type confusion and
adaptive attack paths. No universal content sanitizer is admitted.
