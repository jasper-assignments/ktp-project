from dataclasses import dataclass

@dataclass
class Fact:
  name: str
  value: str

@dataclass
class Conjunction:
  conjuncts: list[Fact]

@dataclass
class Disjunction:
  disjuncts: list[Fact | Conjunction]

@dataclass
class Negation:
  fact: Fact | Conjunction | Disjunction

@dataclass
class Rule:
  antecedent: Disjunction | Conjunction | Fact
  consequents: list[Fact]

@dataclass
class Answer:
  value: str
  label: str

@dataclass
class Question:
  name: str
  description: str
  answers: list[Answer]
