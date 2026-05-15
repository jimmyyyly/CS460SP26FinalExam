# Development Log – The Torchbearer

**Student Name:** Jimmy Ly
**Student ID:** 130222219

---

## Entry 1 – 2026-05-13: Initial Plan

First I will write Dijkstra and build the distance table between the start, relics, and exit. Then I will write the search that tries different orders to visit all relics and picks the cheapest total cost. I think pruning and the README variable-name table will be the trickiest parts. I will test with the auto-grader and a few tiny graphs I can check by hand.

---

## Entry 2 – 2026-05-14: Part 3 mix-up

For Part 3 in the README I first wrote that every node’s `dist` value is already the final shortest distance. That is only true for **finalized** nodes, not the ones still in the heap. I reread the invariant and fixed the bullet so unfinalized nodes mean “best path found so far using finalized nodes inside the path.” I also added **nonnegative weights** to the maintenance bullet like the spec asks. After that, Part 3 matched how Dijkstra actually works.

---

## Entry 3 – 2026-05-14: Parts 4–6 (search, state, pruning)

I wrote **Part 4** in the README about why a greedy next relic step can fail and why we must search different visit **orders** on the `S,B,C,D,T` style example. I copied that text into `explain_search()` so the file matches the README. For **Part 5** I filled the state table with the same names `_explore` uses (`current_loc`, `relics_visited_order`, `cost_so_far`, and `relics_remaining` as a `frozenset`). For **Part 6** I described the `best` list, the lower bound `cost_so_far + min_next`, and pruning only when `lb > best[0]` so we do not cut ties. I checked the graded comment in `_explore` against those bullets so they tell the same story.

---

## Entry 4 – 2026-05-14: Post-Implementation Reflection

With more time I would try a **stronger lower bound** for pruning (for example accounting for more than one future leg or a cheaper estimate toward the exit), because `cost_so_far + min_next` is safe but weak on bigger instances. I would also cache the **best partial cost so far** for each pair `(current_loc, frozenset(relics_remaining))` so if the same situation shows up again with higher fuel, that branch can stop early. Finally I would add a few more **hand tests** (duplicate relic ids, empty relic list, spawn equal to a relic) to match edge cases the auto-grader might use.

---

## Final Entry – 2026-05-18: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 1 |
| Part 2: Precomputation Design | 2 |
| Part 3: Algorithm Correctness | 2 |
| Part 4: Search Design | 1 |
| Part 5: State and Search Space | 1 |
| Part 6: Pruning | 1 |
| Part 7: Implementation | 4.5 |
| README and DEVLOG writing | 2 |
| **Total** | **14.5** |
