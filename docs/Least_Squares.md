#### LEAST SQUARES METHOD

> The Least Squares Method is a popular mathematical trick used in data fitting and regression.
> It finds the best-fit line or curve by **minimizing the sum of squared differences** between your actual data points and the predicted values.
> You’ll see it everywhere — in **statistics, machine learning, and engineering** — because it’s simple, powerful, and gets the job done. Guess that is what we all love, getting the job done 😂

---

In the Least Squares Method, we try to represent all the data points with a **straight line**, usually written as:

```markdown
y = mx + c
```

This helps us **predict the dependent variable (y)** for a given independent variable (x), even if the value was initially unknown. Remember how we talked about relationships? Yep, this is it! 😎

You might ask yourself: **Why use the Least Squares Method?**
Well, if you’ve done some math, you know the **Cartesian plane**. Scatter plots are just collections of points on this plane. By themselves, they don’t tell the full story — we need a line that best represents the trend in the data. That’s where LSM comes in.

---

### LEAST SQUARE METHOD FORMULAS

**Slope (m):**

```
m = [n(Σxy) − (Σx)(Σy)] / [n(Σx²) − (Σx)²]
```

**Intercept (c):**

```
c = (Σy − m(Σx)) / n
```

Where:

* n = number of data points
* Σxy = sum of the product of each pair of x and y values
* Σx = sum of all x values
* Σy = sum of all y values
* Σx² = sum of the squares of the x values

---

### STEP-BY-STEP METHOD TO FIND THE LINE OF BEST FIT

1. Denote **independent variable values** as `x_i` and **dependent variable values** as `y_i`.
2. Calculate the averages `X` (mean of x_i) and `Y` (mean of y_i).
3. Assume the line equation: `y = mx + c` (m = slope, c = intercept).
4. Calculate the slope:

```
m = Σ((x_i - X)*(y_i - Y)) / Σ((x_i - X)²)
```

5. Calculate the intercept:

```
c = Y - mX
```

6. Your **line of best fit** is `y = mx + c`. 🎯

These formulas **minimize the sum of squared differences** between observed and predicted values — hence “Least Squares.”

---

### LIMITATIONS

* Assumes data is **evenly distributed** and **outlier-free**.
* May produce inaccurate results for unevenly distributed data or datasets with outliers.

---

### HOW TO CALCULATE LEAST SQUARES

1. Determine the line you think best fits the data.
2. Calculate **residuals** (differences between observed and predicted values).
3. **Square each residual** and sum them up.
4. Adjust your model to **minimize this sum**.

---

### LEAST SQUARE METHOD EXAMPLE

Suppose we have the following dataset of study hours vs. exam scores:

| Hours Studied (x) | Exam Score (y) |
| ----------------- | -------------- |
| 2                 | 65             |
| 3                 | 70             |
| 5                 | 75             |
| 7                 | 85             |
| 9                 | 95             |

1. Compute averages:

   * X = (2+3+5+7+9)/5 = 5.2
   * Y = (65+70+75+85+95)/5 = 78

2. Calculate slope `m` and intercept `c` using the formulas:

```
m = Σ((x_i - X)*(y_i - Y)) / Σ((x_i - X)²) ≈ 4.25
c = Y - mX ≈ 56
```

3. Line of best fit:

```
y = 4.25x + 56
```

✅ Now we can **predict the exam score** for any number of study hours using this line.

---
