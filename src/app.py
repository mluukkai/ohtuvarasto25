"""Flask web application for managing multiple warehouses (Varasto)."""
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
app.secret_key = 'varasto-secret-key-2025'

# In-memory storage for warehouses
warehouses = {}
warehouse_counter = 0


@app.route('/')
def index():
    """Display all warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['POST'])
def create_warehouse():  # pylint: disable=too-many-statements
    """Create a new warehouse."""
    global warehouse_counter  # pylint: disable=global-statement

    try:
        name = request.form.get('name', '').strip()
        tilavuus = float(request.form.get('tilavuus', 0))
        alku_saldo = float(request.form.get('alku_saldo', 0))

        if not name:
            flash('Nimi on pakollinen!', 'error')
            return redirect(url_for('index'))

        if tilavuus <= 0:
            flash('Tilavuuden pitää olla suurempi kuin 0!', 'error')
            return redirect(url_for('index'))

        warehouse = Varasto(tilavuus, alku_saldo)
        warehouse_counter += 1
        warehouse_id = warehouse_counter
        warehouses[warehouse_id] = {'name': name, 'varasto': warehouse}

        flash(f'Varasto "{name}" luotu onnistuneesti!', 'success')
    except (ValueError, TypeError):
        flash('Virheelliset arvot!', 'error')

    return redirect(url_for('index'))


@app.route('/add/<int:warehouse_id>', methods=['POST'])
def add_to_warehouse(warehouse_id):
    """Add items to a warehouse."""
    try:
        maara = float(request.form.get('maara', 0))

        if warehouse_id not in warehouses:
            flash('Varastoa ei löydy!', 'error')
            return redirect(url_for('index'))

        warehouses[warehouse_id]['varasto'].lisaa_varastoon(maara)
        flash(f'Lisätty {maara} yksikköä!', 'success')
    except (ValueError, TypeError):
        flash('Virheellinen määrä!', 'error')

    return redirect(url_for('index'))


@app.route('/take/<int:warehouse_id>', methods=['POST'])
def take_from_warehouse(warehouse_id):
    """Take items from a warehouse."""
    try:
        maara = float(request.form.get('maara', 0))

        if warehouse_id not in warehouses:
            flash('Varastoa ei löydy!', 'error')
            return redirect(url_for('index'))

        saatu = warehouses[warehouse_id]['varasto'].ota_varastosta(maara)
        flash(f'Otettu {saatu} yksikköä!', 'success')
    except (ValueError, TypeError):
        flash('Virheellinen määrä!', 'error')

    return redirect(url_for('index'))


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    if warehouse_id in warehouses:
        name = warehouses[warehouse_id]['name']
        del warehouses[warehouse_id]
        flash(f'Varasto "{name}" poistettu!', 'success')
    else:
        flash('Varastoa ei löydy!', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Debug mode should only be enabled during development
    # In production, use a proper WSGI server like gunicorn
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
