import json
import os

json_file_path = "test/userdata/user_details.json"
md_file_path = "test/system_instruction/input_user.md"

def json_to_markdown(json_file_path, md_file_path):
    if not os.path.exists(json_file_path):
        print(f"No file found at {json_file_path}")
        return False
    
    with open(json_file_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        # Optionally, write a heading or introduction:
        md_file.write("# User Details\n\n")

        if isinstance(data, dict):
            # If 'data' is a dict, just iterate over its key-value pairs
            for key, value in data.items():
                md_file.write(f"**{key}**: {value}\n\n")

        elif isinstance(data, list):
            # Assuming each element of the list is an object containing "question" and "answer"
            for idx, item in enumerate(data, start=1):
                # Safely get question/answer, in case they don’t exist
                question = item.get("question", "No question found")
                answer = item.get("answer", "No answer found")

                # Write the data in your desired Markdown format
                md_file.write(f"## Q{idx}. {question}\n\n")
                md_file.write(f"**Answer**: {answer}\n\n")
                
        else:
            # If it's not a dict or list, just write the string representation
            md_file.write(str(data))
    
    print(f"Successfully converted {json_file_path} to {md_file_path}")
    return True

if __name__ == "__main__":
    json_to_markdown(json_file_path, md_file_path)
