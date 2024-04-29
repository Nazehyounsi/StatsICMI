import os
import re
import numpy as np

# Path to the directory containing the text files
config_dir = "C:/Users/NEZIH YOUNSI/Desktop/AvgresultsConfig/NOZNOCD"

# Path to the output text file where results will be stored
output_file_path = "C:/Users/NEZIH YOUNSI/Desktop/AvgresultsConfig/NOZNOCD/AvgNOZNOCD.txt"


# Function to extract metrics from a single text file
def extract_metrics_from_file(file_path):
    metrics = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Extract metric name and value using a regular expression
            match = re.match(r'^(.*?):\s*(\d+\.?\d*)$', line.strip())
            if match:
                metric_name = match.group(1).strip()
                metric_value = float(match.group(2))
                if metric_name not in metrics:
                    metrics[metric_name] = []
                metrics[metric_name].append(metric_value)
    return metrics


# Aggregated metrics from all text files
aggregated_metrics = {}

# Loop through all text files in the configuration directory
for file_name in os.listdir(config_dir):
    if file_name.endswith('.txt'):  # Check for txt files
        file_path = os.path.join(config_dir, file_name)
        file_metrics = extract_metrics_from_file(file_path)

        # Add the metrics from this file to the aggregated metrics
        for metric_name, metric_values in file_metrics.items():
            if metric_name not in aggregated_metrics:
                aggregated_metrics[metric_name] = []
            aggregated_metrics[metric_name].extend(metric_values)

# Compute the mean and standard deviation for each metric
metric_averages = {}
metric_std_devs = {}

for metric_name, metric_values in aggregated_metrics.items():
    metric_averages[metric_name] = np.mean(metric_values)
    metric_std_devs[metric_name] = np.std(metric_values, ddof=1)  # ddof=1 for sample standard deviation

# Write the results to the output text file
with open(output_file_path, 'w') as output_file:
    # Write the metric averages
    output_file.write("Metric Averages:\n")
    for metric_name, metric_avg in metric_averages.items():
        output_file.write(f"{metric_name}: {metric_avg:.4f}\n")

    # Write the metric standard deviations
    output_file.write("\nMetric Standard Deviations:\n")
    for metric_name, metric_std in metric_std_devs.items():
        output_file.write(f"{metric_name}: {metric_std:.4f}\n")
