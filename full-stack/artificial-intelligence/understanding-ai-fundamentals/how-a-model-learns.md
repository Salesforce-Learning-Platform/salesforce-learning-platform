# 📈 How a Model Actually Learns

## Data, Patterns, and Weights

A model doesn't start out knowing anything. It starts with **weights** — internal numeric values,
initially close to random — and is shown a large amount of **data**. Through a repeated process
covered next, those weights are gradually adjusted until the model's outputs start reflecting real
**patterns** present in that data. "The model learned X" really means: its internal weights shifted
into values that now produce outputs consistent with the patterns actually present in the training
data.

## What "Training" Actually Means

```
1. Show the model an input (e.g., part of a sentence)
2. The model makes a prediction (e.g., what word comes next)
3. Compare the prediction to the ACTUAL correct answer
4. Measure how wrong the prediction was — this is the LOSS
5. Adjust the weights slightly, in the direction that would have
   reduced that loss
6. Repeat this — millions or billions of times
```

**Training** is this repeated cycle, run an enormous number of times across an enormous amount of
data. Each individual adjustment is small; it's the sheer repetition, across a huge volume of
examples, that gradually shapes the weights into something genuinely useful.

## Loss — the Number That Drives Everything

**Loss** is a numerical measurement of exactly how wrong a model's prediction was, compared to the
real, correct answer. Google's own machine learning materials put it directly: "the goal of
training a model is to minimize the loss, reducing it to its lowest possible value." Every single
weight adjustment during training exists for one reason: to nudge the loss a little lower than it
was the step before.

## Why High-Quality Data Often Matters More Than a Cleverer Algorithm

```
A model trained on 10 million LOW-quality, noisy, inconsistent examples
often performs WORSE than one trained on 1 million carefully-curated,
accurate examples — even with the exact same underlying algorithm.
```

Since a model only ever learns the patterns actually present in its training data, data quality
directly caps what the model can possibly learn — no algorithm, however sophisticated, can learn a
correct pattern from consistently incorrect or noisy examples. This is why real AI teams invest
heavily in data quality and curation, often more than in algorithmic novelty.

## Common Mistakes

- Imagining training as the model being "told the rules" directly — it never is; every pattern it
  ends up reflecting was inferred purely from adjusting weights to reduce loss on real examples.
- Assuming a single training pass makes a model correct — real training runs this loss-reduction
  cycle an enormous number of times, and even then, the result is a statistical tendency, not a
  guarantee.
- Believing a bigger or more complex algorithm always beats better data — in practice, data quality
  is very often the more decisive factor.

## ➡️ Next

Continue to [what-parameters-mean.md](what-parameters-mean.md) to understand exactly what those
adjustable "weights" actually are, and why their count gets so much attention.
