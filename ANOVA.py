import os
import re
import numpy as np
import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import MultiComparison

# Path to the main directory containing all configuration directories
main_dir = "C:/Users/NEZIH YOUNSI/Desktop/Configurations"

# Function to extract metrics from a single text file
def extract_metrics_from_file(file_path):
    metrics = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Extract metric name and value
            match = re.match(r'^(.*?):\s*(\d+\.?\d*)$', line.strip())
            if match:
                metric_name = match.group(1).strip()
                metric_value = float(match.group(2))
                metrics[metric_name] = metric_value
    return metrics

# Dictionary to store aggregated metric data across configurations
aggregated_data = []

# Loop over configuration directories
for config_dir in os.listdir(main_dir):
    config_path = os.path.join(main_dir, config_dir)

    if os.path.isdir(config_path):  # Ensure it's a directory
        # Loop over all text files in the configuration directory
        for file_name in os.listdir(config_path):
            if file_name.endswith('.txt'):  # Only process .txt files
                file_path = os.path.join(config_path, file_name)
                file_metrics = extract_metrics_from_file(file_path)

                # Store metric name, metric value, and configuration name
                for metric_name, metric_value in file_metrics.items():
                    aggregated_data.append({
                        'config_name': config_dir,
                        'metric_name': metric_name,
                        'metric_value': metric_value
                    })

# Prepare data for ANOVA
anova_data = {}

# Group metrics by metric name and configuration
for data_point in aggregated_data:
    metric_name = data_point['metric_name']
    config_name = data_point['config_name']
    metric_value = data_point['metric_value']

    if metric_name not in anova_data:
        anova_data[metric_name] = {}
    if config_name not in anova_data[metric_name]:
        anova_data[metric_name][config_name] = []

    anova_data[metric_name][config_name].append(metric_value)

# Perform ANOVA for each metric
anova_results = {}

for metric_name, metric_groups in anova_data.items():
    # Ensure each group has more than one observation
    if any(len(values) > 1 for values in metric_groups.values()) and len(metric_groups) >= 2:
        # Perform one-way ANOVA with the grouped data
        anova_result = f_oneway(*metric_groups.values())
        anova_results[metric_name] = anova_result
    else:
        anova_results[metric_name] = None  # Not enough data for ANOVA

# Output ANOVA results
print("ANOVA Results:")
post_hoc_results = {}
for metric_name, anova_result in anova_results.items():
    if anova_result:

        print(f"{metric_name}: F-statistic = {anova_result.statistic:.4f}, P-value = {anova_result.pvalue:.4f}")

        #COMMENT THe POST hoc PART IN ORDER TO SEE ANOVA EVENR FOR RESULTS WHERE P VALUE > 0.05
        # Only perform post-hoc analysis if the ANOVA result is significant
        if anova_result.pvalue < 0.05:
            # Create a DataFrame for post-hoc analysis
            df = pd.DataFrame(aggregated_data)
            # Select data for the current metric
            metric_df = df[df['metric_name'] == metric_name]

            # Perform Tukey's HSD
            mc = MultiComparison(metric_df['metric_value'], metric_df['config_name'])
            tukey_result = mc.tukeyhsd()

            # Store the post-hoc results
            post_hoc_results[metric_name] = tukey_result

            # Print post-hoc results
            print(f"Tukey's HSD for {metric_name}:")
            print(tukey_result)
            # Optional: Plot the post-hoc results
            tukey_result.plot_simultaneous()
    else:
        print(f"ANOVA could not be performed for '{metric_name}' due to insufficient data.")
