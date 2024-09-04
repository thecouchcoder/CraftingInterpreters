import os


def define_ast(output_dir: str, base_name: str, types: list[str]):
    absolute = os.path.dirname(__file__)
    path = os.path.join(absolute + output_dir, base_name.lower() + ".py")
    if os.path.exists(path):
        os.remove(path)
    file = ""
    for t in types:
        class_name = t.split(":")[0].strip()
        fields = t.split(":")[1].strip()
        file = define_class(file, class_name, base_name, fields)
    with open(os.path.join(absolute + output_dir, base_name.lower() + ".py"), "w") as f:
        f.write(file)


def define_class(file, class_name, base_name, fields):
    file += "\n\n"
    fields = fields.split(",")
    types = list()
    identifiers = list()
    for field in fields:
        types.append(field.strip().split(" ")[0])
        identifiers.append(field.strip().split(" ")[1])

    file += "class " + class_name + ":\n"
    ctor = "    def __init__(self"
    assign = ""
    zipped = zip(types, identifiers)
    for itr in zipped:
        ctor += f", {itr[1]}"
        assign += f"        self.{itr[1]} = {itr[1]}\n"
    ctor += "):\n"
    file += ctor
    file += assign
    file += "\n"
    file += "    def accept(self, visitor):\n"
    file += (
        f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n"
    )
    return file


if __name__ == "__main__":
    define_ast(
        "../src/",
        "Expr",
        [
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : Object value",
            "Unary    : Token operator, Expr right",
        ],
    )
