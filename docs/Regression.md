## REGRESSION

> Regression can generally be classified into **Linear Regression** and **Logistic Regression**.  
>
> **Linear regression** is basically one of the simplest and quickest ways to predict numbers using a straight line yes, the word *line* is in it, that’s your first heads-up 😉.  
> **Logistic regression**, on the other hand, is used when the output is a yes or a no basically a boolean variable (Java obsession alert! 😆). Got the point? Good.  

---

### UNDERSTANDING SIMPLE LINEAR REGRESSION - THE FUTURE IS ONE CODE AWAY

#### Introduction to Linear Regression

Linear regression is a **supervised machine learning algorithm**. That word *supervised* alone should tell you something,it means it learns from **labeled datasets** to map data points.  
It uses **optimized linear functions** to make predictions.  

💡 Check out my **[Recovery Model for my Simulated Smart Manganese Plant Project](https://github.com/Darlene-13/Intelligent-Manganese-Processing-Plant-Optimization)**

Linear regression assumes a **linear relationship** between input and output — meaning a **constant rate of change** between the two. This relationship can be visualized perfectly as a straight line.

---

#### Examples to Make It Stick

1. Predict a student’s exam score based on study hours: students who study more hours are likely to score higher than those who study less.  

Here, we have **variables**:  
- **Independent variable**: hours studied  
- **Dependent variable**: exam score  

We can have **more than one independent variable**, and that’s called **multiple linear regression**.  
If there’s just one, it’s **simple linear regression**. Keep this in mind — we’ll revisit it 😎.

---

### WHY LINEAR REGRESSION THOUGH?

1. **Simplicity & Interpretability**  
   If you know **linear algebra**, kudos — linear regression is your playground! It embodies linear algebra through coefficient solving and predictions, making it the perfect starting point in ML.

2. **Predictive Ability**  
   Ever wanted to be a fortune teller 🔮? Linear regression is the next best thing. It predicts outcomes (not the future exactly), and it’s widely applicable: health, finance, marketing, and more.

3. **Foundation for Other Models**  
   Think of it as the **master key** 🔑. Advanced algorithms like logistic regression and neural networks build on linear regression.

4. **Efficiency**  
   Computationally light and efficient for problems with linear relationships.

---

> **NOTE:** A heatmap of correlations gives a **head-up** about which variables might have a linear relationship.  
> It doesn’t prove causation or guarantee linearity, but here’s why it helps:  
> 1. Shows correlation coefficients (e.g., Pearson’s r) between pairs of variables.  
> 2. Measures linear association — how well one variable fits a straight line of another.  
> 3. High absolute correlation (near 1 or -1) → strong linear trend; near 0 → weak or no trend.  

---

#### Best Line of Fit in Linear Regression

- In linear regression, the **best line of fit** is the straight line that most accurately represents the relationship between the input (independent variable) and output (dependent variable).  
1. **The goals?** Minimize the difference between actual data points and predicted values — always aim for that.  
   - Visualize it below 👇:

    ![BEST LINE OF FIT](src/models/BestLineOfFit.png)
 
   - The **Y** Axis is the dependent or the target variable and the **X** is the independent variable (the predictor of Y). There are many functions that can used in regression but a linear function is the simplest one.

2. **Equation of the Best-Line of Fit:** For simple linear regression (one independent variable the best line of fit can be represented by the normal linear equation we all know!):
     `y = mx + b`
    Where: y = Predicted value, x = input (dependent variable), m = slope of the line (gradient) and b is the intercept (the value of y when x = 0).

> The best line of fit is the line that optimuzed the values of (m) and (b) that is the gradient and the intercept so that that predicted values are close to the data points.

3. **Minimizing the Error: The Least Squares Method** Whoooa,,,chill chill chill don't freak out. Its actually interesting

    To find the best lien of fit we us a method called **Least Squares** you can find this in my previous documentation **[LEAST SQUARES METHOD](docs/Least_Squares.md)**