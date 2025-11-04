from flask import Flask, render_template, request
from cost import estimate_cost, optimize_cost  # your cost logic file

app = Flask(__name__)

# 🏠 Home page (first page)
@app.route('/')
def home():
    return render_template('home.html')


# 🧮 Estimator form page
@app.route('/estimate_form')
def estimate_form():
    return render_template('index.html')


# 📊 Estimate calculation
@app.route('/estimate', methods=['POST'])
def estimate():
    try:
        area = float(request.form['area'])
        bhk = int(request.form['bhk'])
        quality = request.form['quality']

        total_cost, cost_split = estimate_cost(area, bhk, quality)
        return render_template(
            'result.html',
            total=total_cost,
            cost_split=cost_split,
            area=area,
            bhk=bhk,
            quality=quality
        )
    except Exception as e:
        return render_template('index.html', error=str(e))


# 🌱 Cost Optimization
@app.route('/optimize', methods=['POST'])
def optimize():
    cost_data = request.form.to_dict(flat=False)
    cost_split = {k: float(v[0]) for k, v in cost_data.items() if k != 'total'}
    optimized, savings = optimize_cost(cost_split)
    optimized_total = sum(val[1] for val in optimized.values())

    return render_template(
        'optimized.html',
        optimized=optimized,
        original=cost_split,
        savings=savings,
        optimized_total=round(optimized_total, 2)
    )


if __name__ == '__main__':
    app.run(debug=True)
