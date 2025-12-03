from dataclasses import dataclass

@dataclass
class Fact:
  name: str
  value: str

@dataclass
class Conjunction:
  facts: list[Fact]

@dataclass
class Disjunction:
  conjunctions: list[Conjunction]

@dataclass
class Rule:
  antecedent: Disjunction | Conjunction | Fact
  consequent: Fact