# 07 — Downstream Interpreters and Injection

## Injection is interpretation transfer

A Web request often ends not at the application schema but at another
interpreter:

```text
HTTP and URL parser
→ framework parameter model
→ application string construction
→ SQL, shell, template, expression, regex, path, or code interpreter
```

Injection occurs when data intended as one value acquires delimiters, operators,
directives, or structure in the downstream language.

The most general relation is:

```text
upstream treats value as data
→ downstream parses same representation as syntax
→ attacker changes program meaning
```

## Typed APIs versus string composition

The strongest classical defense is to preserve structure:

- parameterized queries;
- argument arrays instead of shell command strings;
- typed templates with contextual encoding;
- schema-validated structured messages;
- safe object construction rather than reflection from external names;
- capability APIs rather than dynamic code evaluation.

Escaping is interpreter- and context-specific. A value escaped for SQL string
syntax is not safe in a shell, HTML attribute, URL, JavaScript, or model prompt.

## Validation boundaries

CWE-20 recommends treating parsing as a distinct layer rather than scattering
it throughout a program, because inconsistent parsing creates weaknesses. [R14]

A robust boundary:

```text
raw input
→ one parser
→ typed value
→ schema and business validation
→ typed downstream API
```

A fragile boundary:

```text
raw string
→ partial filter
→ concatenation
→ decode or template expansion
→ another parser
```

## Query interpreters

Database query semantics can be changed when externally influenced input is
concatenated into query text. Parameter binding separates data values from query
structure, but identifiers, operators, sort expressions, or schema names may
still require allowlisted structured selection rather than ordinary value
parameters.

The security decision must apply to the actual query plan or typed query
structure sent to the database.

## Command interpreters

Process execution has at least two layers:

```text
program selection
argument vector
```

and, when a shell is invoked:

```text
shell language parse
expansion and substitution
program selection
argument vectors
```

Passing a single command string to a shell introduces another interpreter and
its metacharacters. Even without shell syntax, argument injection can change a
program's options if untrusted input is placed into an argument position the
program interprets as flags or subcommands.

## Template and expression interpreters

Templates combine data and executable or control syntax. Some templates compile
to code, permit method calls, resolve properties, include files, or execute
expressions. A “template value” is not necessarily inert.

Different contexts inside the same template require different output encoding.
Server-side and client-side rendering can parse the result again.

## Serialization and object construction

Serialization formats range from inert data encodings to object graphs carrying
type names, constructors, callbacks, or executable behavior. Deserializing data
from an untrusted source can invoke application classes or lifecycle hooks
outside the sender's intended data model.

Safer designs use restricted schemas, primitive data types, explicit type
registries, and no ambient constructor side effects.

## Regular expressions and resource semantics

A regex can become a resource-consumption interpreter when attacker-controlled
patterns or inputs trigger extreme processing. ReDoS is not a syntax-to-code
injection, but it follows the same principle that interpreter complexity and
input shape create unintended consequence.

## File and object paths

A validated URL path may later become:

- filesystem path;
- archive member path;
- object-store key;
- package name;
- module import;
- template include;
- cloud resource identifier.

Each target has different separators, normalization, symbolic-link, case, and
namespace rules. Reusing URL validation as filesystem authorization is unsafe.

## Model interpreter

An LLM introduces an open-ended natural-language interpreter:

```text
external data
→ model assigns task relevance and imperative meaning
→ model emits structured Tool proposal
→ Host or Tool broker admits proposal
→ deterministic executor acts
```

Unlike SQL or shell grammar, natural-language instruction boundaries are
probabilistic and contextual. The durable defense cannot rely only on escaping
special tokens.

The required separation is:

```text
evidence channel
instruction authority
Task and participant purpose
Tool capability
Effect admission
world verification
```

## Generated code and Tool construction

An Agent can respond to a missing capability by generating code that introduces
new interpreters or dependencies. This expands the chain:

```text
external input
→ cognitive interpretation
→ generated source
→ compiler or interpreter
→ dependency loaders
→ Runtime process
→ external Tool authority
```

Each transition needs source, build, dependency, test, scope, and Effect evidence.

## Multi-stage injection chain

```text
URL value passes gateway validation
→ framework decodes it differently
→ application inserts value into template
→ rendered output becomes HTML
→ browser constructs script-capable DOM
→ Agent reads page and invokes Tool
```

No single “injection category” captures all boundaries. The chain must preserve
each interpreter and authority transition.

## Defensive principles

- Remove unnecessary interpreters.
- Use typed APIs and parameter binding.
- Validate syntax and business semantics after domain parsing.
- Apply contextual output encoding at the final rendering boundary.
- Avoid dynamic evaluation, unrestricted reflection, and unsafe object
  construction.
- Treat paths and identifiers as domain-specific types.
- Build generated Tools in disposable, credential-empty environments.
- Test generated behavior against capability requirements before admission.
- Separate external evidence from model instruction authority.
- Verify deterministic Effects independently of model explanations.

## Evidence requirements

Record:

- every interpreter and version;
- source representation and typed output;
- transformation order;
- generated query, command argument vector, DOM, or AST where safe;
- identity and authority at execution;
- generated code and dependency digests;
- world Effect and residual state.

## Ordivon implication

Runtime owns compiler, process, file, and Artifact truth. Host owns semantic Task,
Context, ToolGrant, and Effect admission. World owns external capability and
results. Security owns adversarial chain interpretation. Ordivon should not build
a universal injection filter.
