def get_cost_per_sqft(quality):
    q = quality.lower()
    if q == "budget":
        return 1500
    if q == "moderate":
        return 2000
    return 2500

def estimate_cost(area, bhk, quality):
    rate = get_cost_per_sqft(quality)
    
    # small factor: more BHK → slightly higher cost
    bhk_factor = 1 + (bhk - 1) * 0.05
    base_cost = area * rate * bhk_factor

    breakdown = {
        "Cement & Bricks": 0.25,
        "Steel": 0.20,
        "Labor": 0.25,
        "Flooring": 0.05,
        "Plumbing & Electrical": 0.10,
        "Contractor": 0.08,
        "Miscellaneous": 0.07
    }

    cost_split = {k: round(base_cost * v, 2) for k, v in breakdown.items()}
    return round(base_cost, 2), cost_split

def optimize_cost(cost_split):
    eco_subs = {
        "Cement & Bricks": ("Fly-Ash Bricks", 0.15),
        "Steel": ("Recycled Steel", 0.12),
        "Flooring": ("Polished Concrete", 0.10),
        "Plumbing & Electrical": ("Water-efficient fittings", 0.05)
    }
    optimized = {}
    savings_total = 0
    for item, cost in cost_split.items():
        if item in eco_subs:
            alt, reduction = eco_subs[item]
            new_cost = round(cost * (1 - reduction), 2)
            optimized[item] = (alt, new_cost)
            savings_total += cost - new_cost
        else:
            optimized[item] = ("Same", cost)
    return optimized, round(savings_total, 2)
