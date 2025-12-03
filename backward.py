from logic import Disjunction, Conjunction, Fact, Rule
from domain import Domain

def evaluate_antecedent(
    rules: list[Rule], domain: Domain, questions: dict[str, str], 
    antecedent: Disjunction | Conjunction | Fact) -> bool:
  match antecedent:
    case Fact():
      return backward(rules, domain, questions, antecedent)
    case Conjunction():
      return all(
        evaluate_antecedent(rules, domain, questions, conjunct)
        for conjunct in antecedent.conjuncts
      )
    case Disjunction():
      return any(
        evaluate_antecedent(rules, domain, questions, disjunct)
        for disjunct in antecedent.disjuncts
      )
    case _:
      msg = f"Unknown antecedent type: {type(antecedent)}"
      raise TypeError(msg)
    
def backward(rules: list[Rule], domain: Domain, questions: dict[str, str], goal: Fact) -> bool:
  if getattr(domain, goal.name) is not None:
    return getattr(domain, goal.name) == goal.value
  
  for rule in rules:
    if rule.consequent == goal and evaluate_antecedent(rules, domain, questions, rule.antecedent):
      setattr(domain, goal.name, goal.value)
      return True
      
  if (question := questions.get(goal.name)) is None:
    return False
  
  setattr(domain, goal.name, ask_user(question))
  return getattr(domain, goal.name) == goal.value