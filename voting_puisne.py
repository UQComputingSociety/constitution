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

duplicate = False
for b in ballots:
    if len(b) != len(set(b)):
        if not duplicate:
            print("Ballots with Duplicate Entries:")
            duplicate = True
        print("  ", b)
if duplicate:
    print()

candidates = sorted(set(i for j in ballots for i in j))
print(f"{len(candidates)} Candidates: {', '.join(candidates)}")
assert nominees == len(candidates)
print(f"{len(ballots)} Ballots")
print(f"{positions} Positions")
quota = len(ballots)/(positions + 1) + epsilon
print(f"Quota: {quota}")

elected = []
eliminated = []
tallies = [{'weight': 1.0, 'order': i} for i in ballots]
stage = 0

while len(elected) + len(candidates) > positions and len(elected) != positions:
    stage += 1
    if verbose:
        print(f"\nRound {stage}")

    # assign each vote to a candidate
    assignments = {c: [] for c in candidates}
    while tallies:
        vote = tallies.pop()
        # remove any elected or eliminated candidates
        for c in elected + eliminated:
            while c in vote['order']:
                vote['order'].remove(c)
        if vote['order']:
            assignments[vote['order'][0]].append(vote)

    kill = True
    minimum = quota
    dying = []
    progress = []

    # for each candidate, count up the number of votes
    # sorting so that candidates are shown elected in the right order (if verbose)
    for c in sorted(assignments.keys(), key=lambda x: (-sum(c['weight'] for c in assignments[x]), x)):
        score = sum(v['weight'] for v in assignments[c])
        progress.append((c, score))

        # if they score above quota, then elect them and return votes with reevaluated votes
        if score >= quota:
            kill = False
            elected.append(c)
            candidates.remove(c)
            if verbose:
                print(f"  Elected: {c}")
            while assignments[c]:
                vote = assignments[c].pop()
                vote['weight'] *= 1 - quota/score
                tallies.append(vote)
        # if they don't score above quota, return votes
        else:
            while assignments[c]:
                vote = assignments[c].pop()
                tallies.append(vote)

        # find the candidates with the minimum scores
        if score < minimum:
            dying = [c]
            minimum = score
        elif score == minimum:
            dying.append(c)

    if verbose and verbosier:
        print("  " + "; ".join(f"{p[0]}: {p[1]:.2f}" for p in sorted(progress, key=lambda x: -x[1])))

    # if someone was elected, move directly to the next round
    if not kill: continue

    # if eliminating candidates would leave insufficient remaining candidates, announce
    if len(elected) + len(candidates) - len(dying) < positions:
        print("Tie In Final Round")
        print("  " + "\n  ".join(e))
        for c in dying:
            eliminated.append(c)
            candidates.remove(c)
        break

    # eliminate candidates
    for c in dying:
        eliminated.append(c)
        candidates.remove(c)
        if verbose:
            print(f"  Eliminated: {c}")

# if candidates remain (who didn't score above quota)
if candidates:
    if len(elected) != positions:
        elected += candidates
        if verbose:
            print("\n" + "\n".join(f"Remainder: {c}" for c in candidates))
    else:
        eliminated += candidates
        if verbose:
            print("\n" + "\n".join(f"Removed: {c}" for c in candidates))

# announce winners
print("\nWinners:\n  " + "\n  ".join(sorted(elected)))
if len(elected) < positions:
    print("\n".join((positions - len(elected)) * ["  + Undetermined"]))
