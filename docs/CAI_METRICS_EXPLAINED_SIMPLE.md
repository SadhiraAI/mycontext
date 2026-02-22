# Output Quality Metrics – Explained Like You're a Kid

---

## What is CAI (Context Amplification Index)?

**Simple idea:** Imagine you ask a friend for help with homework. One time you just say "help me." Another time you say "I need help with problem 3, it's about fractions, and I'm stuck on the part where you have to find the common denominator."

**Which answer is better?** The second one, right? Because you gave them a *structure* (a template) for what you need.

CAI measures: **Does using a good template make the AI's answer better?**

- **CAI > 1.0** = The template helped! Answer got better.
- **CAI < 1.0** = The template didn't help (or made it worse).
- **CAI = 1.0** = Same either way.

---

## The Five Metrics (What We Check)

### 1. **Instruction Following**  
*"Did it do what I asked?"*

Think of it like: You ask for a chocolate cake. You get … a chocolate cake. Good! You get a story about cakes instead. Bad!

**In kid words:** If you ask for 3 ideas and get 3 ideas = good. If you ask for a list and get a paragraph = bad. It's about following the rules you gave.

---

### 2. **Reasoning Depth**  
*"Did it actually think, or just guess?"*

Think of it like:
- Bad: "Because it's bad." (no real thinking)
- Good: "First X happened. That caused Y. So that's why we see Z." (shows the steps)

**In kid words:** Like showing your work in math class. We want to see HOW they got there, not just the final answer. Did they connect the dots?

---

### 3. **Actionability**  
*"Can I actually DO something with this?"*

Think of it like:
- Bad: "Things could be better." (okay, but what do I *do*?)
- Good: "Do these 3 things: 1) Call the doctor. 2) Take the medicine. 3) Rest for 2 days."

**In kid words:** It's like the difference between "clean your room" (vague) and "put toys in the bin, clothes in the hamper, books on the shelf" (you know exactly what to do). Actionable = you can actually use it.

---

### 4. **Structure Compliance**  
*"Did it use the format I wanted?"*

Think of it like: You asked for a recipe with "Ingredients" and "Steps." You get one giant paragraph. Bad! You get clear sections with headers. Good!

**In kid words:** If you asked for a list, did you get a list? If you asked for bullets, did you get bullets? It's about the *shape* of the answer matching what you asked for.

---

### 5. **Cognitive Scaffolding**  
*"Did it use the thinking framework I gave it?"*

Think of it like: You said "compare pros and cons." A bad answer just rambles. A good answer has a clear "Pros:" section and "Cons:" section — it used your framework.

**In kid words:** You gave the AI a *structure* for thinking (like a worksheet with boxes to fill in). Did it actually use those boxes? Or did it ignore your template and do its own thing?

---

## CAI Verdicts (What the Numbers Mean)

| CAI     | Verdict          | Kid Version                                        |
|--------|-------------------|----------------------------------------------------|
| ≥ 1.5  | Significant lift  | "The template really helped! Much better answer."  |
| ≥ 1.2  | Moderate lift     | "The template helped a good amount."               |
| ≥ 1.05 | Slight lift       | "The template helped a little."                    |
| 0.95–1.05 | Neutral       | "About the same either way."                       |
| < 0.95 | Negative lift     | "The template didn't help (maybe made it worse)."  |

---

## Quick Cheat Sheet

| Metric                | In One Sentence                                      |
|-----------------------|------------------------------------------------------|
| Instruction Following | Did it do what I asked?                               |
| Reasoning Depth       | Did it think step-by-step and explain why?            |
| Actionability         | Can I actually DO something with this?                |
| Structure Compliance  | Does it look like the format I asked for?             |
| Cognitive Scaffolding | Did it use my framework (pros/cons, cause/effect)?   |

---

## TL;DR

- **CAI** = How much better the answer gets when you use a good template.
- **The five metrics** = Did it follow instructions? Think deeply? Give you things to do? Use the right format? Use your framework?
- When CAI is high, your structured context is doing its job — it's making the AI's answers better.
