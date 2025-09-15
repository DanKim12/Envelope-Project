class Game:
    def __init__(self, strategy):
        self.strategy = strategy

    def play(self):
        before_count = len(self.strategy.envelopes)
        self.strategy.play()

        after_count = len(self.strategy.envelopes)
        opened_count = before_count - after_count

        if self.strategy.selected_envelope:
            selected_amount = self.strategy.selected_envelope.get_amount()
        else:
            selected_amount = 0

        max_amount = 0
        for e in self.strategy.envelopes:
            if e.get_amount() > max_amount:
                max_amount = e.get_amount()

        if self.strategy.selected_envelope and self.strategy.selected_envelope.get_amount() > max_amount:
            max_amount = self.strategy.selected_envelope.get_amount()

        return GameResult(selected_amount, max_amount, opened_count)


class GameResult:
    def __init__(self, selected_amount, max_amount, opened_count):
        self.selected_amount = selected_amount
        self.max_amount = max_amount
        self.opened_count = opened_count
        self.success = (selected_amount == max_amount)
        if max_amount > 0:
            self.ratio = selected_amount / max_amount
        else:
            self.ratio = 0


    def __str__(self):
        return (f"GameResult(selected={self.selected_amount}, "
                f"max={self.max_amount}, "
                f"opened={self.opened_count}, "
                f"success={self.success}, "
                f"ratio={self.ratio:.2f})")
