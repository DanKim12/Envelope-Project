import random

class Strategy:
    def __init__(self, envelopes):
        self.envelopes = envelopes
        self.selected_envelope = None

    def play(self):
        pass

    def display(self):
        return self.__class__.__name__

"""
This class is the first strategy:
the player picks envelope and decide whether to stop or not
"""
class BaseStrategy(Strategy):
    def play(self):
        stop = False #boolean variable to control if the user wants to stop or not
        while not stop: # run until player decides to stop
            index = random.randint(0, len(self.envelopes) - 1) #random envelope
            want_to_stop = input("Stop? YES/NO").upper()
            if want_to_stop == 'YES':
                stop = True
                self.selected_envelope = self.envelopes[index]
                return

            else:
                opened = self.envelopes.pop(index)
                amount = opened.get_amount()
                print(f"Opened envelope with ${amount}")

    def display(self):
        print(f"Stopped manually ${self.selected_envelope.get_amount()}")


"""
This class is the second strategy: 
the player choose random envelope and keeps it
"""
class Automatic_BaseStrategy(Strategy):
    def play(self):
        self.selected_envelope = random.choice(self.envelopes)

    def display(self):
        print(f"Randomly selected envelope with ${self.selected_envelope.get_amount()}")


"""
This class is the third strategy: 
the player chooses a maximum number of envelopes (N). 
They open envelopes one by one until N have been opened, 
and the last opened envelope is the one they keep.
"""
class N_max_strategy(Strategy):
    def __init__(self, envelopes, N=3):
        super().__init__(envelopes)
        self.N = N

    def play(self):
        for i in range(min(self.N, len(self.envelopes))):
            index = random.randint(0, len(self.envelopes) - 1)
            opened = self.envelopes.pop(index)
            amount = opened.get_amount()
            print(f"Opened envelope with ${amount}")

        if self.envelopes:
            self.selected_envelope = random.choice(self.envelopes)
            print(f"Selected envelope with ${self.selected_envelope.get_amount()}")

        else:
            self.selected_envelope = None
            print("No envelopes left to select.")

    def display(self):
        return f"N_max_strategy (stop after opening {self.N} envelopes)"


"""
This class is the fourth strategy: 
the player selects a percentage of envelopes to open initially. 
From these, the maximum amount is saved as a constant, and the game continues 
until an envelope with a higher amount is found, which the player then keeps.
"""


class More_then_N_percent_group_strategy(Strategy):
    def __init__(self, envelopes, percent=0.25):  # gets the wanted percentage and the envelopes
        super().__init__(envelopes)
        self.percent = percent

    def play(self):
        num_to_open = int(
            len(self.envelopes) * self.percent)  # calculation needed to find how many envelopes we must open first, according to the percentage
        max_amount = -1  # the first "max", preventing from errors in calculation
        max_envelope = None  # none of the envelopes has been checked yet

        for i in range(min(num_to_open,
                           len(self.envelopes))):  # according to the calculation, running N percent of the envelopes
            opened = self.envelopes.pop(
                random.randint(0, len(self.envelopes) - 1))  # poping of the chosen envelope(can not be chosen again)
            amount = opened.get_amount()  # gets the envelope's value
            print(f"Opened envelope with ${amount}")
            if amount > max_amount:  # if the new value is bigger than all the previous ones
                max_amount = amount  # its become the new max
                max_envelope = opened  # apdating the max envelope

        found_better = False  # setting the new variable
        for opened in self.envelopes:  # running for the rest of the envelopes
            amount = opened.get_amount()  # checking on the rest of the envelopes
            print(f"Checking envelope with ${amount}")
            if opened.get_amount() > max_amount:  # if an envelope with more money is opened
                self.selected_envelope = opened  # its immediately becoming the final envelope
                found_better = True
                print(f"Found better envelope with ${self.selected_envelope.get_amount()}")
                break  # no need to keep searching, that is the point of this strategy

        if not found_better:  # if the true max value has been in the original checked percent
            self.selected_envelope = max_envelope  # unforchenetly the last envelope, with big or small amount is the final envelope
            print(f"No better envelope found. Selected envelope with ${self.selected_envelope.get_amount()}")

    def display(self):
        if self.selected_envelope:
            print(f"BetterThanPercentStrategy: Selected envelope with ${self.selected_envelope.get_amount()}")
        else:
            print("BetterThanPercentStrategy: No envelope selected yet.")


"""
בעייה דומה נקראת בעית המזכירה.
 מתמטיקאים הוכיחו שהאחוז המוצלח ביותר כדי לבחור "משהו" מתוך מספר מוגדר של עצמים, הוא 37%.
הפיתרון לבעיה, הנקראת גם כלל 37, הוא לבדוק את 37% הראשונים.
לאחר מכן, יש לבדוק מי מבין ה37% היה המוצלח ביותר
(המזכירה הטובה ביותר, העובד בעל הקורות החיים המרשימים ביותר, הבת זוג החמודה ביותר, וכן הלאה)
ולבחור במועמד הראשון שמוצלח יותר מהמועמד הנוכחי המוצלח ביותר. המקסימלי.
לפי שיטה זאת, יש לאדם סיכוי של 1 לe בערך, כלומר 1 ל2.71828, או באחוזים, מעל 35% הצלחה.
כשמדובר ב1 מתוך 100, מעל 35% הצלחה הם מרשימים מאוד, במיוחד כשאחוזים נוספים מצביעים על אפשרויות טובות נוספות
(המעטפה השנייה בגודלה, המעטפה השלישית בגודלה וכן הלאה) 
"""