#!/usr/bin/env python3
import sys
import math


def inp():
    return sys.stdin.readline().strip()


def get_int():
    return int(inp())


def get_ints():
    return list(map(int, inp().split()))


def solve(n, lasers):
    # Sort lasers by position (ascending)
    lasers.sort(key=lambda x: x[0])
    
    # Find the rightmost laser position
    max_pos = lasers[-1][0]
    
    # The new laser will be placed just to the right of all existing lasers
    new_laser_pos = max_pos + 1
    
    # Instead of trying all possible power levels (which would be too many),
    # we only need to try power levels that make a difference
    # These are the powers that exactly reach different existing lasers
    power_levels = set()
    power_levels.add(0)  # Don't destroy any lasers
    
    for pos, _ in lasers:
        power_levels.add(new_laser_pos - pos)
    
    # Sort power levels for better iteration
    power_levels = sorted(list(power_levels))
    
    min_destroyed = n  # Initialize with worst case
    
    # Try each power level from the set
    for power in power_levels:
        # We only consider valid power levels
        if power < 0:
            continue
            
        # Count how many lasers are destroyed by the new laser
        destroyed_by_new = 0
        survived = []  # List of lasers that survive the new laser
        
        for pos, power_level in lasers:
            if new_laser_pos - pos <= power:
                destroyed_by_new += 1
            else:
                survived.append((pos, power_level))
        
        # If all lasers are destroyed by the new one, we're done
        if destroyed_by_new == n:
            min_destroyed = min(min_destroyed, n)
            continue
        
        # Now we need to simulate the chain reaction among the surviving lasers
        # Sort surviving lasers by position in descending order (right to left)
        survived.sort(reverse=True)
        
        # Track which lasers are still active after the chain reaction
        active = [True] * len(survived)
        total_destroyed = destroyed_by_new  # Start with ones destroyed by new laser
        
        # Activate each surviving laser from right to left
        for i in range(len(survived)):
            if active[i]:  # If this laser is still active
                pos_i, power_i = survived[i]
                # Check which other lasers it destroys
                for j in range(i + 1, len(survived)):
                    if active[j]:
                        pos_j, _ = survived[j]
                        if pos_i - pos_j <= power_i:  # Within destruction range
                            active[j] = False
                            total_destroyed += 1
        
        # Update minimum destroyed count
        min_destroyed = min(min_destroyed, total_destroyed)
    
    return min_destroyed


def main():
    n = get_int()
    lasers = []
    for _ in range(n):
        a, b = get_ints()
        lasers.append((a, b))
    
    result = solve(n, lasers)
    print(result)


if __name__ == '__main__':
    main()
