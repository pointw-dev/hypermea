# Principles

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

* batteries-included
* quick start - settings have sensible defaults
* production ready - devops first
* developer ergonomics matter
* standards based
* opt-in sophistication

# Hypermea Design Principles

## ✅ 1. Standards-Based by Default
**Favor existing standards over inventing new ones.**  
Hypermea adheres strictly to well-established specifications—HAL for hypermedia, ISO 8601 for dates and durations, RFC 7235 for authentication, and more. This commitment ensures predictable behavior, better interoperability, and smoother onboarding for developers already familiar with the web’s foundations.

## � 2. Batteries Included
**Everything you need is already here.**  
From resource modeling and link generation to pagination, rate limiting, structured logging, and request validation—Hypermea equips developers with a powerful toolkit that anticipates real-world needs. Think of it as a well-stocked utility belt: you rarely need to reach outside it.

## ⚡ 3. Instant Start, Zero Configuration
**Run first, configure later.**  
Every service scaffolded by Hypermea runs immediately with sensible defaults—no `.env`, no database setup, no required configuration. Customization is always possible, but never a barrier to entry.

## � 4. Production-Ready Out of the Box
**Built-in support for real-world ops.**  
Structured logs, secure defaults, concurrency control, graceful error handling, and HTTP-compliant rate limiting are not afterthoughts—they’re foundational. A Hypermea service is ready for production from its first boot.

## �‍� 5. Developer Ergonomics Matter
**Tools should bring joy, not friction.**  
Hypermea prioritizes a frictionless developer experience—clear error messages, predictable behaviors, Pydantic models instead of verbose schemas, scaffolded code generation, and powerful CLI tools. It’s designed for flow state.

## � 6. Opt-In Sophistication
**Start simple. Scale when you need it.**  
Hypermea services begin minimal by design. Advanced features—form affordances, resource embedding, concurrency control—can be added as needed, keeping deployments lean and reducing cognitive load.

## � 7. DevOps First
**Infrastructure is not an afterthought.**  
When trade-offs arise between developer convenience and operational clarity, Hypermea chooses the path that enables monitoring, scaling, deployment, and observability—even if it means adding one more line of code to your model.

## � 8. Hypermedia is the Contract
**The client learns as it goes.**  
Hypermea uses links, forms, and typed affordances as a living contract between client and server. This enables clients to adapt dynamically and reduces the risk of brittle integrations.

## � 9. Evolvability Over Stability
**Avoid versioning by avoiding tight coupling.**  
By designing around runtime discovery and affordance-based interaction, Hypermea avoids the pitfalls of breaking changes. Clients evolve naturally by following the links.

## � 10. Layered Simplicity
**Simple at the surface, powerful underneath.**  
The architecture favors clean, declarative code—one concept per file, one file per concept. Beneath that, powerful mechanisms (like Pydantic validation or Cerberus fallbacks) are abstracted away unless explicitly needed.
