"""
In many of the tournament classes we use the same ideas again and again:
- We keep data about the players (strategies) inside dictionaries.
  For example: {"wins": 0, "losses": 0, "points": 0}.

- In every match, we play two strategies and compare their results.
  If one ratio is higher → this player wins.
  If equal → it is a draw.

- After the game we update the dictionary of each player:
  add +1 win, +1 loss, +1 draw, or +3 / +1 points.

- We also keep a "log" list to remember all games.
  Each log entry is a dictionary with information about match number, players, ratios and the winner.

- At the end of the tournament we print or return the final results,
  like standings table, champion name, or bracket.

This way all tournaments share the same logic:
1. loop over games,
2. check conditions,
3. update stats,
4. save history,
5. show final output.
"""

import csv #save in a csv file
import random
from Game import Game
from strategy import BaseStrategy, Automatic_BaseStrategy, N_max_strategy, More_then_N_percent_group_strategy

"""
This class is the father class that creates the term tournament, and implements functions that will
be used in each of his sub classes
"""
class Tournament:
    def __init__(self, strategies):
        self.strategies = strategies
        self.log = []

    def run(self):
        pass

    #this function is the father function, it saves log of the tournament in a csv file
    def save_log_csv(self, filename="tournament_log.csv"):
        if not self.log:
            return
        keys = self.log[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.log)


"""
DeathMatchTournament – two players play again and again
until one of them reaches the win_goal number of wins.
This is a simple "first to X wins" style tournament.
"""
class DeathMatchTournament(Tournament):
    def __init__(self, strategies, win_goal=5):
        super().__init__(strategies)
        self.win_goal = win_goal # number of wins required to be champion

    def run(self):
        # let both players choose strategies
        strategy_classes = [
            BaseStrategy,
            Automatic_BaseStrategy,
            N_max_strategy,
            More_then_N_percent_group_strategy
        ]

        # player 1 chooses strategy
        print("player 1-choose strategy: [0-3]")
        for i in range(len(strategy_classes)):
            print(f"{i}: {strategy_classes[i].__name__}")
        choice1 = int(input("הכנס מספר (0-3): "))
        s1 = strategy_classes[choice1]([])

        # player 2 chooses strategy
        print("player 2-choose strategy: [0-3]")
        for i in range(len(strategy_classes)):
            print(f"{i}: {strategy_classes[i].__name__}")
        choice2 = int(input("הכנס מספר (0-3): "))
        s2 = strategy_classes[choice2]([])

        self.strategies = [s1, s2]
        wins = {s1.display(): 0, s2.display(): 0} # win counter
        match_no = 1

        # keep playing until someone reaches the goal
        while max(wins.values()) < self.win_goal:
            r1 = Game(s1).play()
            r2 = Game(s2).play()

            if r1.ratio > r2.ratio:
                winner = s1.display()
                wins[winner] += 1
            elif r2.ratio > r1.ratio:
                winner = s2.display()
                wins[winner] += 1
            else:
                winner = "draw"

            # save log for this match
            entry = {
                "match": match_no,
                "s1_name": s1.display(),
                "s2_name": s2.display(),
                "s1_selected_amount": r1.selected_amount,
                "s2_selected_amount": r2.selected_amount,
                "s1_ratio": r1.ratio,
                "s2_ratio": r2.ratio,
                "winner": winner
            }
            self.log.append(entry)
            print(f"[DeathMatch {match_no}] {s1.display()} vs {s2.display()} -> {winner}")
            match_no += 1

        # return tournament result
        winner = max(wins, key=wins.get)
        return {"winner": winner, "wins": wins, "history": self.log}


"""
RoundRobinTournament – each strategy plays against all the others
in a round-robin style. Win = 3 points, Draw = 1 point, Loss = 0.
"""
class RoundRobinTournament(Tournament):
    def __init__(self, strategies, rounds=1):
        super().__init__(strategies)
        self.rounds = rounds

    def run(self):
        points = {}
        for s in self.strategies:
            points[s.display()] = 0

        match_no = 1

        for r in range(self.rounds):
            print(f"\n Round {r+1} ")
            for i in range(len(self.strategies)):
                for j in range(i+1, len(self.strategies)):
                    s1, s2 = self.strategies[i], self.strategies[j]
                    r1 = Game(s1).play()
                    r2 = Game(s2).play()

                    if r1.ratio > r2.ratio:
                        points[s1.display()] += 3
                        winner = s1.display()
                    elif r2.ratio > r1.ratio:
                        points[s2.display()] += 3
                        winner = s2.display()
                    else:
                        points[s1.display()] += 1
                        points[s2.display()] += 1
                        winner = "draw"

                    entry = {
                        "match": match_no,
                        "round": r+1,
                        "s1_name": s1.display(),
                        "s2_name": s2.display(),
                        "s1_selected_amount": r1.selected_amount,
                        "s2_selected_amount": r2.selected_amount,
                        "s1_ratio": r1.ratio,
                        "s2_ratio": r2.ratio,
                        "winner": winner
                    }
                    self.log.append(entry)
                    print(f"[RR R{r+1} M{match_no}] {s1.display()} vs {s2.display()} -> {winner}")
                    match_no += 1

        return {"standings": points, "history": self.log}


"""
EliminationTournament – classic knockout tournament.
If there is an odd number of players, one gets a free pass (bye).
The loser is out, the winner continues until only one champion remains.
"""
class EliminationTournament(Tournament):
    def __init__(self, seed):
        super().__init__(seed)

    def run(self):
        round_no = 1
        players = self.strategies[:]
        bracket = []

        while len(players) > 1:
            print(f"\n--- Round {round_no} ---")
            next_round = []
            i = 0


            if len(players) % 2 == 1:
                bye_player = players[0]
                next_round.append(bye_player)
                print(f"{bye_player.display()} gets a BYE to next round")
                players = players[1:]


            while i < len(players):
                s1, s2 = players[i], players[i+1]
                r1 = Game(s1).play()
                r2 = Game(s2).play()

                if r1.ratio > r2.ratio:
                    winner, loser = s1, s2
                elif r2.ratio > r1.ratio:
                    winner, loser = s2, s1
                else:
                    winner, loser = random.choice([(s1, s2), (s2, s1)])

                next_round.append(winner)

                entry = {
                    "round": round_no,
                    "s1": s1.display(),
                    "s2": s2.display(),
                    "s1_ratio": r1.ratio,
                    "s2_ratio": r2.ratio,
                    "winner": winner.display(),
                    "loser": loser.display()
                }
                self.log.append(entry)
                print(f"{s1.display()} vs {s2.display()} -> {winner.display()}")

                i += 2

            players = next_round
            round_no += 1
            bracket.append([p.display() for p in players])

        champion = players[0].display()
        print(f"Champion: {champion}")
        return {"winner": champion, "bracket": bracket, "history": self.log}


"""
LeagueTournament – full league with home and away games.
Each team plays twice against every other team. Points are saved in table.
"""
class LeagueTournament(Tournament):
    def __init__(self, strategies):
        super().__init__(strategies)
        self.table = {}
        for s in strategies:
            self.table[s.display()] = {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "points": 0
            }

    def run(self):
        match_no = 1

        for i in range(len(self.strategies)):
            for j in range(i + 1, len(self.strategies)):
                for round_type in ["home", "away"]:
                    s1, s2 = self.strategies[i], self.strategies[j]
                    r1 = Game(s1).play()
                    r2 = Game(s2).play()

                    if r1.ratio > r2.ratio:
                        winner, loser = s1, s2
                        self.table[winner.display()]["wins"] += 1
                        self.table[loser.display()]["losses"] += 1
                        self.table[winner.display()]["points"] += 3
                        result = winner.display()
                    elif r2.ratio > r1.ratio:
                        winner, loser = s2, s1
                        self.table[winner.display()]["wins"] += 1
                        self.table[loser.display()]["losses"] += 1
                        self.table[winner.display()]["points"] += 3
                        result = winner.display()
                    else:
                        self.table[s1.display()]["draws"] += 1
                        self.table[s2.display()]["draws"] += 1
                        self.table[s1.display()]["points"] += 1
                        self.table[s2.display()]["points"] += 1
                        result = "draw"

                    self.table[s1.display()]["games"] += 1
                    self.table[s2.display()]["games"] += 1

                    entry = {
                        "match": match_no,
                        "s1": s1.display(),
                        "s2": s2.display(),
                        "s1_ratio": r1.ratio,
                        "s2_ratio": r2.ratio,
                        "winner": result
                    }
                    self.log.append(entry)

                    print(f"[League M{match_no}] {s1.display()} vs {s2.display()} -> {result}")
                    match_no += 1

        print("Final League Table:")
        for team, stats in self.table.items():
            print(team, stats)

        return {"table": self.table, "history": self.log}


"""
ChampionshipTournament – group stage followed by playoffs.
First, strategies are split into groups. Each group plays round-robin.
Top 2 from each group go to playoffs. Playoffs continue until champion.
"""
class ChampionshipTournament(Tournament):
    def __init__(self, strategies, groups_count=2):
        super().__init__(strategies)
        self.groups_count = groups_count
        self.groups = {}
        self.playoffs = []
        self.champion = None

    def run(self):
        self.groups = self._split_into_groups(self.strategies, self.groups_count)
        print("\n Group Stage")
        group_results = {}

        for group_name, players in self.groups.items():
            print(f"\nGroup {group_name}:")
            table = {}
            for player in players:
                table[player.display()] = {"points": 0, "wins": 0, "losses": 0, "draws": 0}

            for i in range(len(players)):
                for j in range(i + 1, len(players)):
                    s1, s2 = players[i], players[j]
                    r1, r2 = Game(s1).play(), Game(s2).play()

                    if r1.ratio > r2.ratio:
                        table[s1.display()]["points"] += 3
                        table[s1.display()]["wins"] += 1
                        table[s2.display()]["losses"] += 1
                        winner = s1.display()
                    elif r2.ratio > r1.ratio:
                        table[s2.display()]["points"] += 3
                        table[s2.display()]["wins"] += 1
                        table[s1.display()]["losses"] += 1
                        winner = s2.display()
                    else:
                        table[s1.display()]["points"] += 1
                        table[s2.display()]["points"] += 1
                        table[s1.display()]["draws"] += 1
                        table[s2.display()]["draws"] += 1
                        winner = "draw"

                    print(f" {s1.display()} vs {s2.display()} -> {winner}")

            group_results[group_name] = table

        qualified = []
        for group_name, table in group_results.items():
            sorted_table = sorted(table.items(), key=lambda item: item[1]["points"], reverse=True)
            top2 = []
            for player_name, stats in sorted_table[:2]:
                top2.append(player_name)
            qualified.extend(top2)
            print(f"\nTop 2 from Group {group_name}: {top2}")

        print("\nPlayoffs ")
        while len(qualified) > 1:
            next_round = []
            for i in range(0, len(qualified), 2):
                s1_name = qualified[i]
                s2_name = qualified[i + 1]
                s1 = self.find_strategy(s1_name)
                s2 = self.find_strategy(s2_name)

                r1, r2 = Game(s1).play(), Game(s2).play()
                if r1.ratio > r2.ratio:
                    winner = s1.display()
                elif r2.ratio > r1.ratio:
                    winner = s2.display()
                else:
                    winner = s1.display()

                self.playoffs.append((s1.display(), s2.display(), winner))
                print(f"{s1.display()} vs {s2.display()} -> {winner}")
                next_round.append(winner)

            qualified = next_round

        self.champion = qualified[0]
        print(f"\nChampion: {self.champion}")
        return {
            "groups": group_results,
            "playoffs": self.playoffs,
            "champion": self.champion
        }

    def _split_into_groups(self, strategies, groups_count):
        groups = {}
        group_size = len(strategies) // groups_count
        if len(strategies) % groups_count != 0:
            group_size += 1  # אם לא מתחלק שווה – מוסיפים עוד אחד

        index = 0
        for g in range(groups_count):
            group_name = chr(ord('A') + g)
            groups[group_name] = []
            for i in range(group_size):
                if index < len(strategies):
                    groups[group_name].append(strategies[index])
                    index += 1
        return groups

    def find_strategy(self, name):
        for s in self.strategies:
            if s.display() == name:
                return s
        return None
