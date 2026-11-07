import re
import csv
import json
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
try:
    from sentence_transformers import SentenceTransformer
    have_model = True
except ImportError:
    have_model = False
docs = {
    "returns": "Returns Guide. Thank you for shopping with us. This guide explains how a customer can send an item back after it has been delivered to the address on the order. Unused items can be returned within 14 days of delivery. The item must be in its original packaging with all tags attached, and the customer must start the return request from the Orders page before the parcel is handed to the courier. Return pickup is arranged by the courier within 2 working days after the request is approved. Opened hygiene products cannot be returned unless they arrive damaged. Sale items follow the same 14 day window, but a sale item that was marked as final sale at the time of purchase cannot be returned at all, even when it is unused and still in the original packaging, because the discount was given on the condition that the purchase is permanent and cannot be reversed later. Gift items can be returned by the person who received the gift if the gift receipt is shown. Customers who live outside the main cities may need up to 3 extra days for pickup. Please keep the return slip until the refund has been confirmed, since the support team may ask for the slip number.",
    "refunds": "Refund Guide. This guide describes how and when money is returned after a return has been accepted. Approved refunds are sent to the original payment method within 7 working days. The refund starts only after the warehouse has checked the returned item and marked it as accepted, so the days are counted from that check and not from the day the customer requested the return. Orders paid by cash on delivery cannot be refunded to a card, so the amount is returned by bank transfer after the customer submits the account details form. In the older 2022 guide, refunds were sent within 15 working days, but that period no longer applies to orders placed after January 2024. Refund of the delivery charge is made only when the item was faulty or the wrong item was sent. If a refund has not arrived after 7 working days, the customer should first check with the bank, because some banks need up to 5 extra days to show the credit in the statement. Store credit can be chosen instead of money, and store credit is added to the account at once. Dr. Rana from the finance team approves refunds above Rs. 50000 manually, and these may take longer.",
    "delivery": "Delivery Guide. Most orders are packed within one day and leave the warehouse the same evening. Standard delivery takes 3 to 5 working days. Express delivery is available in the main cities and takes 1 to 2 working days for an extra charge of Rs. 250. Orders above Rs. 3000 qualify for free standard delivery. The free delivery offer does not apply to express delivery or to bulky items such as furniture, which are charged by weight and by the distance between the warehouse and the delivery address, and the exact charge is shown on the checkout page before the customer confirms the payment. Remote areas may need 2 extra working days. The courier will call the phone number on the order before arriving, and if nobody answers, the courier will try again on the next working day for a maximum of 3 attempts. After the third failed attempt the parcel is returned to the warehouse. Customers can track the parcel using the tracking number sent by SMS. Parcels are not delivered on public holidays or on Sundays, and orders placed after 6 pm are counted from the next working day.",
    "warranty": "Warranty Guide. This guide covers repair and replacement for products that stop working normally. Electronics carry a warranty of 12 months from the purchase date. The warranty card or the order invoice must be shown when a claim is made at any service centre. The warranty does not cover damage caused by water or by repairs made outside our service centres. A product that cannot be repaired in 15 working days is replaced with the same model, or with a similar model when the original is out of stock, and the customer does not pay anything for the replacement if the claim is accepted as valid. In the older guide, the warranty period for electronics was 6 months, but this older period is only used for products bought before March 2023. Accessories such as chargers and cables carry a warranty of 3 months only. Batteries are covered for manufacturing faults but not for normal ageing. Claims can be made at the nearest service centre or through the support page. Pick up for repair is free for orders above Rs. 3000.",
    "account": "Account Help. This guide helps customers who cannot sign in to their account on the website or the mobile application. A forgotten password can be reset using the recovery link on the sign-in page. The link is sent to the email address saved in the account and it stays active for 30 minutes only. After five wrong password attempts the account is locked for one hour and it unlocks again by itself, so the customer does not need to contact support during that time. If the email address is no longer available, support can change it only after the customer proves who they are by answering the security questions and by sending the order number of a recent purchase. Support staff never ask for the full password or for the card security code, and customers should never share these details with anybody, even when the message claims to come from the company. Two step verification codes expire after 5 minutes and cannot be skipped by the help desk. Customers can also delete the account from the settings page, which removes the saved addresses but keeps the order records for tax purposes."
}
queries = [
    {"query": "How many days do I have to return an item?", "doc": "returns", "evidence": "Unused items can be returned within 14 days of delivery.", "split": "dev"},
    {"query": "When will my refund reach my bank account?", "doc": "refunds", "evidence": "Approved refunds are sent to the original payment method within 7 working days.", "split": "dev"},
    {"query": "Is delivery free for big orders?", "doc": "delivery", "evidence": "Orders above Rs. 3000 qualify for free standard delivery.", "split": "dev"},
    {"query": "How long does the warranty on electronics last?", "doc": "warranty", "evidence": "Electronics carry a warranty of 12 months from the purchase date.", "split": "dev"},
    {"query": "What should I do if I forgot my login password?", "doc": "account", "evidence": "A forgotten password can be reset using the recovery link on the sign-in page.", "split": "test"},
    {"query": "Can I send back a product I have already opened?", "doc": "returns", "evidence": "Opened hygiene products cannot be returned unless they arrive damaged.", "split": "test"},
    {"query": "How soon will my parcel arrive?", "doc": "delivery", "evidence": "Standard delivery takes 3 to 5 working days.", "split": "test"},
    {"query": "Does the warranty cover water damage?", "doc": "warranty", "evidence": "The warranty does not cover damage caused by water or by repairs made outside our service centres.", "split": "test"},
    {"query": "Which team won the cricket match yesterday?", "doc": None, "evidence": None, "split": "test"},
    {"query": "What is the weather in Murree tomorrow?", "doc": None, "evidence": None, "split": "test"}
]
for name in docs:
    assert 150 <= len(docs[name].split()) <= 250
    print(name, "words:", len(docs[name].split()))
for q in queries:
    if q["doc"]:
        assert q["evidence"] in docs[q["doc"]]
with open("corpus.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, indent=2)
with open("queries.json", "w", encoding="utf-8") as f:
    json.dump(queries, f, indent=2)
print()
print("=" * 60)
print("TASK 1: Tokens and FAQ chatbot")
print("=" * 60)
inputs = ["Hello, world!", "She doesn't know.", "support@shop.pk", "Order #A1042 shipped", "refund_id: RF-2024", "", "آرڈر کب آئے گا"]
for text in inputs:
    ws = text.split()
    wl = re.findall(r"\w+", text)
    print("Original  :", repr(text))
    print("Whitespace:", ws, len(ws))
    print("Word-like :", wl, len(wl))
    print()
if have_model:
    t = time.perf_counter()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    model_load = time.perf_counter() - t
    print("Model load seconds:", round(model_load, 3))
    for text in ["She doesn't know.", "Order #A1042 shipped"]:
        pieces = model.tokenizer.tokenize(text)
        print("Model sub-words:", repr(text), pieces, len(pieces))
else:
    print("Model tokenizer: not run (sentence-transformers is not installed here)")
print()
faqs = [
    {"question": "How long does standard delivery take?", "answer": "Standard delivery takes 3 to 5 working days.", "source": "delivery.txt"},
    {"question": "Can I return an opened item?", "answer": "Opened hygiene products cannot be returned unless they arrive damaged.", "source": "returns.txt"},
    {"question": "How long is the warranty on electronics?", "answer": "Electronics carry a warranty of 12 months from the purchase date.", "source": "warranty.txt"},
    {"question": "How do I reset my password?", "answer": "Use the recovery link on the sign-in page.", "source": "account.txt"},
    {"question": "How long does a refund take?", "answer": "Approved refunds are sent within 7 working days.", "source": "refunds.txt"}
]
faq_vec = TfidfVectorizer()
faq_matrix = faq_vec.fit_transform([f["question"] + " " + f["answer"] for f in faqs])
def faq_reply(query):
    if not query.strip():
        return "Please type a question."
    for f in faqs:
        if query.strip().casefold() == f["question"].casefold():
            return f["answer"] + " [source: " + f["source"] + "]"
    q = faq_vec.transform([query])
    if q.nnz == 0:
        return "No matching FAQ. Please contact the help desk."
    scores = (q @ faq_matrix.T).toarray()[0]
    order = np.argsort(-scores, kind="stable")[:3]
    lines = ["Possible matches, please pick one and ask it exactly:"]
    for i in order:
        lines.append("  " + faqs[i]["question"] + " (similarity " + format(scores[i], ".3f") + ")")
    return "\n".join(lines)
print("--- FAQ chatbot transcript ---")
for typed in ["How long is the warranty on electronics?", "refund money", "", "volcano geology"]:
    print("You:", typed)
    print("Bot:", faq_reply(typed))
    print()
print("Why confirmation: a similarity score is not proof that the FAQ answers the question, so only an exact FAQ question gets its answer shown directly.")
print()
print("=" * 60)
print("TASK 2: Chunking and semantic suggestions")
print("=" * 60)
def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
def window_chunks(text, size=40, overlap=0):
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("bad size or overlap")
    spans = word_spans(text)
    out = []
    i = 0
    while i < len(spans):
        j = min(i + size, len(spans))
        out.append((spans[i][0], spans[j - 1][1]))
        if j == len(spans):
            break
        i = i + size - overlap
    return out
def sentence_pieces(text):
    pieces = []
    pos = 0
    for m in re.finditer(r"[.!?]\s+", text):
        pieces.append((pos, m.end()))
        pos = m.end()
    if pos < len(text):
        pieces.append((pos, len(text)))
    return pieces
def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("size must be positive")
    out = []
    cur_start = None
    cur_end = None
    cur_words = 0
    for a, b in sentence_pieces(text):
        n = len(text[a:b].split())
        if n == 0:
            continue
        if n > size:
            if cur_start is not None:
                out.append((cur_start, cur_end))
                cur_start = None
                cur_words = 0
            for x, y in window_chunks(text[a:b], size, 0):
                out.append((a + x, a + y))
        elif cur_start is not None and cur_words + n <= size:
            cur_end = b
            cur_words = cur_words + n
        else:
            if cur_start is not None:
                out.append((cur_start, cur_end))
            cur_start = a
            cur_end = b
            cur_words = n
    if cur_start is not None:
        out.append((cur_start, cur_end))
    fixed = []
    for a, b in out:
        while b > a and text[b - 1].isspace():
            b = b - 1
        fixed.append((a, b))
    return fixed
def make_chunks(corpus, strategy):
    result = []
    for name, text in corpus.items():
        if strategy == "sentence":
            spans = sentence_chunks(text, 40)
        else:
            spans = window_chunks(text, 40, int(strategy.split("-")[1]))
        for i, (a, b) in enumerate(spans):
            result.append({"id": name + ":" + str(i), "doc": name, "start": a, "end": b, "text": text[a:b]})
    return result
assert window_chunks("") == []
assert window_chunks("short text") == [(0, 10)]
try:
    window_chunks("a b c", 2, 2)
    raise SystemExit("invalid overlap was accepted")
except ValueError:
    pass
long_sentence = " ".join(["word"] * 95) + "."
parts = sentence_chunks(long_sentence, 40)
assert len(parts) == 3 and all(len(long_sentence[a:b].split()) <= 40 for a, b in parts)
for strategy in ["window-0", "window-10", "sentence"]:
    for c in make_chunks(docs, strategy):
        assert c["text"] == docs[c["doc"]][c["start"]:c["end"]] and c["text"].strip()
print("Boundary tests passed: empty, short, invalid overlap, long sentence (3 parts), offsets match source")
print()
total_words = sum(len(t.split()) for t in docs.values())
evidence_list = [q["evidence"] for q in queries if q["doc"]]
print("strategy    chunks  avg_w  min  max  repeated_w  evidence_in_1_chunk")
for strategy in ["window-0", "window-10", "sentence"]:
    chunks = make_chunks(docs, strategy)
    sizes = [len(c["text"].split()) for c in chunks]
    kept = 0
    for q in queries:
        if q["doc"] and any(c["doc"] == q["doc"] and q["evidence"] in c["text"] for c in chunks):
            kept += 1
    print(f"{strategy:<11} {len(chunks):>6}  {np.mean(sizes):>5.1f}  {min(sizes):>3}  {max(sizes):>3}  {sum(sizes) - total_words:>10}  {kept}/{len(evidence_list)}")
print()
print("Sentence splitter failure (abbreviation), delivery document:")
text = docs["delivery"]
at = text.index("Orders above")
for a, b in sentence_pieces(text):
    if a >= at - 10 and b <= at + 120:
        print("  ", repr(text[a:b]))
print()
class Engine:
    def __init__(self, method, chunks):
        self.method = method
        self.chunks = chunks
        texts = [c["text"] for c in chunks]
        t = time.perf_counter()
        if method == "tfidf":
            self.vec = TfidfVectorizer()
            self.matrix = self.vec.fit_transform(texts)
        else:
            self.matrix = model.encode(texts, normalize_embeddings=True)
        self.encode_time = time.perf_counter() - t
        self.search_time = 0
        self.searches = 0
    def scores(self, query):
        t = time.perf_counter()
        if self.method == "tfidf":
            row = (self.vec.transform([query]) @ self.matrix.T).toarray()[0]
        else:
            row = self.matrix @ model.encode([query], normalize_embeddings=True)[0]
        self.search_time += time.perf_counter() - t
        self.searches += 1
        return row
    def top(self, query, k=3):
        row = self.scores(query)
        return [(self.chunks[i], float(row[i])) for i in np.argsort(-row, kind="stable")[:k]]
methods = ["tfidf"]
if have_model:
    methods.append("embedding")
else:
    print("Embedding runs skipped: sentence-transformers is not installed in this environment")
paraphrases = ["How can I get back into my profile?", "I received a faulty item, will I get my money back?", "Do you deliver on Sundays?"]
sent_chunks = make_chunks(docs, "sentence")
for method in methods:
    eng = Engine(method, sent_chunks)
    for q in paraphrases:
        print("[" + method + "]", q)
        for c, s in eng.top(q):
            print("   ", c["id"], "score=" + format(s, ".3f"), "chars", str(c["start"]) + "-" + str(c["end"]) + ":", c["text"][:70] + "...")
print()
print("=" * 60)
print("TASK 3: Retrieval evaluation")
print("=" * 60)
def judge(row, chunks, q):
    top = np.argsort(-row, kind="stable")[:3]
    for rank, i in enumerate(top, 1):
        if chunks[i]["doc"] == q["doc"] and q["evidence"] in chunks[i]["text"]:
            return rank
    return 0
results = {}
logs = []
engines = {}
for strategy in ["window-0", "window-10", "sentence"]:
    chunks = make_chunks(docs, strategy)
    if have_model:
        longest = max(len(model.tokenizer(c["text"], truncation=False)["input_ids"]) for c in chunks)
        print("[" + strategy + "] token audit: longest chunk =", longest, "limit =", model.max_seq_length)
        assert longest <= model.max_seq_length
    for method in methods:
        eng = Engine(method, chunks)
        engines[(strategy, method)] = eng
        ranks = {"dev": [], "test": []}
        for q in queries:
            row = eng.scores(q["query"])
            if q["doc"]:
                ranks[q["split"]].append(judge(row, chunks, q))
            for r, i in enumerate(np.argsort(-row, kind="stable")[:3], 1):
                c = chunks[i]
                logs.append({"strategy": strategy, "method": method, "query": q["query"], "split": q["split"], "answerable": q["doc"] is not None, "rank": r, "score": round(float(row[i]), 4), "chunk_id": c["id"], "start": c["start"], "end": c["end"], "text": c["text"]})
        for split in ["dev", "test"]:
            rk = ranks[split]
            hit = sum(1 for r in rk if r > 0) / len(rk)
            mrr = sum(1 / r for r in rk if r > 0) / len(rk)
            results[(strategy, method, split)] = (hit, mrr)
            print(f"{strategy:<10} {method:<9} {split:<4} Hit@3={hit:.3f} MRR@3={mrr:.3f} chunks={len(chunks)} encode={eng.encode_time:.4f}s search={eng.search_time / eng.searches:.5f}s per query")
with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(logs[0]))
    w.writeheader()
    w.writerows(logs)
print("retrieval_log.csv saved with", len(logs), "rows")
print()
pick_method = methods[-1]
pick = max(["window-0", "window-10", "sentence"], key=lambda s: (results[(s, pick_method, "dev")][1], -len(engines[(s, pick_method)].chunks)))
print("Selected on development MRR (" + pick_method + "):", pick)
print("Held-out test result of selected strategy:", results[(pick, pick_method, "test")])
print()
print("Failures and edge cases (" + pick + ", " + pick_method + "):")
eng = engines[(pick, pick_method)]
for q in queries:
    row = eng.scores(q["query"])
    rank = judge(row, eng.chunks, q) if q["doc"] else 0
    best = eng.chunks[int(np.argmax(row))]
    if q["doc"] is None:
        print("  unanswerable:", repr(q["query"]), "->", best["id"], "score", round(float(row.max()), 3), "chars", best["start"], best["end"])
    elif rank != 1:
        print("  rank", rank, repr(q["query"]), "-> top", best["id"], "score", round(float(row.max()), 3), "chars", best["start"], best["end"])
print()
print("--- Document chatbot session (scripted inputs) ---")
session = [("How soon will my parcel arrive?", "1"), ("Can I send back a product I have already opened?", "1"), ("", ""), ("Which team won the cricket match yesterday?", ""), ("Does the warranty cover water damage?", "1")]
for typed, choice in session:
    print("Question:", typed)
    if not typed.strip():
        print("Please type a question.")
        print()
        continue
    row = eng.scores(typed)
    if row.max() <= 0:
        print("No candidate evidence. Rephrase or contact a human.")
        print()
        continue
    hits = eng.top(typed)
    print("Candidate evidence (not verified):")
    for n, (c, s) in enumerate(hits, 1):
        print("  ", n, c["id"], format(s, ".3f"), "chars", c["start"], c["end"])
    print("Choice:", repr(choice))
    if not choice.isdigit() or not 1 <= int(choice) <= len(hits):
        print("No answer selected. Rephrase or contact a human.")
    else:
        c, s = hits[int(choice) - 1]
        print("Passage:", c["text"])
        print("Source:", c["doc"], "chars", c["start"], c["end"])
    print()
