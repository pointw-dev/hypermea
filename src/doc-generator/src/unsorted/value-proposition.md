# Value Proposition

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::


Plug. Play. Scale.
Stop hard-coding routes and rewriting clients. Hypermea lets you build APIs that explain themselves, so frontends can adapt without breaking.

Ready on Day One
Your service comes with secure defaults, HAL links, pagination, rate limiting, structured logs, and more—no config required.

Fast Start, Smooth Finish
Start building in seconds. Add advanced features like writable forms, embeddable resources, or link-based workflows only when you need them.

Built for Developers, Backed by Ops
Hypermea brings joy to developers and clarity to operations. Developer experience is elegant; DevOps experience is uncompromising.

Powered by Standards
Under the hood? HAL, RFCs, and ISO specs. Hypermea speaks fluent web so you don’t have to write a spec from scratch.




## The Problem
* APIs are brittle.
* Clients depend on out-of-band docs and hard-coded paths.
* Backend changes risk breaking frontends.

## The Solution

Hypermea makes hypermedia-first APIs practical, testable, and evolvable.


## What It Does

✅ Declarative resource modeling (Pydantic)
✅ HAL-compliant responses with links & forms
✅ Scaffold tools (hy resource create, hy link list)
✅ Version-aware pagination & concurrency
✅ Opt-in design—start simple, grow complex


## Why It Matters

* Clients explore via links, not brittle contracts.
* Hypermedia guides interaction, not static docs.
* Your API is testable, debuggable, and forward-compatible.


## Compare to alternatives

| Feature                      | Hypermea (HAL)                     | OpenAPI                        | GraphQL                           | JSON-RPC                   | 
|------------------------------|------------------------------------|--------------------------------|-----------------------------------|----------------------------|
| Client/Server Coupling       | Loose (hypermedia-driven)          | Tight (contract-first)         | Medium (typed schema)             | Tight                      |
| Discoverability              | ✅ via _links, _forms, affordances  | ❌ Clients need prior knowledge | ❌ Schema known, ops must be known | ❌ Hard-coded method names  |
| Runtime Evolvability         | ✅ Clients adapt by following links | ❌ Requires versioning          | ❌ Dependent on schema evolution   | ❌ Requires versioning      |
| Tooling for Devs             | ✅ CLI, Pydantic, HAL tooling       | ✅ Great editor support         | ✅ Great tooling & IDEs            | ⚠️ Minimal                 |
| Spec Format                  | HAL + affordance conventions       | OpenAPI YAML/JSON              | GraphQL SDL                       | Custom JSON-RPC protocol   |
| Forms / Writable Affordances | ✅ Supports method affordances      | ⚠️ Manual or via extensions    | ❌ No affordance concept           | ❌ No affordance concept    |
| Batching & Query Composition | ⚠️ Via link traversal patterns     | ❌ One route per operation      | ✅ Batching & nesting built-in     | ✅ Batching supported       |

