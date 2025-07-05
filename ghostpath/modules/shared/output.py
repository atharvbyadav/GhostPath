import json
import csv

def save_results(data, output_path, output_format):
    if output_format == "json":
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
    elif output_format == "csv":
        with open(output_path, "w", newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow([row])
    else:  # txt
        with open(output_path, "w") as f:
            for item in data:
                f.write(f"{item}\n")
