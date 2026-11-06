# Lab 1 Task 2: rule checker with 2 extra conditions
def check(score, complete, attendance, clean_record):
    if complete == False:
        return "Hold", "documents incomplete"
    if score < 70:
        return "Hold", "score is below 70"
    if attendance < 75:
        return "Hold", "attendance is below 75"
    if clean_record == False:
        return "Hold", "has a disciplinary record"
    return "Review", "all conditions met"
def test(name, score, complete, attendance, clean_record, expected):
    actual, reason = check(score, complete, attendance, clean_record)
    print("Case:", name)
    print("Input:", score, complete, attendance, clean_record)
    print("Expected:", expected)
    print("Actual:", actual)
    print("Reason:", reason)
    print("-----")
test("pass", 85, True, 90, True, "Review")
test("fail attendance", 85, True, 60, True, "Hold")
test("fail conduct", 85, True, 90, False, "Hold")
test("boundary", 70, True, 75, True, "Review")