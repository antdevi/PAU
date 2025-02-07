import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os 

# File paths
INPUT_FILE = "data/scores.json"  # Original JSON file
OUTPUT_FILE = "data/formatted_scores.json"  # Corrected JSON file
STATIC_FOLDER = "static"
def format_json_file(input_file= INPUT_FILE, output_file=OUTPUT_FILE):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            formatted_data = [json.loads(line.strip()) for line in lines]

        with open(output_file, 'w') as file:
            json.dump(formatted_data, file, indent=4)

        print(f"✅ Formatted JSON saved at {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Error processing JSON: {e}")
        return None

# Function to create a progress table
def get_progress_table(json_file=OUTPUT_FILE):
    try:
        with open(json_file, 'r') as file:
            quiz_data = json.load(file)

        if not quiz_data:
            print("⚠️ Warning: JSON file is empty!")
            return None

        for entry in quiz_data:
            entry["date"] = datetime.datetime.fromisoformat(entry["timestamp"].replace("Z", "")).strftime("%Y-%m-%d")

        df = pd.DataFrame(quiz_data)

        if df.empty:
            print("⚠️ Warning: DataFrame is empty after processing JSON!")
            return None

        progress_table = df.groupby("date")["score"].sum().reset_index()
        return progress_table
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        return None

# Function to generate progress chart
def generate_progress_chart(progress_table, save_path=os.path.join(STATIC_FOLDER, "progress_chart.png")):
    try:
        if progress_table is None or progress_table.empty:
            print("❌ Error: No data available to generate a chart.")
            return None

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(progress_table["date"], progress_table["score"], color='blue')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Total Score", fontsize=12)
        ax.set_title("Quiz Progress Over Time", fontsize=14)

        ax.set_xticks(range(len(progress_table["date"])))
        ax.set_xticklabels(progress_table["date"], rotation=0, ha='center', fontsize=10)

        plt.subplots_adjust(bottom=0.15)
        plt.tight_layout()

        fig.savefig(save_path, format="png", dpi=200)
        print(f"✅ Progress chart saved at {save_path}")

        plt.close(fig)
        return save_path
    except Exception as e:
        print(f"❌ Error generating chart: {e}")
        return None

# Main execution (Only runs if executed directly)
if __name__ == "__main__":
    formatted_file = format_json_file()
    if formatted_file:
        progress_data = get_progress_table(formatted_file)
        if progress_data is not None:
            generate_progress_chart(progress_data)