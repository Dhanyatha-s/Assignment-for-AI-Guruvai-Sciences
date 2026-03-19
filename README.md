# Data Structures & Systems Design — SE/ AI ENgineer - AI Agentic System Intern Assessment

**Name:** Dhanyatha S
**Email:** dhanyatha237.y@gmail.com

---

## Problem 1: LRU Cache Implementation

### Problem

Consider a browser that can only hold **3 tabs** in memory at once. When a 4th tab opens, it closes whichever tab has gone unused the longest — the **Least Recently Used** tab.

### Requirements

| # | Operation | Behaviour |
|---|-----------|-----------|
| 1 | `get(key)` | Return the value if found, else `-1`. Mark as recently used. |
| 2 | `put(key, value)` | Add or update the key-value pair. |
| 3 | Eviction | If at capacity, evict the least recently used item first. |
| 4 | **Critical** | Both `get` and `put` must run in **O(1)** time. |

### Solution

A naive approach (array or single structure) requires O(n) to search or reorder nodes. The optimal solution combines **two structures**:

| Structure | Role |
|-----------|------|
| **HashMap** | Instant O(1) key lookup — no searching |
| **Doubly Linked List** | Tracks usage order and allows O(1) removal from any position |

```
HEAD [Most Recently Used] ←→ [B] ←→ [A] [Least Recently Used] TAIL
```

- `get(key)` → HashMap finds the node instantly → move it to the front
- `put(key, value)` → Insert at front → if over capacity, remove from tail

**Why neither works alone:**
- HashMap alone → no ordering, cannot identify LRU
- Linked List alone → O(n) to find a key by scanning

**Together** → HashMap handles fast lookup, Doubly Linked List handles ordering and eviction — both O(1).

### Code

> 📎 [View LRU Cache Implementation →]([https://github.com/Dhanyatha-s/Assignment-for-AI-Guruvai-Sciences/blob/main/lru_cache_implememtation.py)]

---

## Problem 2: Event Scheduler

### Problem

Design a scheduling system for a meeting platform that can:
1. Check if **one person** can attend all meetings without time conflicts
2. Find the **minimum number of rooms** needed to run all meetings simultaneously

### Requirements

| Function | Behaviour |
|----------|-----------|
| `can_attend_all(events)` | `True` if no overlaps, `False` otherwise |
| `min_rooms_required(events)` | Returns minimum concurrent rooms needed |

> **Note:** Adjacent events where `end_time == next start_time` are **not** considered overlaps.

### Solution

**`can_attend_all`** — Sort events by start time, then do one linear pass checking each consecutive pair. If any event starts before the previous one ends → overlap → return `False`.

**`min_rooms_required`** — Use a **min-heap** storing end times of active meetings. For each new meeting:
- If the earliest-ending meeting has already finished → reuse that room (pop heap)
- Otherwise → allocate a new room (push to heap)

The **peak heap size** = minimum rooms required.

Both functions: **Time O(n log n)** — sorting dominates. O(n log n) is optimal because comparing events requires time order, and comparison-based sorting cannot do better.

### Code

> 📎 [View Event Scheduler Implementation →]([https://github.com/Dhanyatha-s/Assignment-for-AI-Guruvai-Sciences/blob/main/even_scheduler.py])

---

## Final Discussion & Analysis

### 1. Time & Space Complexity

#### LRU Cache

| Function | Time | Space | Why |
|----------|------|-------|-----|
| `get(key)` | O(1) | O(1) | HashMap lookup + 2 pointer rewires |
| `put(key, value)` | O(1) | O(1) | Insert at front, remove tail if needed — no loops |
| `_remove(node)` | O(1) | O(1) | Rewires `prev.next` and `next.prev` — fixed operations |
| Overall storage | — | O(capacity) | HashMap + list are both bounded by capacity |

#### Event Scheduler

| Function | Time | Space | Why |
|----------|------|-------|-----|
| `can_attend_all` | O(n log n) | O(n) | Sort + one linear pass; space for sorted copy |
| `min_rooms_required` | O(n log n) | O(n) | Sort + n heap push/pops at O(log n) each; heap holds at most n end times |

---

### 2. Trade-offs: HashMap + Doubly Linked List

| Structure | Lookup | Order tracking | Eviction |
|-----------|--------|---------------|----------|
| HashMap alone | O(1) | ✗ Not possible | ✗ Must scan all entries |
| Linked List alone | O(n) scan | O(1) | O(1) |
| **HashMap + DLL** | **O(1)** | **O(1)** | **O(1)** |

Key point: a **doubly** linked list is required (not singly) because removing a node needs a reference to its previous node — which only a doubly linked list provides in O(1).

---

### 3. Future Proofing — Assigning Room Names

The current implementation counts rooms. To assign names like `"Room A"`, `"Room B"`:

1. **Pool** — maintain a queue of available room names: `["Room A", "Room B", ...]`
2. **Heap** — store `(end_time, room_name)` pairs instead of just end times; when a meeting ends, its room name returns to the pool
3. **Record** — store `event → room_name` in a dictionary for lookup

No change to time complexity — still O(n log n).

---

### 4. Concurrency — Making LRU Cache Thread-Safe

The current implementation is **not thread-safe**. Two threads calling `get()` or `put()` simultaneously can corrupt the linked list (e.g. both writing to `head.next` at once).

**Three approaches:**

| Approach | How | Trade-off |
|----------|-----|-----------|
| Coarse lock *(recommended)* | Wrap `get()` and `put()` in `threading.Lock()` | Simple and correct; one thread at a time |
| Read-write lock | Separate read/write locks | Better throughput, but `get()` still mutates order so benefit is limited |
| Fine-grained / sharded | Split cache into N shards, each with its own lock | High throughput, complex to implement |

**Simplest correct implementation:**

```python
import threading

# in __init__:
self.lock = threading.Lock()

# in get() and put():
with self.lock:
    # existing logic
```

---

*Assessment submission — Dhanyatha S*
