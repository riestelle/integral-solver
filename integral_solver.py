import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from sympy import latex
from PIL import Image
import pytesseract

st.set_page_config(page_title="Integral Solver", layout="wide")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

x = sp.Symbol('x')

st.title("📐 Integral Solver with OCR Awareness")
st.markdown("""
Upload an image or manually enter a function to compute its integral.

⚠️ **Note:** OCR may not work well with graphs, handwritten math, or complex layouts.  
For best results, crop the image to just the printed expression or use [Mathpix](https://mathpix.com) for advanced math OCR.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📥 Input Section")

    uploaded_file = st.file_uploader("Upload an image of the function (optional)", type=["png", "jpg", "jpeg"])
    ocr_text = ""

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        ocr_text = pytesseract.image_to_string(image).strip().replace('\n', '')
        st.write("📄 OCR Extracted Text (may be inaccurate):")
        st.code(ocr_text)

    st.markdown("### Manually enter or correct the function below:")
    default_expr = ocr_text or ""
    expr_input = st.text_area("Function to integrate (in terms of x):", default_expr)

    with st.expander("ℹ️ Input Formatting Guide"):
        st.markdown("""
        ### ✍️ How to Write Math Expressions

        - `**` for exponents → `x**2` means \( x^2 \)  
        - `*` for multiplication → `3*x` means \( 3x \)  
        - Parentheses for grouping → `(x + 1)**2`  
        - `sqrt(x)` for square root → \( \sqrt{x} \)  

        ### 📐 Supported Functions

        - **Trigonometric:**  
          `sin(x)`, `cos(x)`, `tan(x)`, `cot(x)`, `sec(x)`, `csc(x)`  
        - **Inverse Trig:**  
          `asin(x)`, `acos(x)`, `atan(x)`, `acot(x)`, `asec(x)`, `acsc(x)`  
        - **Exponential & Logarithmic:**  
          `exp(x)`, `log(x)`  
        - **Hyperbolic:**  
          `sinh(x)`, `cosh(x)`, `tanh(x)`, etc.

        ### ✅ Examples

        - `x**2 + sin(x) - log(x)`  
        - `x**4 - 8*x**3 + 17*x**2 + 2*x - 24`

        ### ❌ Common Mistakes to Avoid

        - Using `^` for powers → use `**` instead  
        - Writing `3x` without `*` → use `3*x`  
        - Using non-Python syntax or ambiguous formatting
        """)

    integral_type = st.radio("Type of integral:", ["Indefinite", "Definite"])

    a = None
    b = None
    if integral_type == "Definite":
        a_input = st.text_input("Lower limit (a):")
        b_input = st.text_input("Upper limit (b):")
        try:
            a = float(a_input)
            b = float(b_input)
            if a > b:
                a, b = b, a
        except ValueError:
            st.warning("Please enter valid numeric limits for a and b.")
            st.stop()

    use_abs = st.checkbox("Compute total bounded area (ignore sign)", value=False)

with col2:
    st.subheader("📊 Integral Result and Graph")

    try:
        expr = sp.sympify(expr_input)
    except sp.SympifyError:
        st.error("Invalid expression. Please use valid sympy syntax or manually correct the OCR result.")
        st.stop()

    if st.button("Compute Integral"):
        try:
            f = sp.lambdify(x, expr, modules=['numpy'])
        except Exception as e:
            st.error(f"Error converting expression to function: {e}")
            st.stop()

        if integral_type == "Definite":
            x_vals = np.linspace(a, b, 400)
            y_vals = f(x_vals)
            if use_abs:
                y_vals = np.abs(y_vals)
                integral_numeric = np.trapz(y_vals, x_vals)
                integral_symbolic = "Numerical (abs): " + str(round(integral_numeric, 6))
            else:
                integral_symbolic = sp.integrate(expr, (x, a, b))
                integral_numeric = float(integral_symbolic.evalf())

            st.latex(r"\int_{" + str(a) + r"}^{" + str(b) + r"} " + latex(expr) + r"\, dx = " + str(integral_symbolic))
            st.write(f"Decimal Value: `{integral_numeric:.6f}`")
        else:
            integral_symbolic = sp.integrate(expr, x)
            st.latex(r"\int " + latex(expr) + r"\, dx = " + latex(integral_symbolic) + r" + C")
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_vals, y_vals, label=f'$f(x) = {latex(expr)}$', color='blue', linewidth=2)
        ax.axhline(0, color='black', linewidth=1.2)

        if integral_type == "Definite":
            ax.axvline(a, color='red', linestyle='--', linewidth=1.5, label=f'$x = {a}$')
            ax.axvline(b, color='red', linestyle='--', linewidth=1.5, label=f'$x = {b}$')
            ax.fill_between(x_vals, y_vals, 0, where=(x_vals >= a) & (x_vals <= b),
                            interpolate=True, color='skyblue', alpha=0.5)

        ax.set_title("Function Plot with Bounded Area", fontsize=16)
        ax.set_xlabel("x", fontsize=14)
        ax.set_ylabel("f(x)", fontsize=14)
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
    
# 📘 SETUP GUIDE: How to Run This Integral Solver App

# 1. 🔧 Install Required Libraries
# Run this in your terminal or command prompt:
# pip install streamlit sympy matplotlib numpy pillow pytesseract

# 2. 🧠 Install Tesseract OCR Engine
# Download and install from: https://github.com/tesseract-ocr/tesseract
# After installation, update the path in the script to match your system:
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# 3. 🚀 Run the App
# In your terminal, navigate to the folder containing this script and run:
# streamlit run your_script_name.py

# 4. 📂 Upload an Image (Optional)
# You can upload a math image (preferably cropped to just the printed expression).
# The app will extract the function using OCR and let you compute its integral.

# 5. ✍️ Manual Input
# If OCR fails or you prefer typing, enter the function manually using Python-style syntax:
# Example: x**4 - 8*x**3 + 17*x**2 + 2*x - 24

# 6. 📐 Choose Integral Type
# - Indefinite: Computes the general antiderivative
# - Definite: Computes the area under the curve between two bounds

# 7. 📊 View Results
# The app displays:
# - Symbolic integral (LaTeX)
# - Decimal value
# - Graph with shaded area, x-axis line, and vertical bounds

# ✅ You're all set! Customize, remix, and explore further as needed.
