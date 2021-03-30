from collections import defaultdict
import re


class Situation:
    def __init__(self, s_tuple):
        self.left = s_tuple[0]
        self.dot_pos = s_tuple[1]
        self.right = s_tuple[2]
        self.i = s_tuple[3]


class Algo:
    def __init__(self, grammar):
        self.D = []
        self.grammar = grammar

    @staticmethod
    def scan(D, letter, pos):
        D.append(set())
        for situation in D[pos]:
            situation = Situation(situation)
            if situation.dot_pos < len(situation.right) and situation.right[situation.dot_pos] == letter:
                new_situation = (situation.left, situation.dot_pos + 1, situation.right, situation.i)
                D[pos + 1].add(new_situation)

    @staticmethod
    def predict(D, pos, grammar):
        for situation in frozenset(D[pos]):
            situation = Situation(situation)
            if situation.dot_pos < len(situation.right) and situation.right[situation.dot_pos].isupper():
                for rule in grammar[situation.right[situation.dot_pos]]:
                    D[pos].add((situation.right[situation.dot_pos], 0, rule, pos))

    @staticmethod
    def complete(D, pos):
        for situation in frozenset(D[pos]):
            situation = Situation(situation)
            if situation.dot_pos >= len(situation.right):
                for completed in frozenset(D[situation.i]):
                    completed = Situation(completed)
                    if completed.dot_pos < len(completed.right) and \
                            completed.right[completed.dot_pos] == situation.left:
                        D[pos].add((completed.left, completed.dot_pos + 1, completed.right, completed.i))


def earley(grammar, word):
    n = len(word)
    algo = Algo(grammar)
    algo.D.append({('X', 0, 'S', 0)})
    D_copy = frozenset()
    while frozenset(algo.D[0]) != D_copy:
        D_copy = frozenset(algo.D[0])
        algo.predict(algo.D, 0, algo.grammar)
        algo.complete(algo.D, 0)

    for i in range(len(word)):
        D_copy = ()
        algo.scan(algo.D, word[i], i)
        while tuple(algo.D[i + 1]) != D_copy:
            D_copy = tuple(algo.D[i + 1])
            algo.predict(algo.D, i + 1, algo.grammar)
            algo.complete(algo.D, i + 1)
    return ('X', 1, 'S', 0) in algo.D[n]


def main():
    grammar = defaultdict(list)
    rules_cnt = int(input())
    for i in range(rules_cnt):
        rule = input()
        divs = [x.start() for x in re.finditer('\|', rule)]
        prev = 3
        for div in divs:
            grammar[rule[0]].append(rule[prev:div])
            prev = div + 1
        grammar[rule[0]].append(rule[prev:])
    word = input()
    print(earley(grammar, word))


if __name__ == '__main__':
    main()
