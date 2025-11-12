"""Flask web application for managing warehouses."""
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# Dictionary to store warehouses by name
warehouses = {}


@app.route('/')
def index():
    """Display list of all warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            capacity = float(request.form.get('capacity', 0))
        except ValueError:
            flash('Capacity must be a valid number', 'error')
            return redirect(url_for('create_warehouse'))

        if not name:
            flash('Warehouse name is required', 'error')
            return redirect(url_for('create_warehouse'))

        if name in warehouses:
            flash(f'Warehouse "{name}" already exists', 'error')
            return redirect(url_for('create_warehouse'))

        if capacity <= 0:
            flash('Capacity must be greater than 0', 'error')
            return redirect(url_for('create_warehouse'))

        warehouses[name] = Varasto(capacity)
        flash(f'Warehouse "{name}" created successfully', 'success')
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/manage/<name>', methods=['GET', 'POST'])
def manage_warehouse(name):
    """Manage a specific warehouse (add/remove content)."""
    if name not in warehouses:
        flash(f'Warehouse "{name}" not found', 'error')
        return redirect(url_for('index'))

    warehouse = warehouses[name]

    if request.method == 'POST':
        action = request.form.get('action')
        try:
            amount = float(request.form.get('amount', 0))
        except ValueError:
            flash('Amount must be a valid number', 'error')
            return redirect(url_for('manage_warehouse', name=name))

        if action == 'add':
            warehouse.lisaa_varastoon(amount)
            flash(f'Added {amount} units to warehouse "{name}"', 'success')
        elif action == 'remove':
            removed = warehouse.ota_varastosta(amount)
            flash(f'Removed {removed} units from warehouse "{name}"', 'success')

        return redirect(url_for('manage_warehouse', name=name))

    return render_template('manage.html', name=name, warehouse=warehouse)


@app.route('/delete/<name>', methods=['POST'])
def delete_warehouse(name):
    """Delete a warehouse."""
    if name in warehouses:
        del warehouses[name]
        flash(f'Warehouse "{name}" deleted successfully', 'success')
    else:
        flash(f'Warehouse "{name}" not found', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
