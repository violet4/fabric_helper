# fabric_helper

Enhance Daniel Miessler's Fabric to be able to easily write new patterns.

Use LLMs to analyze the structure and content of existing patterns to write new patterns.

Example usage:

`fabric_helper 'please make a new pattern which can be used to help me organize and outline information. it needs to be especially skilled with markdown format, particularly nested bullet/numbered lists. i should be able to feed it an essay and ask it to generate a well structured bullet-point-format outline.'`

* Automatically titles the pattern and places it in your patterns folder (for example, on linux that's `~/.config/fabric/patterns/my_new_pattern/system.md`) with an appropriate name befitting the new pattern.

# How it works

Extract the common sections out of the existing patterns. For example, all of the "IDENTITY and PURPOSE"s, all of the "Steps" sections, etc. It will gather some small number of representative "IDENTITY and PURPOSE" sections, then given the overall prompt: "Please write a new IDENTITY and PURPOSE section in the style of the IDENTITY and PURPOSE sections listed above, for the following prompt." Then, do this for each section of the new pattern, constructing each piece and stitching it together into a single cohesive new pattern.
