import json
import csv
from ghostpath.modules.shared import logger

def save_results(data, output_path, fmt="txt"):
    logger.debug(f"Saving results to '{output_path}' as format: {fmt}")

    try:
        if fmt == "txt":
            with open(output_path, "w") as f:
                for item in data:
                    f.write(f"{item}\n")

        elif fmt == "json":
            with open(output_path, "w") as f:
                json.dump(list(data), f, indent=2)

        elif fmt == "csv":
            with open(output_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["URL"])
                for item in data:
                    writer.writerow([item])

        logger.debug(f"Successfully saved output to: {output_path}")

    except Exception as e:
        logger.debug(f"Failed to save output: {e}")
        print(f"[!] Error saving results to file: {e}")
