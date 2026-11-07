def pick_mode(temp, occupied):
    if occupied is False:
        return "ECO"
    if temp > 26:
        return "COOL"
    if temp < 20:
        return "WARM"
    return "IDLE"
class Controller:
    def __init__(self):
        self.last = None
    def step(self, temp, occupied):
        new = pick_mode(temp, occupied)
        before = self.last
        send = new != before
        self.last = new
        return before, new, send
def run(name, readings):
    ctrl = Controller()
    sent = 0
    print(name)
    for n, (temp, occ) in enumerate(readings, 1):
        before, new, send = ctrl.step(temp, occ)
        if send:
            sent += 1
        room = "occupied" if occ else "empty"
        answer = "command sent" if send else "no command"
        print(f"Reading {n:>2}: {temp} C, {room:<8} | last={str(before):<5} | target={new:<5} | {answer}")
    print("Commands sent:", sent, "of", len(readings), "readings")
    print()
assert pick_mode(26, True) == "IDLE"
assert pick_mode(20, True) == "IDLE"
assert pick_mode(35, False) == "ECO"
main = [(31, True), (31, True), (26, True), (24, True), (20, True), (17, True), (17, True), (23, False), (23, False), (28, True)]
noisy = [(25, True), (27, True), (26, True), (27, True), (26, True), (27, True)]
print("REFLEX AGENT (no memory)")
modes = [pick_mode(t, o) for t, o in main]
print("Modes:", modes)
same = sum(1 for i in range(1, len(modes)) if modes[i] == modes[i - 1])
print("Readings that repeat the previous request:", same)
print()
run("STATEFUL AGENT: main test", main)
run("STATEFUL AGENT: noisy readings around 26 C", noisy)
