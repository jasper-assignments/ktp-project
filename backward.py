from logic import Disjunction, Conjunction, Fact, Rule, Question
from domain import Domain

def evaluate_antecedent(
    rules: list[Rule], domain: Domain, questions: dict[str, Question], 
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
    
def ask_user(question: Question) -> str:
  options = [f"{i}: {a.label}" for i, a in enumerate(question.answers)]
  return question.answers[int(input(f"{question.description} ({", ".join(options)}) > "))].value
    
def backward(rules: list[Rule], domain: Domain, questions: dict[str, Question], goal: Fact) -> bool:
  if getattr(domain, goal.name) is not None:
    return getattr(domain, goal.name) == goal.value
  
  for rule in rules:
    if rule.consequent == goal and evaluate_antecedent(rules, domain, questions, rule.antecedent):
      setattr(domain, goal.name, goal.value)
      return True
      
  if (question := questions.get(goal.name)) is None:
    return False
  answer = ask_user(question)
  setattr(domain, goal.name, answer)
  return getattr(domain, goal.name) == goal.value
