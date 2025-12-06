from logic import Disjunction, Conjunction, Fact, Rule, Question
from domain import Domain

def evaluate_antecedent(
    rules: list[Rule], domain: Domain, questions: dict[str, Question], 
    antecedent: Disjunction | Conjunction | Fact):
  match antecedent:
    case Fact():
      return (yield from backward(rules, domain, questions, antecedent))
    case Conjunction():
      for conjunct in antecedent.conjuncts:
        if not (yield from evaluate_antecedent(rules, domain, questions, conjunct)):
          return False
      return True
    case Disjunction():
      for disjunct in antecedent.disjuncts:
        if (yield from evaluate_antecedent(rules, domain, questions, disjunct)):
          return True
      return False
    case _:
      msg = f"Unknown antecedent type: {type(antecedent)}"
      raise TypeError(msg)
    
def backward(rules: list[Rule], domain: Domain, questions: dict[str, Question], goal: Fact) -> bool:
  if getattr(domain, goal.name) is not None:
    return getattr(domain, goal.name) == goal.value
  
  for rule in rules:
    if rule.consequent == goal and (yield from evaluate_antecedent(rules, domain, questions, rule.antecedent)):
      setattr(domain, goal.name, goal.value)
      return True
      
  if (question := questions.get(goal.name)) is None:
    return False
  answer = yield question
  setattr(domain, goal.name, answer)
  return getattr(domain, goal.name) == goal.value
