from datetime import datetime
from flask import Flask, render_template, request, session
from utils.geometry import (
    circle,
    cone,
    cube,
    cuboid,
    cylinder,
    ellipse,
    hexagon,
    pentagon,
    rhombus,
    sphere,
    square,
    trapezium,
    triangle,
    rectangle,
)

app = Flask(__name__)
app.secret_key = "replace-with-a-secret-key"


def add_history_entry(shape, inputs, results, unit):
    history = session.get("history", [])
    entry = {
        "shape": shape,
        "inputs": inputs,
        "results": results,
        "unit": unit,
        "timestamp": datetime.now().strftime("%d %B %Y %H:%M")
    }
    history.append(entry)
    session["history"] = history


# ------------------------------
# Home Page
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/formulas")
def formulas_page():
    return render_template("formulas.html")


@app.route("/history")
def history_page():
    history = session.get("history", [])
    return render_template("history.html", history=history)


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


# ------------------------------
# Rectangle Calculator
# ------------------------------
@app.route("/rectangle", methods=["GET", "POST"])
def rectangle_page():

    # When user opens the page for the first time
    if request.method == "GET":
        return render_template(
            "rectangle.html",
            length=None,
            width=None,
            area=None,
            perimeter=None,
            diagonal=None,
            unit="cm",
            scale=20,
            error=None
        )

    # ------------------------------
    # Read Form Data
    # ------------------------------
    unit = request.form.get("unit", "cm")

    try:
        length = float(request.form["length"])
        width = float(request.form["width"])

    except ValueError:
        return render_template(
            "rectangle.html",
            length=None,
            width=None,
            area=None,
            perimeter=None,
            diagonal=None,
            unit=unit,
            scale=20,
            error="Please enter valid numbers."
        )

    # ------------------------------
    # Validation
    # ------------------------------
    if length <= 0 or width <= 0:

        return render_template(
            "rectangle.html",
            length=length,
            width=width,
            area=None,
            perimeter=None,
            diagonal=None,
            unit=unit,
            scale=20,
            error="Length and Width must be greater than zero."
        )

    # ------------------------------
    # Perform Calculations
    # ------------------------------
    area, perimeter, diagonal = rectangle(length, width)

    # ------------------------------
    # Calculate Scale for SVG
    # ------------------------------
    max_size = max(length, width)
    if max_size <= 15:
        scale = 20
    elif max_size <= 30:
        scale = 12
    elif max_size <= 60:
        scale = 7
    else:
        scale = 3

    # ------------------------------
    # Send Results to HTML
    # ------------------------------
    add_history_entry(
        "Rectangle",
        {"Length": f"{length} {unit}", "Width": f"{width} {unit}"},
        {"Area": f"{area} {unit}²", "Perimeter": f"{perimeter} {unit}", "Diagonal": f"{round(diagonal,2)} {unit}"},
        unit
    )

    return render_template(
        "rectangle.html",
        length=length,
        width=width,
        area=area,
        perimeter=perimeter,
        diagonal=round(diagonal, 2),
        unit=unit,
        scale=scale,
        error=None
    )

@app.route("/square", methods=["GET", "POST"])
def square_page():

    if request.method == "GET":
        return render_template(
            "square.html",
            side=None,
            area=None,
            perimeter=None,
            diagonal=None,
            unit="cm",
            scale=20,
            error=None
        )

    unit = request.form.get("unit", "cm")

    try:
        side = float(request.form["side"])

    except ValueError:
        return render_template(
            "square.html",
            side=None,
            area=None,
            perimeter=None,
            diagonal=None,
            unit=unit,
            scale=20,
            error="Please enter a valid number."
        )

    if side <= 0:
        return render_template(
            "square.html",
            side=side,
            area=None,
            perimeter=None,
            diagonal=None,
            unit=unit,
            scale=20,
            error="Side must be greater than zero."
        )

    area, perimeter, diagonal = square(side)

    # Dynamic scaling
    MAX_DRAW_SIZE = 250
    scale = min(20, MAX_DRAW_SIZE / side)

    add_history_entry(
        "Square",
        {"Side": f"{side} {unit}"},
        {"Area": f"{area} {unit}²", "Perimeter": f"{perimeter} {unit}", "Diagonal": f"{round(diagonal,2)} {unit}"},
        unit
    )

    return render_template(
        "square.html",
        side=side,
        area=area,
        perimeter=perimeter,
        diagonal=round(diagonal, 2),
        unit=unit,
        scale=scale,
        error=None
    )

@app.route("/triangle", methods=["GET", "POST"])
def triangle_page():

    # ---------------- GET REQUEST ----------------
    if request.method == "GET":
        return render_template(
            "triangle.html",
            base=None,
            height=None,
            side1=None,
            side2=None,
            area=None,
            perimeter=None,
            triangle_type=None,
            unit="cm",
            scale=20,
            error=None
        )

    unit = request.form.get("unit", "cm")
    scale = 20

    # ---------------- READ INPUTS ----------------
    try:
        base = float(request.form["base"])
        height = float(request.form["height"])
        side1 = float(request.form["side1"])
        side2 = float(request.form["side2"])

    except ValueError:

        return render_template(
            "triangle.html",
            base=None,
            height=None,
            side1=None,
            side2=None,
            area=None,
            perimeter=None,
            triangle_type=None,
            unit=unit,
            scale=20,
            error="Please enter valid numbers."
        )

    # ---------------- POSITIVE VALUE CHECK ----------------
    if base <= 0 or height <= 0 or side1 <= 0 or side2 <= 0:

        return render_template(
            "triangle.html",
            base=base,
            height=height,
            side1=side1,
            side2=side2,
            area=None,
            perimeter=None,
            triangle_type=None,
            unit=unit,
            scale=20,
            error="All values must be greater than zero."
        )

    # ---------------- STEP 1 : TRIANGLE VALIDATION ----------------
    if (
        base + side1 <= side2 or
        base + side2 <= side1 or
        side1 + side2 <= base
    ):

        return render_template(
            "triangle.html",
            base=base,
            height=height,
            side1=side1,
            side2=side2,
            area=None,
            perimeter=None,
            triangle_type=None,
            unit=unit,
            scale=scale,
            error="Invalid Triangle! The given side lengths cannot form a triangle."
        )

    # ---------------- CALCULATE AREA & PERIMETER ----------------
    area, perimeter = triangle(base, height, side1, side2)
    # Maximum drawing area
    MAX_WIDTH = 300
    MAX_HEIGHT = 180
    
    # Scale based on both width and height
    scale_x = MAX_WIDTH / base
    scale_y = MAX_HEIGHT / height
    
    # Use the smaller scale so the triangle fits
    scale = min(scale_x, scale_y)

    # ---------------- DYNAMIC SCALING ----------------
    MAX_DRAW_SIZE = 250
    scale = min(20, MAX_DRAW_SIZE / max(base, height))

    # ---------------- STEP 2 : TRIANGLE TYPE ----------------
    if base == side1 == side2:
        triangle_type = "Equilateral"

    elif base == side1 or base == side2 or side1 == side2:
        triangle_type = "Isosceles"

    else:
        triangle_type = "Scalene"

    # ---------------- RETURN RESULT ----------------
    add_history_entry(
        "Triangle",
        {
            "Base": f"{base} {unit}",
            "Height": f"{height} {unit}",
            "Side 1": f"{side1} {unit}",
            "Side 2": f"{side2} {unit}"
        },
        {
            "Area": f"{round(area, 2)} {unit}²",
            "Perimeter": f"{round(perimeter, 2)} {unit}"
        },
        unit
    )

    return render_template(
        "triangle.html",
        base=base,
        height=height,
        side1=side1,
        side2=side2,
        area=round(area, 2),
        perimeter=round(perimeter, 2),
        triangle_type=triangle_type,
        unit=unit,
        scale=scale,
        error=None
    )


@app.route("/ellipse", methods=["GET", "POST"])
def ellipse_page():
    major_axis = None
    minor_axis = None
    area = None
    perimeter = None
    error = None
    scale = 20
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            major_axis = float(request.form["major_axis"])
            minor_axis = float(request.form["minor_axis"])
        except ValueError:
            error = "Please enter valid numbers."
        else:
            if major_axis <= 0 or minor_axis <= 0:
                error = "Major and Minor Axis must be greater than zero."
            else:
                area, perimeter = ellipse(major_axis, minor_axis)
                max_axis = max(major_axis, minor_axis)
                scale = min(20, 180 / max_axis)

                add_history_entry(
                    "Ellipse",
                    {
                        "Major Axis": f"{major_axis} {unit}",
                        "Minor Axis": f"{minor_axis} {unit}"
                    },
                    {
                        "Area": f"{area} {unit}²",
                        "Perimeter": f"{perimeter} {unit}"
                    },
                    unit
                )

    return render_template(
        "ellipse.html",
        major_axis=major_axis,
        minor_axis=minor_axis,
        area=area,
        perimeter=perimeter,
        scale=scale,
        unit=unit,
        error=error
    )


@app.route("/rhombus", methods=["GET", "POST"])
def rhombus_page():
    side = None
    diagonal1 = None
    diagonal2 = None
    area = None
    perimeter = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            side = float(request.form["side"])
            diagonal1 = float(request.form["diagonal1"])
            diagonal2 = float(request.form["diagonal2"])
        except ValueError:
            error = "Please enter valid numbers."
        else:
            if side <= 0 or diagonal1 <= 0 or diagonal2 <= 0:
                error = "All values must be greater than zero."
            else:
                area, perimeter = rhombus(side, diagonal1, diagonal2)

                add_history_entry(
                    "Rhombus",
                    {
                        "Side": f"{side} {unit}",
                        "Diagonal 1": f"{diagonal1} {unit}",
                        "Diagonal 2": f"{diagonal2} {unit}"
                    },
                    {
                        "Area": f"{area} {unit}²",
                        "Perimeter": f"{perimeter} {unit}"
                    },
                    unit
                )

    return render_template(
        "rhombus.html",
        side=side,
        diagonal1=diagonal1,
        diagonal2=diagonal2,
        area=area,
        perimeter=perimeter,
        unit=unit,
        error=error
    )


@app.route("/trapezium", methods=["GET", "POST"])
def trapezium_page():
    base_a = None
    base_b = None
    side_c = None
    side_d = None
    height = None
    area = None
    perimeter = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            base_a = float(request.form["base_a"])
            base_b = float(request.form["base_b"])
            side_c = float(request.form["side_c"])
            side_d = float(request.form["side_d"])
            height = float(request.form["height"])
        except ValueError:
            error = "Please enter valid numbers."
        else:
            if base_a <= 0 or base_b <= 0 or side_c <= 0 or side_d <= 0 or height <= 0:
                error = "All values must be greater than zero."
            else:
                area, perimeter = trapezium(base_a, base_b, side_c, side_d, height)

                add_history_entry(
                    "Trapezium",
                    {
                        "Base A": f"{base_a} {unit}",
                        "Base B": f"{base_b} {unit}",
                        "Side C": f"{side_c} {unit}",
                        "Side D": f"{side_d} {unit}",
                        "Height": f"{height} {unit}"
                    },
                    {
                        "Area": f"{area} {unit}²",
                        "Perimeter": f"{perimeter} {unit}"
                    },
                    unit
                )

    return render_template(
        "trapezium.html",
        base_a=base_a,
        base_b=base_b,
        side_c=side_c,
        side_d=side_d,
        height=height,
        area=area,
        perimeter=perimeter,
        unit=unit,
        error=error
    )


@app.route("/pentagon", methods=["GET", "POST"])
def pentagon_page():
    side = None
    area = None
    perimeter = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            side = float(request.form["side"])
        except ValueError:
            error = "Please enter a valid number."
        else:
            if side <= 0:
                error = "Side must be greater than zero."
            else:
                area, perimeter = pentagon(side)

                add_history_entry(
                    "Pentagon",
                    {"Side": f"{side} {unit}"},
                    {
                        "Area": f"{area} {unit}²",
                        "Perimeter": f"{perimeter} {unit}"
                    },
                    unit
                )

    return render_template(
        "pentagon.html",
        side=side,
        area=area,
        perimeter=perimeter,
        unit=unit,
        error=error
    )


@app.route("/hexagon", methods=["GET", "POST"])
def hexagon_page():
    side = None
    area = None
    perimeter = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            side = float(request.form["side"])
        except ValueError:
            error = "Please enter a valid number."
        else:
            if side <= 0:
                error = "Side must be greater than zero."
            else:
                area, perimeter = hexagon(side)

                add_history_entry(
                    "Hexagon",
                    {"Side": f"{side} {unit}"},
                    {
                        "Area": f"{area} {unit}²",
                        "Perimeter": f"{perimeter} {unit}"
                    },
                    unit
                )

    return render_template(
        "hexagon.html",
        side=side,
        area=area,
        perimeter=perimeter,
        unit=unit,
        error=error
    )


@app.route("/cube", methods=["GET", "POST"])
def cube_page():
    side = None
    surface_area = None
    volume = None
    diagonal = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            side = float(request.form["side"])
        except ValueError:
            error = "Please enter a valid number."
        else:
            if side <= 0:
                error = "Side must be greater than zero."
            else:
                surface_area, volume, diagonal = cube(side)

                add_history_entry(
                    "Cube",
                    {"Side": f"{side} {unit}"},
                    {
                        "Surface Area": f"{surface_area} {unit}²",
                        "Volume": f"{volume} {unit}³",
                        "Diagonal": f"{diagonal} {unit}"
                    },
                    unit
                )

    return render_template(
        "cube.html",
        side=side,
        surface_area=surface_area,
        volume=volume,
        diagonal=diagonal,
        unit=unit,
        error=error
    )


@app.route("/cuboid", methods=["GET", "POST"])
def cuboid_page():
    length = None
    width = None
    height = None
    surface_area = None
    volume = None
    diagonal = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            length = float(request.form["length"])
            width = float(request.form["width"])
            height = float(request.form["height"])
        except ValueError:
            error = "Please enter valid numbers."
        else:
            if length <= 0 or width <= 0 or height <= 0:
                error = "All values must be greater than zero."
            else:
                surface_area, volume, diagonal = cuboid(length, width, height)

                add_history_entry(
                    "Cuboid",
                    {
                        "Length": f"{length} {unit}",
                        "Width": f"{width} {unit}",
                        "Height": f"{height} {unit}"
                    },
                    {
                        "Surface Area": f"{surface_area} {unit}²",
                        "Volume": f"{volume} {unit}³",
                        "Diagonal": f"{diagonal} {unit}"
                    },
                    unit
                )

    return render_template(
        "cuboid.html",
        length=length,
        width=width,
        height=height,
        surface_area=surface_area,
        volume=volume,
        diagonal=diagonal,
        unit=unit,
        error=error
    )


@app.route("/cylinder", methods=["GET", "POST"])
def cylinder_page():
    radius = None
    height = None
    surface_area = None
    curved_surface_area = None
    volume = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            radius = float(request.form["radius"])
            height = float(request.form["height"])
        except ValueError:
            error = "Please enter valid numbers."
        else:
            if radius <= 0 or height <= 0:
                error = "Radius and Height must be greater than zero."
            else:
                surface_area, curved_surface_area, volume = cylinder(radius, height)

                add_history_entry(
                    "Cylinder",
                    {
                        "Radius": f"{radius} {unit}",
                        "Height": f"{height} {unit}"
                    },
                    {
                        "Surface Area": f"{surface_area} {unit}²",
                        "Curved Surface Area": f"{curved_surface_area} {unit}²",
                        "Volume": f"{volume} {unit}³"
                    },
                    unit
                )

    return render_template(
        "cylinder.html",
        radius=radius,
        height=height,
        surface_area=surface_area,
        curved_surface_area=curved_surface_area,
        volume=volume,
        unit=unit,
        error=error
    )


@app.route("/cone", methods=["GET", "POST"])
def cone_page():
    radius = None
    height = None
    surface_area = None
    slant_height = None
    volume = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            radius = float(request.form["radius"])
            height = float(request.form["height"])
        except ValueError:
            error = "Please enter valid numbers."
        else:
            if radius <= 0 or height <= 0:
                error = "Radius and Height must be greater than zero."
            else:
                surface_area, slant_height, volume = cone(radius, height)

                add_history_entry(
                    "Cone",
                    {
                        "Radius": f"{radius} {unit}",
                        "Height": f"{height} {unit}"
                    },
                    {
                        "Surface Area": f"{surface_area} {unit}²",
                        "Slant Height": f"{slant_height} {unit}",
                        "Volume": f"{volume} {unit}³"
                    },
                    unit
                )

    return render_template(
        "cone.html",
        radius=radius,
        height=height,
        surface_area=surface_area,
        slant_height=slant_height,
        volume=volume,
        unit=unit,
        error=error
    )


@app.route("/sphere", methods=["GET", "POST"])
def sphere_page():
    radius = None
    surface_area = None
    volume = None
    error = None
    unit = "cm"

    if request.method == "POST":
        unit = request.form.get("unit", "cm")

        try:
            radius = float(request.form["radius"])
        except ValueError:
            error = "Please enter a valid number."
        else:
            if radius <= 0:
                error = "Radius must be greater than zero."
            else:
                surface_area, volume = sphere(radius)

                add_history_entry(
                    "Sphere",
                    {"Radius": f"{radius} {unit}"},
                    {
                        "Surface Area": f"{surface_area} {unit}²",
                        "Volume": f"{volume} {unit}³"
                    },
                    unit
                )

    return render_template(
        "sphere.html",
        radius=radius,
        surface_area=surface_area,
        volume=volume,
        unit=unit,
        error=error
    )

@app.route("/circle", methods=["GET", "POST"])
def circle_page():

    radius = None
    area = None
    circumference = None
    diameter = None
    error = None
    scale = 20
    unit = "cm"

    if request.method == "POST":

        unit = request.form.get("unit", "cm")

        try:

            radius = float(request.form["radius"])

            if radius <= 0:
                raise ValueError("Radius must be greater than zero.")

            area, circumference, diameter = circle(radius)

            MAX_RADIUS = 120
            scale = MAX_RADIUS / radius
            if scale > 20:
                scale = 20

            add_history_entry(
                "Circle",
                {"Radius": f"{radius} {unit}"},
                {
                    "Area": f"{area} {unit}²",
                    "Circumference": f"{circumference} {unit}",
                    "Diameter": f"{diameter} {unit}"
                },
                unit
            )

        except ValueError as e:
            error = str(e)

    return render_template(
        "circle.html",
        radius=radius,
        area=area,
        circumference=circumference,
        diameter=diameter,
        scale=scale,
        unit=unit,
        error=error
    )


# ------------------------------
# Run Flask
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)