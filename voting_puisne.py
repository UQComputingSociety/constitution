positions = 3
verbose = True
verbosier = True
nominees = 7
epsilon = 0 # 1e-6

ballots = [
    ["Orange", "Pear"],
    ["Orange", "Pear"],
    ["Orange", "Pear"],
    
    ["Pear", "Strawberry", "Cake"],
    ["Pear", "Strawberry", "Cake"],
    ["Pear", "Strawberry", "Cake"],
    ["Pear", "Strawberry", "Cake"],
    ["Pear", "Strawberry", "Cake"],
    ["Pear", "Strawberry", "Cake"],
    ["Pear", "Strawberry", "Cake"],
    ["Pear", "Strawberry", "Cake"],
    
    ["Strawberry", "Orange", "Pear"],
    
    ["Cake", "Chocolate"],
    ["Cake", "Chocolate"],
    ["Cake", "Chocolate"],
    
    ["Chocolate", "Cake", "Burger"],
    
    ["Burger", "Chicken"],
    ["Burger", "Chicken"],
    ["Burger", "Chicken"],
    ["Burger", "Chicken"],
    
    ["Chicken", "Chocolate", "Burger"],
    ["Chicken", "Chocolate", "Burger"],
    ["Chicken", "Chocolate", "Burger"]
]

duplicate = []
for b in ballots:
    if len(b) != len(set(b)):
        duplicate.append(str(b))
if duplicate:
    print("Ballots with Duplicate Entries:\n  " + "\n  ".join(duplicate) + "\n")

candidates = set(i for j in ballots for i in j)
print(f"{len(candidates)} Candidates: {', '.join(sorted(candidates))}")
assert nominees == len(candidates)
print(f"{len(ballots)} Ballots")
print(f"{positions} Positions")
quota = len(ballots)/(positions + 1) + epsilon
print(f"Quota: {quota}")

elected = set()
eliminated = set()
tallies = [{'weight': 1.0, 'order': i} for i in ballots]
stage = 0

while len(elected) + len(candidates) > positions and len(elected) != positions:
    assert len(elected) + len(candidates) + len(eliminated) == nominees
    stage += 1
    if verbose:
        print(f"\nRound {stage}")

    # assign each vote to a candidate
    assignments = {c: [] for c in candidates}
    while tallies:
        vote = tallies.pop()
        # remove any elected or eliminated candidates
        vote["order"] = [i for i in vote["order"] if i in candidates]
        if vote['order']:
            assignments[vote['order'][0]].append(vote)

    kill = True
    minimum = quota
    dying = set()
    progress = {}

    # for each candidate, count up the number of votes
    # sorting so that candidates are shown elected in the right order (if verbose)
    for c in sorted(assignments.keys(), key=lambda x: (-sum(v['weight'] for v in assignments[x]), x)):
        score = sum(v['weight'] for v in assignments[c])
        progress[c] = score

        # if they score above quota, then elect them and return votes with reevaluated votes
        if score >= quota:
            kill = False
            elected.add(c)
            candidates.remove(c)
            if verbose:
                print(f"  Elected: {c}")
            for vote in assignments[c]:
                vote['weight'] *= 1 - quota/score
                tallies.append(vote)
        # if they don't score above quota, return votes to the tallies unchanged
        else:
            tallies.extend(assignments[c])

        # find the candidates with the minimum scores
        if score < minimum:
            dying = set([c])
            minimum = score
        elif score == minimum:
            dying.add(c)

    if verbose and verbosier:
        print("  " + "; ".join(f"{p}: {progress[p]:.2f}" for p in sorted(progress, key=progress.get, reverse=True)))

    # if someone was elected, move directly to the next round
    if not kill: continue

    # if eliminating candidates would leave insufficient remaining candidates, announce
    if len(elected) + len(candidates) - len(dying) < positions:
        print("Tie In Final Round")
        print("  " + "\n  ".join(dying))
        eliminated.update(dying)
        candidates.difference_update(dying)
        break

    # eliminate candidates
    if verbose:
        print("\n".join(f"  Eliminated: {c}" for c in dying))
    eliminated.update(dying)
    candidates.difference_update(dying)

# if candidates remain (who didn't score above quota)
if candidates:
    if len(elected) != positions:
        elected.update(candidates)
        if verbose:
            print("\n" + "\n".join(f"Remainder: {c}" for c in candidates))
    else:
        eliminated.update(candidates)
        if verbose:
            print("\n" + "\n".join(f"Removed: {c}" for c in candidates))

# announce winners
print("\nWinners:\n  " + "\n  ".join(sorted(elected)))
if len(elected) < positions:
    print("\n".join((positions - len(elected)) * ["  + Undetermined"]))
