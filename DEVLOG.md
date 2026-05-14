# Development Log – The Torchbearer

**Student Name:** Jimmy Ly
**Student ID:** 130222219

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – 2026-05-13: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

First I will write Dijkstra and build the distance table between the start, relics, and exit. Then I will write the search that tries different orders to visit all relics and picks the cheapest total cost. I think pruning and the README variable-name table will be the trickiest parts. I will test with the auto-grader and a few tiny graphs I can check by hand.

---

## Entry 2 – 2026-05-14: Part 3 mix-up

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

For Part 3 in the README I first wrote that every node’s `dist` value is already the final shortest distance. That is only true for **finalized** nodes, not the ones still in the heap. I reread the invariant and fixed the bullet so unfinalized nodes mean “best path found so far using finalized nodes inside the path.” I also added **nonnegative weights** to the maintenance bullet like the spec asks. After that, Part 3 matched how Dijkstra actually works.

---

## Entry 3 – 2026-05-14: Parts 4–6 (search, state, pruning)

I wrote **Part 4** in the README about why a greedy next relic step can fail and why we must search different visit **orders** on the `S,B,C,D,T` style example. I copied that text into `explain_search()` so the file matches the README. For **Part 5** I filled the state table with the same names `_explore` uses (`current_loc`, `relics_visited_order`, `cost_so_far`, and `relics_remaining` as a `frozenset`). For **Part 6** I described the `best` list, the lower bound `cost_so_far + min_next`, and pruning only when `lb > best[0]` so we do not cut ties. I checked the graded comment in `_explore` against those bullets so they tell the same story.

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
