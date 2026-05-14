"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Jimmy Ly
Student ID:   130222219

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return (
        "- **Why a single shortest-path run from S is not enough:**\n"
        "  One run from `S` only fixes shortest-path distances *from* the entrance. It never "
        "chooses which relic to visit next and that sequence changes the total fuel even when "
        "every leg uses a shortest path between its endpoints.\n"
        "- **What decision remains after all inter-location costs are known:**\n"
        "  You still must pick a visit order for which relic comes first from `S`, which comes "
        "second from there, and so on, then the final leg to `T`, summing the precomputed "
        "corridor costs between those stops.\n"
        "- **Why this requires a search over orders (one sentence):**\n"
        "  Total fuel depends on the order in which relics are collected so the answer comes "
        "from comparing feasible orders (search), not from one shortest-path computation from "
        "`S` alone."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """
    _ = exit_node  # exit is not a Dijkstra source in README Part 2a; kept for API
    seen = set()
    out = []
    for x in [spawn] + list(relics):
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    TODO
    """
    nodes = set(graph.keys())
    for nbrs in graph.values():
        for v, _ in nbrs:
            nodes.add(v)
    nodes.add(source)

    dist = {u: float("inf") for u in nodes}
    dist[source] = 0.0
    pq = [(0.0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in graph.get(u, ()):
            nd = d + float(w)
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    TODO
    """
    dist_table = {}
    for s in select_sources(spawn, relics, exit_node):
        dist_table[s] = run_dijkstra(graph, s)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    return """### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):** `dist[v]` is the true cheapest cost to reach `v` from the source; no cheaper route exists once `v` is pulled from the heap and finalized.

- **For nodes not yet finalized (not in S):** `dist[u]` is the cheapest cost found so far using paths whose **internal** vertices (everything strictly between the source and `u`) are all already finalized.

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:** Only the source is finalized with distance `0`, and every other label is either `∞` or the weight of a single edge from the source, so every stored value matches a real path that uses no non-source internal vertices yet.

- **Maintenance : why finalizing the min-dist node is always correct:** The unfinalized node `x` with smallest tentative distance cannot still get a cheaper path through another unfinalized node, because **all edge weights are nonnegative**, so any other route to `x` would have to go through a vertex at least as expensive as `x` was when selected; therefore `dist[x]` is final and `x` can be added to the finalized set.

- **Termination : what the invariant guarantees when the algorithm ends:** Every reachable vertex has been finalized, so each `dist[v]` is the true shortest-path cost from the source; unreachable vertices stay at `∞`.

### Part 3c: Why This Matters for the Route Planner

If Dijkstra's distances are wrong, the planner's legs between landmarks use bad numbers, so it can pick a relic order that is not minimum fuel or think a corridor route exists when it does not."""


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    return """### Why Greedy Fails

- **The failure mode:** A greedy rule looks only at the **next** relic hop from the current chamber and does not budget for how expensive the **rest** of the tour can become after that choice.
- **Counter-example setup:** Use the handout graph with entrance `S`, relics `B`, `C`, `D`, exit `T`, and the corridor costs from the spec table (for example `S→B` costs `1`, while `S→C` and `S→D` each cost `2`).
- **What greedy picks:** A myopic planner can still follow the spec's **route 2** `S→C→B→D→T` (for example by exploring a bad branch first or using a fixed priority instead of comparing full tours), which totals **5** fuel in the illustration.
- **What optimal picks:** The spec's cheaper tour `S→B→D→C→T` visits every relic and ends at `T` with total fuel **4**.
- **Why greedy loses:** Picking the locally tempting first step can force longer middle legs later, so the **sum** of shortest-path legs for a bad first choice beats the global minimum over full **orders**.

### What the Algorithm Must Explore

- The planner must enumerate (directly or with search and pruning) different **order**s in which the relic chambers are visited before `T`, because the minimum total fuel depends on that permutation, not on one greedy next-relic decision."""


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    pass


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
