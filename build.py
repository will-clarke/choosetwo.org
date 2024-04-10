import jinja2

environment = jinja2.Environment()
template_string = open("template.html").read()
template = environment.from_string(template_string)

index = template.render(
    h2="Life is short, make a conscious decision how to spend it",
    corner_top="Career",
    corner_right="Hobbies",
    corner_left="Family",
)

print(index)
