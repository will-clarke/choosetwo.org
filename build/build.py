import jinja2
import yaml
from typing import List, Optional
from pydantic import BaseModel, StrictStr

template_path = "template.html"
trilemma_path = "trilemma.yaml"


class Triangle(BaseModel):
    top: StrictStr
    right: StrictStr
    left: StrictStr


class Trillema(BaseModel):
    name: StrictStr
    url: StrictStr
    triangle: Triangle
    strapline: StrictStr
    source: Optional[StrictStr]


def read_trilemmas() -> List[Trillema]:
    with open(trilemma_path, "r") as stream:
        config = yaml.safe_load(stream)
        return [Trillema(**item) for item in config]


environment = jinja2.Environment()
template_string = open(template_path).read()
template = environment.from_string(template_string)


trilemmas = read_trilemmas()
previous_url = trilemmas[-1].url
for i, trilemma in enumerate(trilemmas):
    next_url = trilemmas[(i + 1) % len(trilemmas)].url
    html = template.render(
        h2=trilemma.name,
        corner_top=trilemma.triangle.top,
        corner_right=trilemma.triangle.right,
        corner_left=trilemma.triangle.left,
        strapline=trilemma.strapline,
        source=trilemma.source,
        previous_url=previous_url + ".html",
        next_url=trilemma.url + ".html",
    )
    previous_url = trilemma.url
    with open(f"../{trilemma.url}.html", "w") as f:
        f.write(html)
