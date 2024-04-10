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

index = template.render(
    h2="Life is short, make a conscious decision how to spend it",
    corner_top="Career",
    corner_right="Hobbies",
    corner_left="Family",
)

trilemmas = read_trilemmas()
for trilema in trilemmas:
    html = template.render(
        h2=trilema.name,
        corner_top=trilema.triangle.top,
        corner_right=trilema.triangle.right,
        corner_left=trilema.triangle.left,
        strapline=trilema.strapline,
        source=trilema.source,
    )
    with open(f"../{trilema.url}.html", "w") as f:
        f.write(html)
