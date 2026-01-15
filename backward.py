from logic import Disjunction, Conjunction, Fact, Rule, Question, Negation, Subclass
from domain import Domain

def evaluate_antecedent(
    subclasses: list[Subclass], domain: dict, questions: dict[str, Question], 
    antecedent: Negation | Disjunction | Conjunction | Fact):
  match antecedent:
    case Fact():
      return (yield from backward(subclasses, domain, questions, antecedent))
    case Conjunction():
      for conjunct in antecedent.conjuncts:
        if not (yield from evaluate_antecedent(subclasses, domain, questions, conjunct)):
          return False
      return True
    case Disjunction():
      for disjunct in antecedent.disjuncts:
        if (yield from evaluate_antecedent(subclasses, domain, questions, disjunct)):
          return True
      return False
    case Negation():
      return not (yield from evaluate_antecedent(subclasses, domain, questions, antecedent.fact))
    case _:
      msg = f"Unknown antecedent type: {type(antecedent)}"
      raise TypeError(msg)

def backward(rules: list[Rule], domain: Domain, subclasses: dict[str, Subclass], goal: Fact):
  if (fact := domain.getFact(goal.name)) is not None:
    return fact == goal.value
  
  for rule in rules:
    if goal in rule.consequents and (yield from evaluate_antecedent(rules, domain, subclasses, rule.antecedent)):
      for consequent in rule.consequents:
        domain.setFact(consequent.name, consequent.value)
      return True
  
  question = None
  
  for subclassName in domain.subclassOrder:
    subclass = subclasses[subclassName]
    questions = subclass.questions
    if (question := questions.get(goal.name)) is not None:
      # If we switched subclass, that is we started a new subclass before and the current subclass is different,
      # we complete the old subclass and give the user a complete message first.
      currentSubclass = domain.getCurrentSubclass()
      if currentSubclass is not None and currentSubclass != subclassName:
        # Only give the complete message if it is the first time.
        if domain.completeSubclass(currentSubclass):
          yield {"message": {"description": subclasses[currentSubclass].completeMessage}}

      # If first time we ask a question from this subclass then we give the user a start message first.
      if domain.startSubclass(subclassName):
        yield {"message": {"description": subclasses[subclassName].startMessage}}

      # Question is not none, break and ask user question.
      break
  
  if question is None:
    # No more questions to ask so our goal is not achieved
    return False

  answer = yield {"question": question}
  domain.setFact(goal.name, answer)

  return domain.getFact(goal.name) == goal.value
