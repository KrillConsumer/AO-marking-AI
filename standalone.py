from openai import OpenAI
import json

# can hide api key in future for security
api_key = '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'

client = OpenAI(api_key=api_key)

def evaluate_writing(grade, question, content, criteria):

    criteria_description = process_criteria(criteria)

    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "user", "content": f"Please evaluate the following piece of writing written by a grade {grade} student to the question '{question}' based on these criteria: {criteria_description}\n\n{content}"}
        ])
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def process_criteria(criteria):
    # Initialize an empty list to hold the formatted criteria strings
    criteria_strings = []

    # Loop through each main category ("Content_Form_Organization_Style", "Expression")
    for category, bands in criteria.items():
        # Add the category name as a header
        criteria_strings.append(f"{category} Criteria:\n")

        # Loop through each band within the category
        for band, descriptors in bands.items():
            # Add the band score range as a subheader
            criteria_strings.append(f"  Score {band}:")

            # Loop through each descriptor within the band and format it
            for descriptor, description in descriptors.items():
                criteria_strings.append(f"    - {descriptor}: {description}")

            # Add a newline for spacing after each band
            criteria_strings.append("")

    # Join all the criteria strings with newlines to form the final string
    return "\n".join(criteria_strings)

def main():
    with open('input.json', 'r') as file:
        data = json.load(file)
    
    grade = data.get('grade', '')
    question = data.get('question', '')

    try:
        with open('content.txt', 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    with open('narrative_rubric.json') as file:
        rubric = json.load(file)

    if not content or not rubric:
        print("Content or criteria missing.")
        return

    result = evaluate_writing(grade, question, content, rubric, api_key)
    print("\nEvaluation Result:\n", result)

if __name__ == '__main__':
    main()
