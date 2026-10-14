# ---
# DETAILS:
#   title: AI Agent
#   author: Andrew Seamana
#   date: 2026-10-12
# ---

# Utils
def format_insert(insert):
    insert = insert.strip().lower()

    if insert == "newline":
         insert = "\n"
    elif insert == "divider": 
        insert = "—————"

    print(insert)



# Import model
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")  # key can be anything

# Print the exact model names the server knows about
for m in client.models.list().data:
    print(m.id)

format_insert('newline')

response = client.chat.completions.create(
    model="gemma-4-12b-uncensored",  # use the id printed above if it differs
    messages=[
        {"role": "system", "content": "You are a helpful assistant. You reply very quickly unless the user specifies extra effort should be spent."},
        {"role": "user", "content": "Explain why bottom-up-processing is very difficult for level 1 autistic a 25 year-old male when trying to learn AI Agent Engineering."},
    ],
)
print(response.choices[0].message.content)
format_insert('divider')