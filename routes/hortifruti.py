from flask import Blueprint, render_template, request, redirect, url_for
from models.model import Cesta, Item, Pedido, PedidoItem, Promocao
from extensions.database import db
from datetime import datetime
from sqlalchemy import func, outerjoin

hortifruti_blueprint = Blueprint('hortifruti', __name__, url_prefix='/hortifruti')

@hortifruti_blueprint.route('/')
def index():
    # 1. Busca as cestas (mantido seu código original para a estrutura)
    cestas = Cesta.query.limit(3).all()
    cestas_formatadas = []

    # 2. Busca os Itens que estão em Promoção
    # Faz um JOIN de Item com Promocao, e filtra pela data atual
    # Nota: Assumindo que você tem acesso ao objeto db e às classes Promocao e Item
    itens_em_promocao_query = db.session.query(Item, Promocao).\
        join(Promocao, Item.id == Promocao.item_id).\
        filter(
            Promocao.data_inicio <= datetime.utcnow(),
            Promocao.data_fim <= datetime.utcnow()
        ).all()
    
    # Formata os itens em promoção em um dicionário para fácil acesso
    # Chave: item_id, Valor: {item_data, desconto}
    itens_promocao_map = {}
    for item, promocao in itens_em_promocao_query:
        preco_com_desconto = item.preco * (1 - promocao.desconto / 100)
        itens_promocao_map[item.id] = {
            "nome": item.nome,
            "descricao": item.descricao,
            "preco_original": item.preco,
            "preco_promocao": round(preco_com_desconto, 2), # Arredonda para 2 casas decimais
            "desconto": promocao.desconto,
            "cesta_id": item.cesta_id,
            "imagem": f"/static/img/itens/{item.imagem}" if item.imagem else "/static/img/cestas/sem_imagem.png"
        }

    # 3. Formata as cestas (código original)
    for c in cestas:
        cestas_formatadas.append({
            "id": c.id,
            "nome": c.nome,
            "descricao": c.descricao,
            "preco": c.preco,
            "imagem": f"/static/img/cestas/{c.imagem}" if c.imagem else "/static/img/cestas/sem_imagem.png"
        })

    # 4. Busca os itens mais relevantes em promoção
    # Vamos agrupar os itens em promoção pela cesta à qual pertencem.
    itens_promocao_por_cesta = {}
    for item_data in itens_promocao_map.values():
        cesta_id = item_data['cesta_id']
        if cesta_id not in itens_promocao_por_cesta:
            itens_promocao_por_cesta[cesta_id] = []
        itens_promocao_por_cesta[cesta_id].append(item_data)
        
    # 5. Prepara os dados finais para o template
    
    # Exemplo 1: Enviar todos os itens em promoção para o template (mais simples)
    itens_em_promocao_lista = list(itens_promocao_map.values())

    # Exemplo 2: Se você quiser enriquecer 'cestas_formatadas' com itens em promoção:
    # for cesta in cestas_formatadas:
    #     cesta['itens_em_promocao'] = itens_promocao_por_cesta.get(cesta['id'], [])

    return render_template(
        'index.html', 
        cestas=cestas_formatadas, 
        itens_em_promocao=itens_em_promocao_lista # Nova variável para o template
    )

@hortifruti_blueprint.route('/itens/<int:id>', methods=['GET'])
def itens(id):
    itens = Item.query.filter_by(id_cesta=id).all()
    return render_template('itens.html')
