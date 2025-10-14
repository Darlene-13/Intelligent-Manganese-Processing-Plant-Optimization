## REGRESSION

> Regression can generally be classified to Linear Regression and Logistic Regression. 
>
>Linear regression is basically one of the simplest and quickest ways to predict numbers using a straight like, (linear => The word line in it should give you a headsup). On the other hand logistic regression is used when the output is either a yes or a no,,,,I'd be tempted to say a boolean variable (that's how obsessed I am with java!). Point home? I guess.


### LINEAR REGRESSION
#### INTRODUCTION TO LINEAR REGRESSION
 Linear regression is a supervised machine learning algorithm. That line alone should tell you a lot. (Supervised) to mean it learns from labelled datasets and maps that has datapoints. 
 Linear regression has the most optimized linear functions which can be used in prediction. 
* Have a look at my **[Recovery Model for my Simulated smart manganese plant project.](https://github.com/Darlene-13/Intelligent-Manganese-Processing-Plant-Optimization)**

 Linear regression works with the assumption that there exists a linear relationship between the input and the output, this should tell you that there should be a constant rate of change between the two. The relationship can be well represented in a straight line.

 Wait wait wait! I learn with examples so why not give you some examples: 
1. If you wanted to predict a student's exam score based on how many hours they studied, a possible outcome would be that students who study more hours are likely to pass their exams compared to students who studied less hours. 

 Looking at that example you realize we have more than one variable. One is the dependent variable and the other is the independent variable, that's how relationships are formed the independent variable predicts the dependent variable.

 That brings us to: We can have more thna one independent variable in linear regression and that is called multiple linear regression....the opposite is true, simple linear regression. We will definetly come back to this, keep reading hahaha.

### WHY LINEAR REGRESSION THOUGH?

1. **Simplicity and Intepretability** If you know linear algebra then kudos you know linear regression because it embodies linear algebra by solving for co-efficients and computing predictions. It is the best starting point for machine learning
2. **Predictive Ability** I guess we've all at somepoint wanted to be witches who could predict the future, guess what, that where linear regression comes, it helps in predictions, not the future but kinda....this can be applied in various field eg: Health, Finance, Marketing etc.
3. **Base for Other Models** Should we call it the master key or what? Anyway most advance algorithms like logistic regssion or neural networks have built on linear regression.
4. **Efficiency** Linear regression is computatnally efficient for problems with a linear relationship.


> NOTE: Tell me if you agree with this. a heatmap of correlations gives us a head-up about which variables might have a linear relationshop, it does not really prove causation or guarantee linearity though...
> 
> Anyway I think it kinda does because: A heatmap usually shows correlation coefficients (like Pearson’s r) between pairs of variables. 
> 1. Pearson correlation measures linear association: how well one variable can be approximated as a straight-line function of another. 
> 2. High absolute correlation (near 1 or -1) suggests a strong linear trend, low correlation (near 0) suggests little to no linear trend.
 
Let's jump tot the interesting part for math lovers....

#### BEST LINE OF FIT IN LINEAR REGRESSION
- In linear regression the best line of fit is a straight line that most accurately represents the relationship between the input(independent variable) and the output (dependent variable). 
- This line basically aims in minimizing the difference between the actual data points and the predicted values from the model. That should always be the goal.
- Look at the graph below.

![BEST LINE OF FIT](src/models/BestLineOfFit.png)

