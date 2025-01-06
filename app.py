import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from EllipticCurveElGamal import EllipticCurveElGamal

# Streamlit app title
st.title("Elliptic Curve Visualization")

# Create an instance of EllipticCurveElGamal
ecc = EllipticCurveElGamal()

# Elliptic curve parameters
a, b, p = ecc.a, ecc.b, ecc.p

# Display elliptic curve parameters
st.subheader("Elliptic Curve Parameters")
st.latex(r"a = {}, \; b = {}, \; p = {}".format(a, b, p))

# 1. Plot the elliptic curve equation in real numbers
# Display the elliptic curve equation using st.latex
st.subheader("Elliptic Curve Equation")
st.latex(r"y^2 = x^3 + {}x + {}".format(a, b))

# Elliptic curve equation: y^2 = x^3 + ax + b


def elliptic_curve(x):
    """Use the elliptic curve equation defined in the class."""
    return ecc.elliptic_curve_equation(x)


# Generate x values for real number domain
x_values = np.linspace(-10, 10, 1000)
y_squared_values = elliptic_curve(x_values)

# Filter valid y values (real solutions only)
real_x = []
real_y_pos = []
real_y_neg = []

for x, y_squared in zip(x_values, y_squared_values):
    if y_squared >= 0:  # Only consider real solutions
        y = np.sqrt(y_squared)
        real_x.append(x)
        real_y_pos.append(y)
        real_y_neg.append(-y)

# Plot the continuous elliptic curve
fig1, ax1 = plt.subplots(figsize=(8, 8))
ax1.plot(real_x, real_y_pos, label="+sqrt(y^2)", color="red")
ax1.plot(real_x, real_y_neg, label="-sqrt(y^2)", color="red")
ax1.axhline(0, color="black", linewidth=0.5)  # x-axis
ax1.axvline(0, color="black", linewidth=0.5)  # y-axis
ax1.set_title("Elliptic Curve (Real Numbers)")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.legend()
ax1.grid()

# Display the first plot
st.pyplot(fig1)

# 2. Scatter plot for valid points on the curve
st.subheader("Valid Points on Elliptic Curve")
valid_points = ecc.valid_points
valid_points_x = [point.x for point in valid_points if not point.is_infinity()]
valid_points_y = [point.y for point in valid_points if not point.is_infinity()]

# Create scatter plot for valid points
fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.scatter(valid_points_x, valid_points_y,
            color="blue", label="Valid Points on Curve")
ax2.axhline(0, color="black", linewidth=0.5)  # x-axis
ax2.axvline(0, color="black", linewidth=0.5)  # y-axis
ax2.set_title("Valid Points on Elliptic Curve")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.legend()
ax2.grid()

# Display the second plot
st.pyplot(fig2)
