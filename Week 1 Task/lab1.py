# Lab 1: comparing rule method and probability method
def rule_based(score, complete):
    if complete == True and score >= 70:
     return "Review"
    else:
     return "Hold"
def probability_based(probability):
    if probability >= 0.70:
     return "Review"
    else:
     return "Hold"
def show(name, score, complete, probability):
    rule_result = rule_based(score, complete)
    prob_result = probability_based(probability)
    different = rule_result != prob_result
    print(name, "|", rule_result, "|", prob_result, "|", different)
print("case | rule | probability | different")
show("complete_high", 82, True, 0.81)
show("complete_low", 68, True, 0.74)
show("incomplete_high", 91, False, 0.88)
show("boundary", 70, True, 0.70)