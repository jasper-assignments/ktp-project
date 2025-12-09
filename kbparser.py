import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from logic import Conjunction, Disjunction, Fact, Rule, Answer, Question, Negation

def parse_antecedent(antecedent: Element) -> Disjunction | Conjunction | Fact:
  match antecedent.tag:
    case "fact":
      return Fact(
        name=antecedent.attrib["name"],
        value=antecedent.text
      )
    case "and":
      return Conjunction([parse_antecedent(conjunct) for conjunct in antecedent])
    case "or":
      return Disjunction([parse_antecedent(disjunct) for disjunct in antecedent])
    case "not":
      return Negation(parse_antecedent(antecedent[0]))
    case _:
      msg = f"Unknown antecedent type: {antecedent.tag}"
      raise ValueError(msg)
    
def parse_consequent(consequent: Element) -> Fact:
  if consequent.tag != "fact":
    msg = f"Consequent must be a fact, got: {consequent.tag}"
    raise ValueError(msg)
  return Fact(
    name=consequent.attrib["name"],
    value=consequent.text
  )

def parse_rule(rule: Element) -> Rule:
  antecedent = parse_antecedent(rule.find("if")[0])
  consequent = parse_consequent(rule.find("then").find("fact"))
  return Rule(antecedent=antecedent, consequent=consequent)

def parse_question(question: Element) -> Question:
  answers = list(map(
    lambda a: Answer(value=a.attrib["value"], label=a.text),
    question.find("answers").findall("answer")
  ))
  return Question(name=question.attrib["name"], description=question.find("description").text, answers=answers)

def parse_kb() -> tuple[list[Rule], dict[str, Question]]:
  tree = ET.parse("kb.xml")
  root = tree.getroot()
  # goal = Fact(name=root.find("goal").attrib["name"], value=root.find("goal").find("value").text)
  rules = [parse_rule(rule) for rule in root.find("rules")]
  
  questions = {
    q.name: q for q in (parse_question(question) for question in root.find("questions"))
  }
  
  return rules, questions
