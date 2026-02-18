def calculate_federal_tax(income):
    brackets = [
        (11000, 0.10),
        (44725, 0.12),
        (95375, 0.22),
        (182100, 0.24),
    ]

    tax = 0
    previous_limit = 0

    for limit, rate in brackets:
        if income > limit:
            tax += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            tax += (income - previous_limit) * rate
            return tax

    tax += (income - previous_limit) * 0.32
    return tax


def calculate_net_income(
    salary,
    bonus,
    healthcare_cost,
    retirement_percent
):
    total_income = salary + bonus

    retirement_contribution = total_income * (retirement_percent / 100)
    taxable_income = total_income - retirement_contribution

    federal_tax = calculate_federal_tax(taxable_income)

    net_income = (
        total_income
        - federal_tax
        - healthcare_cost
        - retirement_contribution
    )

    return {
        "total_income": total_income,
        "federal_tax": federal_tax,
        "retirement_contribution": retirement_contribution,
        "net_income": net_income
    }

def calculate_self_employment_tax(income):
    return income * 0.153


def compare_w2_vs_contractor(
    w2_salary,
    contractor_rate,
    hours_per_year,
    healthcare_cost,
    retirement_percent,
    employer_match_percent
):

    contractor_income = contractor_rate * hours_per_year
    contractor_tax = calculate_self_employment_tax(contractor_income)

    contractor_net = contractor_income - contractor_tax - healthcare_cost

    w2_total = w2_salary
    retirement_contribution = w2_total * (retirement_percent / 100)
    employer_match = w2_total * (employer_match_percent / 100)

    w2_tax = calculate_self_employment_tax(w2_total) * 0.6  # rough estimate

    w2_net = (
        w2_total
        - w2_tax
        - healthcare_cost
        - retirement_contribution
        + employer_match
    )

    return {
        "contractor_net": contractor_net,
        "w2_net": w2_net
    }
STATE_TAX_RATES = {
    "NY": 0.06,
    "CA": 0.08,
    "TX": 0.00,
    "FL": 0.00
}


def calculate_federal_tax(income):
    brackets = [
        (11000, 0.10),
        (44725, 0.12),
        (95375, 0.22),
        (182100, 0.24),
    ]

    tax = 0
    prev = 0

    for limit, rate in brackets:
        if income > limit:
            tax += (limit - prev) * rate
            prev = limit
        else:
            tax += (income - prev) * rate
            return tax

    tax += (income - prev) * 0.32
    return tax


def calculate_state_tax(income, state):
    rate = STATE_TAX_RATES.get(state, 0.05)
    return income * rate
def calculate_pto_value(salary, pto_days):
    daily_rate = salary / 260
    return daily_rate * pto_days
def five_year_projection(annual_net, growth_rate=0.03):
    projections = []
    current = annual_net

    for year in range(1, 6):
        projections.append(round(current, 2))
        current *= (1 + growth_rate)

    return projections
def advanced_compare(
    w2_salary,
    contractor_rate,
    hours_per_year,
    state,
    healthcare_cost,
    retirement_percent,
    employer_match_percent,
    pto_days
):

    contractor_income = contractor_rate * hours_per_year
    contractor_federal = calculate_federal_tax(contractor_income)
    contractor_state = calculate_state_tax(contractor_income, state)
    contractor_self_tax = contractor_income * 0.153

    contractor_net = (
        contractor_income
        - contractor_federal
        - contractor_state
        - contractor_self_tax
        - healthcare_cost
    )

    w2_federal = calculate_federal_tax(w2_salary)
    w2_state = calculate_state_tax(w2_salary, state)

    retirement = w2_salary * (retirement_percent / 100)
    employer_match = w2_salary * (employer_match_percent / 100)
    pto_value = calculate_pto_value(w2_salary, pto_days)

    w2_net = (
        w2_salary
        - w2_federal
        - w2_state
        - healthcare_cost
        - retirement
        + employer_match
        + pto_value
    )

    return {
        "contractor_net": round(contractor_net, 2),
        "w2_net": round(w2_net, 2),
        "contractor_projection": five_year_projection(contractor_net),
        "w2_projection": five_year_projection(w2_net)
    }
