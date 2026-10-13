# IPL Eye-In: How Many Balls Until a Batter Gets Set?

## 1. Project Overview

Cricket commentators often say that a batter needs time to "get their eye in." But how many balls does it actually take for a batter to become comfortable at the crease?

This project investigates how a batter's scoring rate and dismissal frequency change as they face more balls in an innings, using IPL ball-by-ball data.

The project uses Python, data analysis, linear regression, polynomial regression, and bootstrap confidence intervals to investigate the eye-in effect.

## 2. Objectives

- Analyse dismissal frequency at different ball positions.
- Understand how strike rate changes during the first 30 balls.
- Compare batting trends across the powerplay, middle overs, and death overs.
- Identify batters with large observed scoring-rate improvements.
- Compare linear and polynomial regression models.
- Estimate uncertainty in player-level scoring improvements.

## 3. Dataset

**Source:** [Cricsheet](https://cricsheet.org/)

The dataset consists of IPL ball-by-ball JSON files.

Current processed dataset statistics:

- Raw delivery records: 295,732
- Deliveries counted as balls faced: 285,856
- Unique batter innings: 18,837
- Unique batters: 738
- Dismissal-event deliveries on wides: 58

The dataset includes match information, batter and bowler names, runs, delivery types, dismissal events, and the number of balls faced by each batter in an innings.

## 4. Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Bootstrap resampling
- Streamlit (optional dashboard)

## 5. Methodology

### A. Data Preprocessing

The Cricsheet JSON files are loaded and converted into a tabular dataset.

The preprocessing steps include:

- Extracting ball-by-ball match information.
- Identifying batter, bowler, runs, and dismissal events.
- Excluding wides from balls-faced counts.
- Calculating each batter's ball position within an innings.
- Assigning deliveries to powerplay, middle, and death phases.

### B. Scoring-Rate Analysis

Strike rate is calculated using:

Strike Rate = (Runs Scored / Balls Faced) × 100

The scoring rate is calculated at each ball position to investigate how batting performance changes as the innings progresses.

### C. Dismissal-Frequency Analysis

Dismissal frequency is calculated at each ball position:

Dismissal Frequency = (Dismissals / Batter Innings Reaching That Position) × 100

The number of innings reaching each ball position decreases as the position increases. Later-ball estimates must therefore be interpreted cautiously.

Dismissals on wides are tracked separately because wides do not count as balls faced.

### D. Regression Models

Two models are compared:

**Linear Regression**

Models a straight-line relationship between balls faced and strike rate.

**Polynomial Regression**

Models a curved relationship between balls faced and strike rate.

The models are evaluated using:

- R² score
- Root Mean Squared Error (RMSE)

### E. Eye-In Index

The Eye-In Index measures the difference between a batter's strike rate after ball 20 and during their first 10 balls.

Eye-In Improvement = After-20 Strike Rate − First-10 Strike Rate

A positive value indicates a higher observed strike rate in the later period.

Bootstrap resampling is used to estimate a 95% confidence interval for the scoring-rate difference.

## 6. Preliminary Results

### Regression Comparison

Previously recorded test-set results:

| Model | Test R² | Test RMSE |
|---|---:|---:|
| Linear Regression | 0.8163 | 13.3547 |
| Polynomial Regression | 0.8174 | 13.3170 |

Polynomial regression performed slightly better on the reported test metrics. The improvement was small, so the results do not establish a substantial advantage over linear regression.

### Example: DA Miller

The current bootstrap analysis reports:

- First-period innings: 144
- Later-period innings: 41
- First-10 strike rate: approximately 111.30
- After-20 strike rate: approximately 192.70
- Scoring-rate improvement: approximately 81.40 points
- 95% bootstrap interval: approximately 55.56 to 106.66

This result shows a higher observed strike rate after ball 20. It does not prove that facing more balls causes the improvement.

### Dismissal Frequency

The current graph shows approximately:

- Ball 1: 4.03%
- Ball 2: 4.27%
- Ball 7: 5.18%
- Ball 20: 5.41%

The dismissal frequency fluctuates across ball positions. Later positions have fewer observations, so their estimates may be less stable.

## 7. Project Structure

```text
Cricket_Prediction/
├── README.md
├── app/
├── data/
│   ├── raw/
│   └── processed/
├── eye-in/
├── notebooks/
└── src/
    ├── analysis.py
    ├── confidence_intervals.py
    ├── data_loader.py
    ├── feature_engineering.py
    ├── player_ranking.py
    └── regression_models.py
```

Keep the structure consistent with the files actually present in the project.

## 8. Installation

Install the main dependencies:

```bash
pip install pandas numpy matplotlib scikit-learn jupyter
```

For the optional Streamlit dashboard:

```bash
pip install streamlit
```

## 9. How to Run the Project

1. Download the IPL JSON data from Cricsheet.
2. Place the JSON files in `data/raw/`.
3. Open the project in VS Code.
4. Start Jupyter Notebook.
5. Open the analysis notebook in the `notebooks/` folder.
6. Run the notebook cells in order, starting with data loading and preprocessing.
7. Generate the metrics, regression comparisons, and visualizations.

## 10. Limitations

- Batters who reach ball 20 form a selected group, creating survivor bias.
- Batting position, opposition, venue, match phase, and match situation can influence scoring.
- Player estimates based on fewer innings have greater uncertainty.
- Bootstrap intervals quantify sampling uncertainty but do not eliminate selection bias.
- Dismissal frequency at a ball position is not the same as conditional dismissal probability or survival probability.
- Regression describes relationships in the observed data and does not establish causation.
- Results depend on the selected IPL seasons and preprocessing decisions.

## 11. Conclusion

This project investigates the cricket concept of getting one's eye in using ball-by-ball data rather than relying only on commentary or intuition.

By combining scoring-rate analysis, dismissal-frequency analysis, regression models, player comparisons, and bootstrap confidence intervals, it provides a quantitative view of how batting performance varies with balls faced.

The findings should be interpreted with attention to sample size, selection bias, and match context.

## 12. Acknowledgements

The ball-by-ball dataset is provided by [Cricsheet](https://cricsheet.org/). Please follow its applicable data-use and attribution requirements.
