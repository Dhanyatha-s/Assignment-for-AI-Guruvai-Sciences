"""
======================
2. Event Scheduler
======================

can_attend_all:
    Sort the events by start time. Then walk through them one by one.
    If any event starts strictly before the previous event has ended,
    there is an overlap — return False. Adjacent events (end == start)
    are allowed per the spec.

min_rooms_required:
    every meeting as two separate timeline events:
    a "room needed" moment (start) and a "room freed" moment (end).
    Sort starts and ends independently, then use two pointers to sweep
    through time. Each time a new meeting starts before the earliest
    current meeting ends, we need an extra room. Each time a meeting
    ends before the next one starts, a room is freed. The highest
    simultaneous room count we ever reach is our answer.
"""
import heapq

def can_attend_all(events: list[tuple])->bool:

    if not events:
        return True
    
    sorted_events = sorted(events, key=lambda e:e[0])

    for i in range(1, len(sorted_events)):
        prev_end = sorted_events[i-1][1]
        curr_start = sorted_events[i][0]

        if curr_start < prev_end:
            return False
    
    return True

def min_rooms_required(events: list[tuple])-> int:

    if not events:
        return 0
    
    sorted_events = sorted(events, key = lambda e: e[0])
    min_heap = []

    for start, end in sorted_events:
        if min_heap and min_heap[0] <= start:
            heapq.heappop(min_heap) #earliest meeting finished reuse it's room

        # if not assign new or reused room to this event
        heapq.heappush(min_heap, end)

    return len(min_heap)

# --- Quick smoke tests ---
events1 = [(9, 10), (10, 11), (11, 12)]
print(can_attend_all(events1))       # True  — adjacent, no overlaps
print(min_rooms_required(events1))   # 1     — sequential, 1 room is enough

events2 = [(9, 11), (10, 12), (11, 13)]
print(can_attend_all(events2))       # False — (9,11) and (10,12) overlap
print(min_rooms_required(events2))   # 2     — peak of 2 concurrent meetings

events3 = [(9, 10), (9, 11), (9, 12)]
print(min_rooms_required(events3))   # 3     — all start at same time

