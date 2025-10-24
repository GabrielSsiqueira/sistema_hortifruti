from extensions.database import db 
# Modelo Cesta

class Cesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=True)
    itens = db.Relationship('Item', backref='cesta', lazy=True)

    def __repr__(self):
        return f'Cesta({self.nome})'
    
# Modelo Item

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=True)
    cesta_id = db.Column(db.Integer, db.ForeignKey('cesta.id'), nullable=False)

    def __repr__(self):
        return f'Item({self.nome})'

# modelo Promoção

class Promocao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref='promocao', lazy=True)
    desconto = db.Column(db.Float, nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Promocao({self.desconto})'


# Modelo Pedido

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(100), nullable=False)
    cliente_telefone = db.Column(db.String(20), nullable=False)
    itens = db.relationship('PedidoItem', backref='pedido', lazy=True)

    def __repr__(self):
        return f'Pedido({self.id})'

# Modelo Pedido Item

class PedidoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    item = db.relationship('Item', backref='pedido_itens', lazy=True)

    def __repr__(self):
        return f'PedidoItem({self.id})'


