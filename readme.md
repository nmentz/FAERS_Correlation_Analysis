# Surface Patterns and Hidden Biases in Drug Marketing and Safety Data

A preliminary analysis appears to suggest a positive correlation between the aggressiveness of pharmaceutical marketing campaigns and the number of reported adverse side effects. However, closer examination highlights how easily data can be misinterpreted without proper context. Marketing aggressiveness, approximated here through marketing expenditure data, and patient harm, assessed via adverse event reports from the FDA Adverse Event Reporting System (FAERS), both suffer from important measurement limitations. While a superficial relationship can be observed — aggressive marketing coinciding with higher reported harm — confounding factors complicate the picture. Possible explanations include increased drug utilization leading to more reports, reporting bias, discontinuities in FAERS drug classification (such as generics defaulting to brand names), and minor formulation differences. Critically, the data is not normalized against total prescription counts, making it impossible to distinguish whether more reports reflect greater inherent risk or simply broader use. Thus, the observed association serves less as evidence of causation and more as a case study in how preliminary patterns in incomplete datasets can misleadingly imply relationships that remain fundamentally uncertain.

Due to incomplete marketing data for a drug’s generic counterpart, the generic is assigned the same marketing expenditure value as the brand-name version in order to maintain consistency in categorization. Ozempic and Wegovy have the same generic.

![Alt Text](https://github.com/nmentz/FAERS_Correlation_Analysis/blob/master/Figure_1.png)

## Running This Yourself
You will need the following modules installed

 - [pandas](https://pandas.pydata.org/)
 - [seaborn](https://seaborn.pydata.org/)
 - [matplotlib](https://matplotlib.org/)

Installing these can be done in a few different ways. The safest way would be to spawn a python [virtual environment](https://docs.python.org/3/library/venv.html) and use pip to install them with ```pip install foo```. If you want to install modules directly to your filesystem, that's not a problem, but generally this should be done with a package manager to avoid any dependency conflicts, [brew](brew.sh) for mac, or whatever package manger is used on your linux distro.

Once you have these dependencies, you need to download [FAERS](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html) data. It is provided in quarterly. There will be an xml option and an ascii option, this program can only handle ascii. In main.py you can see how the the folders for Q1-Q4 for 2024 are quite literally unzipped and placed in the same folder as main.py, nothing fancy going on there. The hardest part will be finding pricing data. The best I could find were [estimations](https://www.fiercepharma.com/marketing/abbvie-pulls-hat-trick-3rd-straight-year-top-tv-drug-ad-spender-buoyed-skyrizi-and-rinvoq). Publically traded companies do tend to publically disclose their budget allocations, that might be a good place to look. Finding exact market data for a specific drug might prove challenging.