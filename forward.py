from logic import Question, Fact, Rule, Conjunction, Disjunction
from domain import Domain

def evaluate_antecedent(domain: Domain, antecedent: Fact | Conjunction | Disjunction) -> bool:
    match antecedent:
        case Fact():
            return getattr(domain, antecedent.name) == antecedent.value
        case Conjunction():
            return all(
                evaluate_antecedent(domain, conjunct)
                for conjunct in antecedent.conjuncts
            )
        case Disjunction():
            return any(
                evaluate_antecedent(domain, disjunct)
                for disjunct in antecedent.disjuncts
            )
        case _:
            msg = f"Unknown antecedent type: {type(antecedent)}"
            raise TypeError(msg)

def choose_question(domain: Domain, questions: dict[str, Question]) -> str | None:
    knowns = (f.name for f in fields(domain) if getattr(domain, f.name) is not None)
    askable = list(questions.keys() - knowns)
    return questions[askable[0]] if askable else None

def ask_user(q: Question) -> str:
    print(q.description)
    for a in q.answers:
        print(f" - {a.value}: {a.label}")
    return input("? ").strip()

def fire_rules(rules: list[Rule], domain: Domain) -> bool:
    fired = False
    for rule in rules:
        if getattr(domain, rule.consequent.name) is None and evaluate_antecedent(domain, rule.antecedent):
            setattr(domain, rule.consequent.name, rule.consequent.value)
            fired = True
    return fired

def forward(rules: list[Rule], domain: Domain, questions: dict[str, Question], goal: Fact) -> str:
    while getattr(domain, goal.name) is None:
        if fire_rules(rules, domain):
            continue

        question = choose_question(domain, questions)
        if question is None: # No question can be asked
            break

        answer = ask_user(question)
        setattr(domain, question, answer)
    
    return getattr(domain, goal)
