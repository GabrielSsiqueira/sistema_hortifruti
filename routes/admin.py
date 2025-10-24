from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
import base64,os
from datetime import datetime
from models.model import Cesta, Item, Promocao
from extensions.database import db

UPLOAD_DIR = "static/img/cestas"
UPLOAD_ITEM_DIR = "static/img/itens"

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/hortifruti/admin')
def painel():
    return render_template('admin/painel.html')

# Rotas de Cestas    

@admin_blueprint.route('/hortifruti/admin/listar')
def listCesta():
    cestas = Cesta.query.all()
    return render_template('admin/listCestas.html', cestas=cestas)

@admin_blueprint.route('/hortifruti/admin/editar/<int:id>')
def editCesta(id):
    cesta = Cesta.query.get(id)
    return render_template('editCesta.html', cesta=cesta)

@admin_blueprint.route('/hortifruti/admin/update', methods=['PUT'])
def update_cesta(id):
    cesta = Cesta.query.get(id)

    if cesta is None:
        return jsonify({'error': 'Cesta não encontrada'}), 404

    data = request.get_json()
    
    cesta.nome = data.get('nome', cesta.nome)
    cesta.descricao = data.get('descricao', cesta.descricao)
    cesta.preco = data.get('preco', cesta.preco)

    db.session.commit()
    return jsonify({'message': 'Cesta atualizada com sucesso'}),200

@admin_blueprint.route('/admin/adicionar', methods=['GET'])
def addCestas():
    return render_template('admin/addCestas.html')

@admin_blueprint.route('/hortifruti/admin/add', methods=['POST'])
def create_cesta():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'dados não fornecidos'}), 400

    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    imagem = data.get('imagem')

    # criar o diretorio se não existir
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # remover o prefixo base64
    if ',' in imagem:
        imagem = imagem.split(',')[1]

    # decodificando e salvando
    imagem_bytes = base64.b64decode(imagem)
    nome_arquivo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    caminho_arquivo = os.path.join(UPLOAD_DIR, nome_arquivo)

    with open(caminho_arquivo, 'wb') as f:
        f.write(imagem_bytes)


    nova_cesta = Cesta(nome=nome,
                        descricao=descricao, 
                        preco=preco,
                        imagem=nome_arquivo
                    )
    db.session.add(nova_cesta)
    db.session.commit()

    return jsonify({"mensagem": "Cesta Adicionada com Sucesso!"}), 201

# Rotas de Itens

@admin_blueprint.route('/hortifruti/admin/listItens')
def listItens():
    itens = Item.query.all()
    return render_template('admin/listItens.html', itens=itens)

@admin_blueprint.route('/hortifruti/admin/addItens')
def addItens():
    cestas = Cesta.query.all()
    return render_template('admin/addItens.html', cestas=cestas)

@admin_blueprint.route('/hortifruti/admin/createItens', methods=['POST'])
def create_itens():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'dados não fornecidos'}), 400

    
    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    id_cesta = data.get('id_cesta')
    imagem = data.get('imagem')

    # criar o diretorio se não existir
    os.makedirs(UPLOAD_ITEM_DIR, exist_ok=True)

    # remover o prefixo base64
    if ',' in imagem:
        imagem = imagem.split(',')[1]

    # decodificando e salvando
    imagem_bytes = base64.b64decode(imagem)
    nome_arquivo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    caminho_arquivo = os.path.join(UPLOAD_ITEM_DIR, nome_arquivo)

    with open(caminho_arquivo, 'wb') as f:
        f.write(imagem_bytes)


    novo_item = Item(nome=nome,
                        descricao=descricao, 
                        preco=preco,
                        cesta_id=id_cesta,
                        imagem=nome_arquivo
                    )
    db.session.add(novo_item)
    db.session.commit()

    return jsonify({"mensagem": "Item adicionado com sucesso!"}), 201

@admin_blueprint.route('/hortifruti/admin/DeleteItem/<int:id>', methods=['POST'])
def delete_item(id):
    # 1. Busca o item
    item = Item.query.get(id) 

    if item is None: 
        flash('Item não encontrado.', 'error')
        # Confirme se 'admin.listItens' é o nome correto da função da rota de listagem
        return redirect(url_for('admin.listItens'))

    try:
        # CORREÇÃO 1: Você deve deletar a INSTÂNCIA 'item', não a CLASSE 'Item'
        db.session.delete(item) 
        
        # Confirma a exclusão no banco de dados
        db.session.commit()

        # CORREÇÃO 2: Acessar o nome corretamente (assumindo que seja 'nome' e não 'none' conforme o modelo)
        flash(f'O Item "{item.nome}" foi excluído com sucesso!', 'success')
    
    except Exception as e:
        # CORREÇÃO 3: O método correto é 'rollback' com dois 'l'
        db.session.rollback() 
        flash(f'Erro ao excluir o item: {str(e)}', 'error')

    return redirect(url_for('admin.listItens'))
# rotas Promoção
@admin_blueprint.route('/hortifruti/admin/listPromocao')
def listPromocao():
    promocaos = Promocao.query.all()
    return render_template('admin/listPromocao.html', promocaos=promocaos)

@admin_blueprint.route('/hortifruti/admin/addPromocao')
def addPromocao():
    itens = Item.query.all()
    return render_template('/admin/addPromocao.html', itens=itens)


@admin_blueprint.route('/hortifruti/admin/createPromocao', methods=['POST'])
def create_promocao():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'dados não fornecidos'}), 400

    item = data.get('item_id')
    desconto = data.get('desconto')
    data_inicio = data.get('data_inicio')
    data_fim = data.get('data_fim')

    nova_promocao = Promocao(
        item_id=item,
        desconto=desconto,
        data_inicio=data_inicio,
        data_fim=data_fim
    )
    db.session.add(nova_promocao)
    db.session.commit()

    return jsonify({"mensagem": "Promoção adicionada com sucesso!"}), 201

