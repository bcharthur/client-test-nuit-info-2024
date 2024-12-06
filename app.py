from flask import Flask, render_template, request, redirect, url_for, flash

import requests

API_BASE_URL = "http://localhost:5000/api"  # URL de l'API du serveur

app = Flask(__name__)
app.secret_key = "secret_key_for_client"

@app.route('/')
def home():
    return redirect(url_for('list_items'))

@app.route('/items')
def list_items():
    r = requests.get(f"{API_BASE_URL}/items")
    if r.status_code == 200:
        data = r.json()
        items = data.get("items", [])
        return render_template('items/index.html', items=items)
    else:
        flash("Erreur de récupération des items", "danger")
        # Même en cas d'erreur, on affiche le template index.html avec une liste vide
        return render_template('items/index.html', items=[])


@app.route('/items/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        label = request.form.get('label')
        # Envoi de la requête POST à l'API
        r = requests.post(f"{API_BASE_URL}/items", json={"label": label})
        if r.status_code == 201:
            flash("Item ajouté avec succès", "success")
            return redirect(url_for('list_items'))
        else:
            flash("Erreur lors de l'ajout de l'item", "danger")
            return redirect(url_for('list_items'))
    return render_template('items/add.html')

@app.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if request.method == 'POST':
        label = request.form.get('label')
        r = requests.put(f"{API_BASE_URL}/items/{item_id}", json={"label": label})
        if r.status_code == 200:
            flash("Item modifié avec succès", "success")
            return redirect(url_for('list_items'))
        else:
            flash("Erreur lors de la modification de l'item", "danger")
            return redirect(url_for('list_items'))
    else:
        # On va chercher l'item auprès de l'API pour préremplir le formulaire
        r = requests.get(f"{API_BASE_URL}/items")
        if r.status_code == 200:
            data = r.json()
            items = data.get("items", [])
            # Récupérer l'item avec l'id
            item_to_edit = next((i for i in items if i['id'] == item_id), None)
            if not item_to_edit:
                flash("Item introuvable", "danger")
                return redirect(url_for('list_items'))
            return render_template('items/edit.html', item=item_to_edit)
        else:
            flash("Erreur de récupération des items", "danger")
            return redirect(url_for('list_items'))

@app.route('/items/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    r = requests.delete(f"{API_BASE_URL}/items/{item_id}")
    if r.status_code == 200:
        flash("Item supprimé avec succès", "success")
    else:
        flash("Erreur lors de la suppression de l'item", "danger")
    return redirect(url_for('list_items'))


if __name__ == '__main__':
    # Démarre le serveur Flask du client sur le port 5001
    app.run(port=5001, debug=True)

