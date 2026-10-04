# Teaching Style Guide

This style guide establishes the authoring standards, voice, conventions, and constraints for all educational content in `et-ccc`. Every module author and reviewer follows this guide.

---

## 1. Tone and Voice

- **Warm and plain**: Direct, respectful, and clear. Speak directly to the reader in the second person ("you", "your").
- **No cheerleading or hype**: Avoid exclamation marks, false enthusiasm ("This is super exciting!"), and patronizing encouragement ("Don't worry, it's easy!"). Let the clarity of the explanation build the learner's confidence.
- **No condescension**: Never tell the learner that a concept is "obvious", "trivial", or "simple". If an idea is tricky, show why with a small, concrete example.
- **Short sentences**: In Stages 0–2, keep sentences short and direct (target under 25 words; warning at 30 words). One idea per sentence.
- **Sentence-case headings**: Use sentence case for all headings (e.g., "Choosing good variable names", not "Choosing Good Variable Names").

---

## 2. Formatting and Punctuation

- **No em dashes**: Do not use em dashes (`—` or `--`) in prose or headings. Use commas, periods, or parentheses instead. (The only exception is typography inside bullet lists where a term is defined: `- **Term** — description`).
- **No bold overuse**: Bold terms only when first defined or introduced. Do not bold whole clauses for emphasis.
- **No emoji in content headings**: Keep headings clean and text-only.
- **Prose over bullet lists**: Do not turn explanations into lists of bullet points. Use paragraphs of connected prose. Reserve bullet lists strictly for genuine item sets or parameter options.
- **No "It's not X, it's Y" pivots**: State facts positively. Avoid "This is not about speed; it is about memory." Write: "This focuses on memory rather than speed."

---

## 3. Avoid-AI-Writing Rules

All content is drafted using the `avoid-ai-writing` skill with the `warm` voice and `docs` context.
- **Zero Tier 1 words**: Never use words like *delve*, *robust*, *leverage*, *pivotal*, *tapestry*, *realm*, *seamless*, *comprehensive*, *intricate*, *holistic*, *synergy*, *embark*, or *testament*.
- **No hollow intensifiers**: Cut *genuinely*, *truly*, *actually*, *real*, *quite frankly*, and *to be honest*.
- **No rule-of-three triads**: Avoid grouping adjectives or clauses into compulsive sets of three.
- **No vague endorsement**: Cut *worth exploring*, *worth checking out*, or *worth your time*. Explain specifically why a technique matters.

---

## 4. Contest Framing (R14 Rules)

- **No score targets or cutoffs**: Never mention "75/75", "full marks", "realistic score", "score ceiling", cutoffs, Honour Roll, or CCO qualification.
- **No speed disparagement**: Never state that Python "cannot solve" a problem or is "too slow". Teach proper algorithmic complexity and Python performance techniques (local variables, list comprehension, flat lists, fast I/O).
- **Subtask breakdown as objective fact only**: When teaching partial marks, state a problem's subtask bounds as an objective fact about that problem (e.g., "Subtask 1 guarantees N <= 100"). Never compare totals or set cutoff expectations.
- **Zero walkthroughs, editorials, or hints**: The app teaches concepts and algorithms on the author's own worked examples. It never solves a numbered CCC problem or provides hints.

---

## 5. Python 3.8 Code Conventions

- **Language level**: Python 3.8 (the CCC grader baseline). Do not use features from Python 3.9+ (no `:=` walrus operator outside bad38 error fixtures, no dictionary union `|`, no built-in generic types like `list[int]`).
- **Style**: Standard PEP 8 with 4-space indentation.
- **Naming**: `snake_case` for variables and functions, `UPPER_CASE` for constants.
- **House skeleton (from Stage 3 onward)**:
  ```python
  import sys


  def main() -> None:
      input_data = sys.stdin.read().split()
      if not input_data:
          return
      # algorithm implementation


  if __name__ == "__main__":
      main()
  ```

---

## 6. Visuals & Pedagogy

- **One concept per section**: Introduce one idea at a time.
- **Show, then tell, then show again**: Introduce the visual on a small input first, explain the mechanics, and follow with executable code.
- **Terminology synchronization**: The text, the visual stage, and the step captions must use identical terminology.

---

## 7. Teaching-Voice Sample (Approved Reference)

The following 414-word sample passage establishes the target voice for all modules:

### How Variables Work in Python

When you write a program, you need a way to hold on to data so you can use it later. In Python, you do that with a variable.

Think of a variable as a sticky note with a name written on it. When you assign a value, you place that sticky note onto an object in memory.

Look at this line of code:

```python
total = 12
```

Here is what Python does behind the scenes:
1. Python creates the integer number 12 in memory.
2. Python takes the name `total` and attaches it to that number 12.

From that moment on, whenever you write `total` in your code, Python follows the name to the number 12.

You can print it out:

```python
print(total)
```

The screen displays:
```
12
```

### Changing what a name points to

Now look at what happens when you write this next line:

```python
total = 25
```

A common beginner mistake is to imagine that Python erased the number 12 inside a box and wrote 25 in its place. Python does not do that. Numbers in Python cannot be edited in place.

Instead, Python creates a brand-new integer object with the value 25. Then it peels the name tag `total` off the number 12 and sticks it onto 25. The number 12 is left behind without any tag. Because nothing points to 12 anymore, Python quietly removes it from memory when it cleans up.

You can also use the current value of a variable to compute its next value:

```python
count = 5
count = count + 1
print(count)
```

When Python sees `count = count + 1`, it always evaluates the right side of the equals sign first.
1. It looks up `count`, which currently points to 5.
2. It adds 1 to 5, which produces the new number 6.
3. It takes the name `count` and attaches it to this new number 6.

The output is:
```
6
```

### Choosing good variable names

In contest problems, clear names save you from making silly mistakes when your code grows. Use lowercase letters, separating words with the underscore character.

A name like `left_pointer` or `current_weight` tells you what data it holds. Single letters like `i` or `j` are standard for simple loop counters, but avoid vague names like `temp2` or `data_val`. When you read your code ten minutes later, a clear name lets you follow your own logic without pausing to remember what you stored there.
