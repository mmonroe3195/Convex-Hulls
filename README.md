# Problem Set 1: Convex Hulls

## Setup

1. From the terminal, clone your repository with the command

    `git clone your_repository_link`

    where `repository_link` is likely of the form ```https://github.com/HamiltonCollege/ps01-convexhulls-username```.

2. `cd` into the directory created (of the form ps01-convexhulls-*username*), and replace or update *hull.py* with your functions from the assignment.

3. From the repository directory, run the timing code with 

    `python3 hull_timer.py`

    then type in one of the four experiment options

    `all noslow onlygraham hullsize`

    which will run a subset of the algorithms so that you can evaluate the running time.

## Evaluating growth rates

**Experiments**: `all`, `noslow`, `onlygraham`

In this experiment a single table is printed, one line at a time. On each line of the experimental output, the number of input points *n* doubles. Evaluate the growth rate of your algorithms by looking at how the running time grows with the number of points:

- For *O(n log n)* running time, you should see the running time approximately double as *n* doubles.
- For *O(nh)* running time, the experiment uses *h = n*; as *n* doubles you should see the running time approximately increase by a factor of 4.
- For *O(n^3)* running time, as *n* doubles you should see the running time approximately increase by a factor of 8.

*Suggestion*: first run `all`, if the *slow* algorithm makes it difficult to evaluate other running times, run `noslow`; if the *jarvis* algorithm makes it difficult to evaluate *graham*, run `onlygraham`.

**Experiments**: `hullsize`

In this experiment, multiple tables are printed, one line at a time. On each line of the experimental output, different values of *n* and *h* are printed. Within each table, *n* is fixed and *h* doubles (starting at 4, reaching *n*). Between tables, *n* doubles. For this experiment:

- For running time *O(nh)*, as *h* doubles, you should see the running time approximate double.

## Submitting

You only need to submit the file *hull.py*. The easiest way is to upload it to GitHub by opening your repository in a browser (you can find it by navigating to github.com and clicking the link on the left-hand side); then click the *Upload files* button, and drag *hull.py* to the browser window to update it.

Otherwise, from your repository directory on your machine, use `git` commands to submit your code with: 

`git add hull.py`

`git commit -m "commit message goes here"`

`git push origin master`
