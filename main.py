from decimal import Decimal


class Interval:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class LetterInterval(Interval):
    def __init__(self, letter, left, right):
        super().__init__(left, right)
        self.letter = letter


def calculate_frequencies(message):
    total_length = len(message)
    frequencies = {}
    for char in message:
        frequencies[char] = frequencies.get(char, 0) + 1
    for char in frequencies:
        frequencies[char] = Decimal(frequencies[char]) / Decimal(total_length)
    return dict(sorted(frequencies.items(), key=lambda item: item[1]))


def build_intervals(frequencies):
    letter_intervals = {}
    current_left = Decimal('0')
    for letter, prob in frequencies.items():
        current_right = current_left + prob
        letter_intervals[letter] = LetterInterval(letter, current_left, current_right)
        current_left = current_right
    return letter_intervals


def update_intervals(main_interval, frequencies):
    new_intervals = {}
    current_left = main_interval.left
    range_width = main_interval.right - main_interval.left
    for letter, prob in frequencies.items():
        current_right = current_left + range_width * prob
        new_intervals[letter] = LetterInterval(letter, current_left, current_right)
        current_left = current_right
    return new_intervals


def arithmetic_encode(message):
    frequencies = calculate_frequencies(message)
    print("Frequencies:", frequencies)

    letter_intervals = build_intervals(frequencies)
    print("\nInitial Intervals:")
    for interval in letter_intervals.values():
        print(interval.letter, interval.left, interval.right)

    main_interval = Interval(Decimal('0'), Decimal('1'))

    for char in message:
        main_interval = Interval(
            letter_intervals[char].left,
            letter_intervals[char].right
        )
        letter_intervals = update_intervals(main_interval, frequencies)
        print("\nUpdated Intervals:")
        for interval in letter_intervals.values():
            print(interval.letter, interval.left, interval.right)

    print("\nFinal Interval: [{}, {})".format(main_interval.left, main_interval.right))
    return main_interval


# Input and encoding
message = input("Enter the message to encode: ")
arithmetic_encode(message)
