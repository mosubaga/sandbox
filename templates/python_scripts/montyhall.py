#! /usr/bin/python3

"""
Monte‑Carlo simulation of the Monty Hall problem.
"""

import random
from collections import Counter
from typing import Tuple

# ----------------------------------------------------------------------
# Helper: simulate one game
# ----------------------------------------------------------------------
def monty_hall_one_game(switch: bool) -> bool:

    """
    Simulate a single Monty Hall round.

    Parameters
    ----------
    switch : bool
        If True, the contestant switches to the other unopened door after
        Monty reveals a goat.  If False, the contestant sticks with the original choice.

    Returns
    -------
    win : bool
        True if the contestant wins the car, False otherwise.
    """

    doors = [0, 1, 2]                # 0: car, 1&2: goats
    car_door = random.choice(doors)   # Monty knows where the car is

    # Contestant picks a door at random
    pick = random.choice(doors)

    # Monty opens one of the remaining doors that has a goat.
    # We build a list of possible doors he could open:
    remaining = [d for d in doors if d != pick and d != car_door]
    monty_opens = random.choice(remaining)

    # Determine the final choice after optional switch
    if switch:
        # Switch to the only unopened door that is not the original pick or Monty's door
        final_pick = next(d for d in doors if d not in (pick, monty_opens))
    else:
        final_pick = pick

    return final_pick == car_door


# ----------------------------------------------------------------------
# Monte‑Carlo experiment
# ----------------------------------------------------------------------
def run_experiment(n_games: int) -> Tuple[float, float]:

    """
    Run `n_games` simulations for both strategies.

    Returns
    -------
    win_rate_stay : float   # empirical probability of winning when staying
    win_rate_switch : float  # empirical probability of winning when switching
    
    """
    outcomes = Counter()

    for _ in range(n_games):
        # Stay strategy
        if monty_hall_one_game(switch=False):
            outcomes['stay'] += 1

        # Switch strategy
        if monty_hall_one_game(switch=True):
            outcomes['switch'] += 1

    win_rate_stay   = outcomes['stay']   / n_games
    win_rate_switch = outcomes['switch'] / n_games
    return win_rate_stay, win_rate_switch


# ----------------------------------------------------------------------
# Main block – run and display results
# ----------------------------------------------------------------------
if __name__ == "__main__":
    N_GAMES = 1_000_000     # adjust for higher precision

    stay, switch = run_experiment(N_GAMES)

    print(f"After {N_GAMES:,} simulated games:")
    print(f"  Stay   → Win rate: {stay:.6f} (theoretical ≈ 0.3333)")
    print(f"  Switch → Win rate: {switch:.6f} (theoretical ≈ 0.6667)")

    # Optional sanity check
    assert abs(stay - 1/3) < 0.002, "Stay win rate deviates from 1/3!"
    assert abs(switch - 2/3) < 0.002, "Switch win rate deviates from 2/3!"

