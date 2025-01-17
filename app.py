from flask import Flask, render_template, request, jsonify
from sympy import symbols, sympify
from scipy.optimize import brentq

app = Flask(__name__)

x = symbols('x')

# Bisection Method
def bisection_method(func, x, xl, xu, tol, max_iter):
    steps = []
    
    if abs(func.subs(x, xl)) < tol:
        return [{'iteration': 1, 'xl': xl, 'xu': xu, 'xr': xl, 'fxl': 0, 'fxu': func.subs(x, xu), 'fxr': 0, 'fxl_fxr': 0, 'formula': f"x_r = {xl}", 'update': f"f(xl) \\times f(x_r) = 0"}]
    if abs(func.subs(x, xu)) < tol:
        return [{'iteration': 1, 'xl': xl, 'xu': xu, 'xr': xu, 'fxl': func.subs(x, xl), 'fxu': 0, 'fxr': 0, 'fxl_fxr': 0, 'formula': f"x_r = {xu}", 'update': f"f(xl) \\times f(x_r) = 0"}]
    
    for i in range(max_iter):
        fxl = float(func.subs(x, xl))
        fxu = float(func.subs(x, xu))
        xr = (xl + xu) / 2
        fxr = float(func.subs(x, xr))

        step_info = {
            'iteration': i + 1,
            'xl': xl,
            'xu': xu,
            'xr': xr,
            'fxl': fxl,
            'fxu': fxu,
            'fxr': fxr,
            'fxl_fxr': fxl * fxr,
            'formula': f"x_r = \\frac{{xl + xu}}{{2}} = \\frac{{{xl} + {xu}}}{{2}} = {xr:.6f}",
            'update': f"f(xl) \\times f(x_r) = {fxl:.6f} \\times {fxr:.6f}"
        }

        steps.append(step_info)

        if abs(fxr) < tol or (xu - xl) / 2 < tol:
            break

        if fxl * fxr < 0:
            xu = xr
        else:
            xl = xr

    if abs(func.subs(x, xr)) >= tol:
        raise ValueError(f"Gagal menghitung akar : Interval tidak memenuhi syarat Bisection f(xl)*f(xu) > 0. Pilih interval yang sesuai!")
    
    return steps

# Regula Falsi Method
def regula_falsi_method(func, x, xl, xu, tol, max_iter):
    steps = []

    if abs(func.subs(x, xl)) < tol:
        return [{'iteration': 1, 'xl': xl, 'xu': xu, 'xr': xl, 'fxl': 0, 'fxu': func.subs(x, xu), 'fxr': 0, 'fxl_fxr': 0, 'formula': f"x_r = {xl}", 'update': f"f(xl) \\times f(x_r) = 0"}]
    if abs(func.subs(x, xu)) < tol:
        return [{'iteration': 1, 'xl': xl, 'xu': xu, 'xr': xu, 'fxl': func.subs(x, xl), 'fxu': 0, 'fxr': 0, 'fxl_fxr': 0, 'formula': f"x_r = {xu}", 'update': f"f(xl) \\times f(x_r) = 0"}]

    for i in range(max_iter):
        fxl = float(func.subs(x, xl))
        fxu = float(func.subs(x, xu))
        xr = xu - (fxu * (xu - xl)) / (fxu - fxl)
        fxr = float(func.subs(x, xr))

        step_info = {
            'iteration': i + 1,
            'xl': xl,
            'xu': xu,
            'xr': xr,
            'fxl': fxl,
            'fxu': fxu,
            'fxr': fxr,
            'fxl_fxr': fxl * fxr,
            'formula': f"x_r = xu - \\frac{{f(xu)(xu-xl)}}{{f(xu)-f(xl)}} = {xr:.6f}",
            'update': f"f(xl) \\times f(x_r) = {fxl:.6f} \\times {fxr:.6f}"
        }

        steps.append(step_info)

        if abs(fxr) < tol:
            break

        if fxl * fxr < 0:
            xu = xr
        else:
            xl = xr

    if abs(func.subs(x, xr)) >= tol:
        raise ValueError(f"Gagal menghitung akar : Interval tidak memenuhi syarat Regula-Falsi f(xl)*f(xu) > 0. Pilih interval yang sesuai!")

    return steps

# Brent Method
def brent_method(func, x, xl, xu, tol, max_iter):
    steps = []

    for i in range(max_iter):
        # Menggunakan brentq dari scipy untuk menghitung nilai akar
        xr = brentq(lambda t: float(func.subs(x, t)), xl, xu, xtol=tol)

        fxl = float(func.subs(x, xl))
        fxu = float(func.subs(x, xu))
        fxr = float(func.subs(x, xr))

        # Menyimpan langkah-langkah iterasi
        step_info = {
            'iteration': i + 1,
            'xl': xl,
            'xu': xu,
            'xr': xr,
            'fxl': fxl,
            'fxu': fxu,
            'fxr': fxr,
            'fxl_fxr': fxl * fxr,
            'formula': f"x_r = \\text{{brentq}}(f(x), {xl}, {xu}) = {xr:.6f}",
            'update': f"f(xl) \\times f(xr) = {fxl:.6f} \\times {fxr:.6f}"
        }

        steps.append(step_info)

        if abs(fxr) < tol:
            break

        # Update interval
        if fxl * fxr < 0:
            xu = xr
        else:
            xl = xr

    if abs(func.subs(x, xr)) >= tol:
        raise ValueError(f"Gagal menghitung akar : Interval tidak memenuhi syarat Brent f(xl)*f(xu) > 0. Pilih interval yang sesuai!")

    return steps

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk perhitungan
@app.route('/calculate', methods=['POST'])
def calculate():
    func_str = request.form['function']
    a = float(request.form['a'])
    b = float(request.form['b'])
    tol = float(request.form['tolerance'])
    max_iter = int(request.form['iterations'])

    if 'method' not in request.form:
        return jsonify({'error': 'Method is required'}), 400

    method = request.form['method']
    func = sympify(func_str)
    steps = []

    try:
        if method == 'bisection':
            steps = bisection_method(func, x, a, b, tol, max_iter)
        elif method == 'regula_falsi':
            steps = regula_falsi_method(func, x, a, b, tol, max_iter)
        elif method == 'secant':
            steps = brent_method(func, x, a, b, tol, max_iter)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'steps': steps})

# Menjalankan Aplikasi
if __name__ == '__main__':
    app.run(debug=True)
