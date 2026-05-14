# The Torchbearer

**Student Name:** Jimmy Ly
**Student ID:** 130222219
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  One run from `S` only fixes shortest-path distances *from* the entrance. It never chooses which relic to visit next and that sequence changes the total fuel even when every leg uses a shortest path between its endpoints.

- **What decision remains after all inter-location costs are known:**
  You still must pick a visit order for which relic comes first from `S`, which comes second from there, and so on, then the final leg to `T`, summing the precomputed corridor costs between those stops.

- **Why this requires a search over orders (one sentence):**
  Total fuel depends on the order in which relics are collected so the answer comes from comparing feasible orders (search), not from one shortest-path computation from `S` alone.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

- **Entrance (`spawn`):** Every valid route begins at `S`, so we need shortest-path costs from the entrance to every other landmark.
- **Relic chamber (each distinct relic in `relics`):** After a relic is collected, the next corridor leg starts at that chamber, so we need shortest-path costs from each distinct relic node to the others and to `T`.

| Source Node Type | Why it is a source |
|---|---|
| Entrance (`spawn`) | Supplies `dist(spawn, ·)` for the first relic the Torchbearer chooses in any order. |
| Relic chamber (each distinct node in `relics`) | Supplies `dist(relic, ·)` for every later leg, because `current_loc` is always `spawn` or a relic already visited before the final hop to `T`. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested `dict` (`dist_table`) |
| What the keys represent | Outer key = source node `u`; inner key = destination node `v` |
| What the values represent | Shortest-path cost from `u` to `v` (a `float`; `inf` if unreachable) |
| Lookup time complexity | O(1) expected per lookup |
| Why O(1) lookup is possible | Python `dict` maps keys by hashing, so one `dist_table[u][v]` access is average-case constant time for fixed landmark sets |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** One per distinct node returned by `select_sources` (the distinct nodes in `{spawn} ∪ relics`), which is at most `k + 1` when `k` counts distinct relic chambers and `spawn` is not one of them.
- **Cost per run:** `O(m log n)` with `n = |V|` and `m = |E|`, as given in the spec for one Dijkstra with a binary heap.
- **Total complexity:** `O(σ · m log n)` where `σ` is the number of distinct sources (at most `k + 1`); same order as `O(k m log n)` when `k` is the dominant term.
- **Justification (one line):** Each source run relaxes every edge in the worst case, and we repeat that once per landmark source we keep in `select_sources`.

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  _Your answer here._

- **For nodes not yet finalized (not in S):**
  _Your answer here._

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  _Your answer here._

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Your answer here._

- **Termination : what the invariant guarantees when the algorithm ends:**
  _Your answer here._

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

_Your answer here._

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Your answer here._
- **Counter-example setup:** _Your answer here._
- **What greedy picks:** _Your answer here._
- **What optimal picks:** _Your answer here._
- **Why greedy loses:** _Your answer here._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
