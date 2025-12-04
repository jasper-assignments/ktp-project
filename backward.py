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
  return question.answers[int(input(f"{question.description} ({", ".join(options)}) > "))]

"""def ask_user(q: Question) -> str:
    print(q.description)
    for a in q.answers:
        print(f" - {a.value}: {a.label}")
    return input("? ").strip()"""
    
def backward(rules: list[Rule], domain: Domain, questions: dict[str, Question], goal: Fact) -> bool:
  if getattr(domain, goal.name) is not None:
    print(f"Found in domain: {goal.name}={getattr(domain, goal.name)}")
    return getattr(domain, goal.name) == goal.value
  
  for rule in rules:
    print(f"Applying rule: {rule}")
    if rule.consequent == goal:
      print(f"Rule consequent matches goal: {goal.name}={goal.value}")
      if evaluate_antecedent(rules, domain, questions, rule.antecedent):
        print(f"Antecedent evaluated to True for goal: {goal.name}={goal.value}")
        setattr(domain, goal.name, goal.value)
        return True
    if rule.consequent == goal and evaluate_antecedent(rules, domain, questions, rule.antecedent):
      print(f"Rule is the goal and goal is achieved")
      setattr(domain, goal.name, goal.value)
      return True
      
  if (question := questions.get(goal.name)) is None:
    print(f"No question found for: {goal.name}")
    return False
  print("domain is", domain)
  answer = ask_user(question)
  print(f"User answered: {answer} for question {question.name}")
  setattr(domain, goal.name, answer)
  return getattr(domain, goal.name) == goal.value
