# Reflection

**1. Which source would be easiest to integrate into a future pipeline, and why?**

customers.csv is the easiest to integrate. It is flat, structured, and has a clear candidate primary key (customer_id) with no nested structures that need to be resolved before it can even be described in a schema. orders.json and products.parquet both introduce extra decisions first - orders.json has a nested shipping object that must be flattened or restructured, and products.parquet requires a specific library (pyarrow) just to be opened at all.

**2. Which source presents the greatest schema or data-quality risk, and what evidence supports your answer?**

orders.json presents the greatest risk. Profiling showed that its shipping field is a nested Python object rather than a flat column, which even broke the straightforward `nunique()` distinct-value count until it was wrapped in error handling. That is concrete evidence that a naive JSON-to-table conversion could silently drop or mishandle that data. In addition, total_amount appeared to equal subtotal + shipping_fee in every sampled row without that relationship being documented anywhere, meaning a pipeline could either duplicate the calculation incorrectly or fail to notice if the source ever stops guaranteeing it.

**3. What could go wrong if a pipeline is built before the source schema and contract are understood?**

A pipeline built too early could silently drop the nested shipping fields during a naive conversion, load duplicate customer records because no uniqueness rule was ever enforced, or break outright when a field like customer_segment introduces a new, unanticipated value. These kinds of failures often do not surface immediately as a crash - they show up later as quietly incorrect analytics numbers, which are far more expensive to diagnose and fix than a loud pipeline failure would have been.

**4. How do Git, virtual environments, containers, and documentation improve reproducibility for a data-engineering team?**

Git records exactly which version of the code and schema produced a given result, so a teammate can check out the same commit and see precisely what changed and when. The virtual environment pins the exact Python package versions used, preventing "it works on my machine" issues caused by silently mismatched dependencies. Docker containers guarantee that every team member runs an identical PostgreSQL version and configuration rather than whatever happens to already be installed locally, which removes an entire category of environment-specific bugs. Finally, documentation - the lifecycle map, source inventory, and data contract produced in this lab - turns knowledge that would otherwise live only in one person's head into something a new team member, or a future version of the same person, can rely on without having to re-derive it from scratch months later.
