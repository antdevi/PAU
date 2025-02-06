import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# File paths
input_file = "data/scores.json"  # Original JSON file
output_file = "data/formatted_scores.json"  # Corrected JSON file

# Function to format and save JSON data
def format_json_file(input_file, output_file):
    try:
        # Read the JSON file line by line
        with open(input_file, 'r') as file:
            lines = file.readlines()
            formatted_data = [json.loads(line.strip()) for line in lines]

        # Save as a properly formatted JSON array
        with open(output_file, 'w') as file:
            json.dump(formatted_data, file, indent=4)

        print(f"Formatted JSON saved successfully as {output_file}")
        return output_file
    except Exception as e:
        print(f"Error processing JSON file: {e}")
        return None

# Function to create a progress table
def get_progress_table(json_file):
    try:
        with open(json_file, 'r') as file:
            quiz_data = json.load(file)

        if not quiz_data:
            print("Warning: JSON file is empty!")
            return None

        for entry in quiz_data:
            entry["date"] = datetime.datetime.fromisoformat(entry["timestamp"].replace("Z", "")).strftime("%Y-%m-%d")

        df = pd.DataFrame(quiz_data)

        if df.empty:
            print("Warning: DataFrame is empty after processing JSON!")
            return None

        progress_table = df.groupby("date")["score"].sum().reset_index()
        return progress_table
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return None

# Function to generate progress chart
def generate_progress_chart(progress_table, save_path="data/progress_chart.png"):
    try:
        if progress_table is None or progress_table.empty:
            print("Error: No data available to generate a chart.")
            return None

        # Ensure the 'data/' folder exists
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(progress_table["date"], progress_table["score"], color='blue')
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Score")
        ax.set_title("Quiz Progress Over Time")

        ax.set_xticks(range(len(progress_table["date"])))
        ax.set_xticklabels(progress_table["date"], rotation=45)

        # Save the graph instead of just displaying it
        fig.savefig(save_path, format="png")
        print(f"✅ Progress chart saved at {save_path}")

        plt.show()  # Display the chart as well
    except Exception as e:
        print(f"Error generating chart: {e}")
        return None

# Main execution
if __name__ == "__main__":
    formatted_file = format_json_file(input_file, output_file)

    if formatted_file:
        progress_data = get_progress_table(formatted_file)
        if progress_data is not None:
            generate_progress_chart(progress_data)
