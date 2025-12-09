from logic import Disjunction, Conjunction, Fact, Rule, Question, Negation

def evaluate_antecedent(
    rules: list[Rule], domain: dict, questions: dict[str, Question], 
    antecedent: Negation | Disjunction | Conjunction | Fact):
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
    case Negation():
      return not (yield from evaluate_antecedent(rules, domain, questions, antecedent.fact))
    case _:
      msg = f"Unknown antecedent type: {type(antecedent)}"
      raise TypeError(msg)
    
def backward(rules: list[Rule], domain: dict, questions: dict[str, Question], goal: Fact) -> bool:
  if domain.get(goal.name, None) is not None:
    return domain.get(goal.name) == goal.value
  
  for rule in rules:
    if rule.consequent == goal and (yield from evaluate_antecedent(rules, domain, questions, rule.antecedent)):
      domain[goal.name] = goal.value
      return True
      
  if (question := questions.get(goal.name)) is None:
    return False
  answer = yield question
  domain[goal.name] = answer
  return domain.get(goal.name, None) == goal.value
