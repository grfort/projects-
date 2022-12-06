### Difference in Difference & Propensity Score Model

The Jupyter Notebook aims to replicate the results from the paper titled "Risk Targeting and Policy Illusions – Evidence from the
Announcement of the Volcker Rule". The paper estimates the impact of the Volcker Rule, a banking regulation implemented following the 2008 Financial crisis, which limits the amount of risk that banking institutions can undertake. Specifically, the affected banks are banks with a trading asset ratio of more than 3%. 

Based on the difference in difference model, the affected banks reduced their trading asset ratio for 2.34% more than the banks in the control group. To test the robustness of the results, a propensity score model was also conducted. Under the propensity score model, new control group is formed by selecting 3 K-Nearest Neighbours control banks with the closest propensity score for each bank in the treatment group. The control banks are selected with replacement. The results show that the results are robust with affected banks reducing their trading asset ratios by 2.98%. 
