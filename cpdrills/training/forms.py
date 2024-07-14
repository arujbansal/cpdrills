from django import forms

TAG_CHOICES = [('dp', 'Dynamic Programming'),
               ('graphs', 'Graph Theory'),
               ('strings', 'Strings'),
               ('brute force', 'Brute Force'),
               ('dsu', 'Union Find Disjoint Set'),
               ('binary search', 'Binary Search'),
               ('data structures', 'Data Structures'),
               ('constructive algorithms', 'Constructive Algorithms'),
               ('2-sat', '2-Satisfiability'),
               ('bitmasks', 'Bitmasks'),
               ('chinese remainder theorem', 'Chinese Remainder Theorem'),
               ('combinatorics', 'Combinatorics'),
               ('dfs and similar', 'DFS and Similar'),
               ('expression parsing', 'Expression Parsing'),
               ('fft', 'Fast Fourier Transform'),
               ('flows', 'Flows'),
               ('games', 'Game Theory'),
               ('greedy', 'Greedy'),
               ('hashing', 'Hashing'),
               ('implementation', 'Implementation'),
               ('interactive', 'Interactive'),
               ('math', 'Math'),
               ('matrices', 'Matrices'),
               ('meet-in-the-middle', 'Meet In The Middle'),
               ('number theory', 'Number Theory'),
               ('probabilities', 'Probability'),
               ('schedules', 'Schedules'),
               ('shortest paths', 'Shortest Paths'),
               ('sortings', 'Sorting'),
               ('string suffix structures', 'String Suffix Structures'),
               ('strings', 'Strings'),
               ('ternary search', 'Ternary Search'),
               ('trees', 'Trees'),
               ('two pointers', 'Two Pointers'),
               ]

RATING_CHOICES = ((800, 800), (900, 900))

CONTEST_CHOICES = (('Div. 1', 'Div. 1'), ('(Div. 2)', 'Div. 2'), ('Div. 3', 'Div. 3'), ('Edu', 'Div. 2 Edu'),
                   ('ICPC', 'ICPC Related'))

PROBLEM_CHOICES = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'),
                   ('I', 'I'))


class SpeedTrainProblemForm(forms.Form):
    rating = forms.ChoiceField(
        help_text="Choose a codeforces rating from the dropdown. Selecting topics and contest type is optional.",
        choices=[(x, x) for x in range(800, 3600, 100)], required=True)

    topics = forms.MultipleChoiceField(choices=TAG_CHOICES,
                                       widget=forms.CheckboxSelectMultiple, required=False,
                                       help_text="Optional. Recommends problems of random topics if none selected.")

    contest_type = forms.MultipleChoiceField(choices=CONTEST_CHOICES,
                                             widget=forms.CheckboxSelectMultiple, required=False,
                                             label='Contest Type')

    problem_type = forms.MultipleChoiceField(choices=PROBLEM_CHOICES,
                                             widget=forms.CheckboxSelectMultiple, required=False,
                                             label='Problem Type')
