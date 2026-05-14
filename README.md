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

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):** `dist[v]` is the true cheapest cost to reach `v` from the source; no cheaper route exists once `v` is pulled from the heap and finalized.

- **For nodes not yet finalized (not in S):** `dist[u]` is the cheapest cost found so far using paths whose **internal** vertices (everything strictly between the source and `u`) are all already finalized.

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:** Only the source is finalized with distance `0`, and every other label is either `∞` or the weight of a single edge from the source, so every stored value matches a real path that uses no non-source internal vertices yet.

- **Maintenance : why finalizing the min-dist node is always correct:** The unfinalized node `x` with smallest tentative distance cannot still get a cheaper path through another unfinalized node, because **all edge weights are nonnegative**, so any other route to `x` would have to go through a vertex at least as expensive as `x` was when selected; therefore `dist[x]` is final and `x` can be added to the finalized set.

- **Termination : what the invariant guarantees when the algorithm ends:** Every reachable vertex has been finalized, so each `dist[v]` is the true shortest-path cost from the source; unreachable vertices stay at `∞`.

### Part 3c: Why This Matters for the Route Planner

If Dijkstra's distances are wrong, the planner's legs between landmarks use bad numbers, so it can pick a relic order that is not minimum fuel or think a corridor route exists when it does not.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** A greedy rule looks only at the **next** relic hop from the current chamber and does not budget for how expensive the **rest** of the tour can become after that choice.
- **Counter-example setup:** Use the handout graph with entrance `S`, relics `B`, `C`, `D`, exit `T`, and the corridor costs from the spec table (for example `S→B` costs `1`, while `S→C` and `S→D` each cost `2`).
- **What greedy picks:** A myopic planner can still follow the spec's **route 2** `S→C→B→D→T` (for example by exploring a bad branch first or using a fixed priority instead of comparing full tours), which totals **5** fuel in the illustration.
- **What optimal picks:** The spec's cheaper tour `S→B→D→C→T` visits every relic and ends at `T` with total fuel **4**.
- **Why greedy loses:** Picking the locally tempting first step can force longer middle legs later, so the **sum** of shortest-path legs for a bad first choice beats the global minimum over full **orders**.

### What the Algorithm Must Explore

- The planner must enumerate (directly or with search and pruning) different **order**s in which the relic chambers are visited before `T`, because the minimum total fuel depends on that permutation, not on one greedy next-relic decision.

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
