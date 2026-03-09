from pathlib import Path
from collections import defaultdict
from datetime import date
from io import StringIO
import csv

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from expense_app.authentication import auth
from expense_app.authentication.database import (
    get_expenses,
    get_categories,
    setup_expense_tables,
    setup_category_table,
    setup_databse,
    get_user_id,
    add_category,
    add_expense,
    get_expenses_with_ids,
    get_expense_by_id,
    update_expense,
    delete_expense,
    setup_budget_table,
    set_budget,
    get_budgets,
)

app = FastAPI(title="Expense Manager API")

app.add_middleware(SessionMiddleware, secret_key="change-me-secret-key")

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.on_event("startup")
def startup():
    setup_databse()
    setup_expense_tables()
    setup_category_table()
    setup_budget_table()


def _require_username(request: Request):
    return request.session.get("username")


@app.get("/", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None, "info": None},
    )


@app.post("/login")
async def handle_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    success, msg = auth.login(username, password)
    if success:
        request.session["username"] = username
        return RedirectResponse(url="/main", status_code=303)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": msg, "info": None},
        status_code=400,
    )


@app.post("/logout")
async def handle_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


@app.get("/signup", response_class=HTMLResponse)
async def show_signup(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "error": None},
    )


@app.post("/signup")
async def handle_signup(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    success, msg = auth.signup(username, password)
    if success:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": None,
                "info": "Account created successfully. Please log in.",
            },
        )
    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "error": msg},
        status_code=400,
    )


def _build_summaries(expenses):
    by_category = defaultdict(float)
    by_date = defaultdict(float)
    by_month = defaultdict(float)

    for _, exp_date, category, amount, _ in expenses:
        amt = float(amount)
        by_category[category] += amt
        by_date[exp_date] += amt

        if len(exp_date) >= 7:
            month = exp_date[:7]
            by_month[month] += amt

    return {
        "by_category": dict(sorted(by_category.items(), key=lambda x: x[0])),
        "by_date": dict(sorted(by_date.items(), key=lambda x: x[0])),
        "by_month": dict(sorted(by_month.items(), key=lambda x: x[0])),
    }


def _filter_expenses(expenses, filter_category, filter_from, filter_to):
    result = []
    for row in expenses:
        exp_id, exp_date, category, amount, desc = row
        if filter_category and category != filter_category:
            continue
        if filter_from and exp_date < filter_from:
            continue
        if filter_to and exp_date > filter_to:
            continue
        result.append(row)
    return result


@app.get("/main", response_class=HTMLResponse)
async def main_page(request: Request):
    username = _require_username(request)
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user_id = get_user_id(username)
    categories = get_categories(user_id)

    q = request.query_params
    filter_category = q.get("filter_category", "")
    filter_from = q.get("filter_from", "")
    filter_to = q.get("filter_to", "")

    all_expenses = get_expenses_with_ids(user_id)
    expenses = _filter_expenses(all_expenses, filter_category, filter_from, filter_to)
    summaries = _build_summaries(expenses)

    budget_rows = get_budgets(user_id)
    budgets = {cat: float(b) for cat, b in budget_rows}

    today = date.today().isoformat()
    current_month = today[:7]
    month_spent = defaultdict(float)
    for _, exp_date, category, amount, _ in all_expenses:
        if exp_date.startswith(current_month):
            month_spent[category] += float(amount)

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "username": username,
            "user_id": user_id,
            "categories": categories,
            "expenses": expenses,
            "summaries": summaries,
            "filter_category": filter_category,
            "filter_from": filter_from,
            "filter_to": filter_to,
            "budgets": budgets,
            "month_spent": dict(month_spent),
            "current_month": current_month,
        },
    )


@app.post("/categories")
async def create_category(request: Request, name: str = Form(...)):
    username = _require_username(request)
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user_id = get_user_id(username)
    cleaned = name.strip()
    if cleaned:
        add_category(user_id, cleaned)
    return RedirectResponse(url="/main", status_code=303)


@app.post("/expenses")
async def create_expense(
    request: Request,
    amount: str = Form(...),
    category: str = Form(...),
    description: str = Form(""),
    date_value: str = Form(""),
):
    username = _require_username(request)
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user_id = get_user_id(username)

    try:
        numeric_amount = float(amount)
    except ValueError:
        return RedirectResponse(url="/main?error=amount", status_code=303)

    if not date_value:
        date_value = date.today().isoformat()

    if category:
        add_expense(
            user_id,
            date_value,
            category,
            numeric_amount,
            description,
        )
    return RedirectResponse(url="/main", status_code=303)


@app.post("/budgets")
async def create_or_update_budget(
    request: Request,
    category: str = Form(...),
    monthly_budget: str = Form(...),
):
    username = _require_username(request)
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user_id = get_user_id(username)

    try:
        value = float(monthly_budget)
    except ValueError:
        return RedirectResponse(url="/main", status_code=303)

    if category and value >= 0:
        set_budget(user_id, category, value)

    return RedirectResponse(url="/main", status_code=303)


@app.get("/expenses/edit/{expense_id}", response_class=HTMLResponse)
async def edit_expense_page(request: Request, expense_id: int):
    username = _require_username(request)
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user_id = get_user_id(username)
    categories = get_categories(user_id)
    row = get_expense_by_id(user_id, expense_id)
    if not row:
        return RedirectResponse(url="/main", status_code=303)

    all_expenses = get_expenses_with_ids(user_id)
    summaries = _build_summaries(all_expenses)

    return templates.TemplateResponse(
        "edit_expense.html",
        {
            "request": request,
            "username": username,
            "user_id": user_id,
            "categories": categories,
            "expense": {
                "id": row[0],
                "date": row[1],
                "category": row[2],
                "amount": row[3],
                "description": row[4],
            },
            "summaries": summaries,
        },
    )


@app.post("/expenses/update/{expense_id}")
async def update_expense_action(
    request: Request,
    expense_id: int,
    amount: str = Form(...),
    category: str = Form(...),
    description: str = Form(""),
    date_value: str = Form(...),
):
    username = _require_username(request)
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user_id = get_user_id(username)

    try:
        numeric_amount = float(amount)
    except ValueError:
        return RedirectResponse(url=f"/expenses/edit/{expense_id}", status_code=303)

    update_expense(user_id, expense_id, date_value, category, numeric_amount, description)
    return RedirectResponse(url="/main", status_code=303)


@app.post("/expenses/delete/{expense_id}")
async def delete_expense_action(request: Request, expense_id: int):
    username = _require_username(request)
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user_id = get_user_id(username)
    delete_expense(user_id, expense_id)
    return RedirectResponse(url="/main", status_code=303)


@app.get("/api/expenses/{user_id}")
def read_expenses(user_id: int):
    return get_expenses(user_id)


@app.get("/api/categories/{user_id}")
def read_categories(user_id: int):
    return get_categories(user_id)


@app.get("/export")
def export_expenses(
    request: Request,
):
    username = _require_username(request)
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user_id = get_user_id(username)

    q = request.query_params
    filter_category = q.get("filter_category", "")
    filter_from = q.get("filter_from", "")
    filter_to = q.get("filter_to", "")

    all_expenses = get_expenses_with_ids(user_id)
    expenses = _filter_expenses(all_expenses, filter_category, filter_from, filter_to)

    def generate():
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["id", "date", "category", "amount", "description"])
        for exp_id, exp_date, category, amount, desc in expenses:
            writer.writerow([exp_id, exp_date, category, amount, desc])
        yield buffer.getvalue()

    filename = "expenses.csv"
    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )