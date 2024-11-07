from collections import defaultdict
from glob import glob
import os
import re

from openai import OpenAI

prompt = """
i need to be able to provide an article, book content, or something similar, extract the important points of the outline, and then create a hierarchical nested bulleted list markdown that shows the outline and organization of the original content.
""".strip()

client = OpenAI(base_url='http://127.0.0.1:5000/v1', api_key='asdf')

model = 'meta-llama_Llama-3.2-3B-Instruct'

def generate_text(message):
    resp = client.chat.completions.create(messages=[{'role': 'user', 'content': message}], model=model)
    return resp.choices[0].message.content

sections_re = re.compile('(^|\n)# ')

section_prompt = """
an AI can be improved by giving it structured examples of what the user wants. for this, we have a collection of prompt templates. they outline a common recurring need, which are then appended with new information to analyze or produce new information based on the recurring need. for example, if we want to write some code, we can have a template which says, "You are an expert software engineer with particular experience in Python and cross-platform applications." The template then goes on to explain how "You are especially experienced with ensuring bug-free, secure code." This helps prime the LLM for a new prompt which could include specific information, for example, "Please write a function which calculates the sum of a list of numbers."

Following are several examples from existing templates from various domains. The user is requesting a new template for a new domain. Please focus on the examples below; understand their domain, and how they are structured. Notice that they are written in second person, "You are.."

## Example 1

You are a PHD expert on the subject defined in the input section provided below.

## Example 2

You are an expert on writing concise, clear, and illuminating essays on the topic of the input provided.

## Example 3

You are an expert at writing Semgrep rules.

Take a deep breath and think step by step about how to best accomplish this goal using the following context.

# CURRENT CHALLENGE

above are examples from several '{section_title}' sections from existing patterns. we need to produce a new similar section for a new pattern, but the use case is the following:

{prompt}

Don't acknowledge, introduce, or explain. Only write the section requested. please write a new '{section_title}' section for the use case outlined above:

# IDENTITY and PURPOSE
"""


patterns_dir = os.path.expanduser('~/.config/fabric/patterns')
pattern_files = glob(os.path.join(patterns_dir, '*', 'system.md'))


grouped_sections = defaultdict(list)
for pattern_file in pattern_files:
    with open(pattern_file, 'r') as fr:
        content = fr.read()

    sections = sections_re.split(content)
    sections = list(filter(lambda s: s.strip(), sections))
    for i in range(len(sections)):
        section = sections[i]
        if '\n' not in section:
            continue
        title, content = section.split('\n', maxsplit=1)
        title = title.strip().rstrip(':')
        content = content.strip()
        grouped_sections[title].append(content)
    pass

removal_keys = []
for k, v in grouped_sections.items():
    if len(v) < 5:
        removal_keys.append(k)

for k in removal_keys:
    grouped_sections.pop(k)

section_aliases = {
    'GOAL': ['GOALS'],
    'IDENTITY and PURPOSE': [
        'IDENTITY AND GOALS',
        'IDENTITY',
    ],
    'STEPS': ['Steps'],
}

for key, titles in section_aliases.items():
    main_section = grouped_sections[key]
    for alt_title in titles:
        main_section.extend(grouped_sections.pop(alt_title))

# for section in sorted(grouped_sections):
#     print("#######################")
#     print(f"'{section}'")
#     print(len(grouped_sections[section]))

important_sections = [
    'IDENTITY and PURPOSE',
]

with open('new_pattern.md', 'w') as fw:
    for title in important_sections:
        examples = grouped_sections[title]
        three_examples = examples[:3]
        for i in range(len(three_examples)):
            example = three_examples[i]
            example = f"## Example {i}\n\n{example}\n"
            three_examples[i] = example
        examples_text = ''.join(three_examples)
        current_prompt = examples_text + '\n\n' + section_prompt.format(section_title=title, prompt=prompt)
        print(f'full current prompt:\n##################################\n{current_prompt}\n###################################')
        exit()
        response = generate_text(current_prompt)
        print(f"# {title}\n\n", file=fw)
        print(response, file=fw)

