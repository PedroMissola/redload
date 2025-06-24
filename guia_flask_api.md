# Guia Completo e Simples de Como Funciona o Flask e Como Criar APIs com Ele

## O que é o Flask?

O Flask é um microframework escrito em Python, muito usado para criar sites, aplicativos web e principalmente APIs. Ele é chamado de "micro" porque é simples e não vem com muitas coisas prontas, mas permite que você adicione só o que realmente precisa. Isso dá liberdade e controle ao programador. É ideal para quem está começando no mundo da programação web, mas também pode ser usado em projetos maiores e mais complexos.

Com o Flask, você consegue montar uma aplicação que responde a acessos pela internet, usando URLs que você define. Ele serve tanto para exibir páginas normais de um site (como HTML) quanto para criar sistemas de troca de dados (como APIs REST), que é o foco principal deste guia.

## O que o Flask oferece

- Facilidade de uso e aprendizado rápido
- Criação de URLs dinâmicas com variáveis
- Boa integração com bancos de dados
- Suporte ao envio e recebimento de dados no formato JSON
- Possibilidade de usar diferentes métodos HTTP (GET, POST, PUT, DELETE)
- Compatível com bibliotecas como Flask-Login, Flask-WTF, Flask-JWT, entre outras
- Comunidade ativa e boa documentação

---

## 1. Exemplo Básico de um Projeto Flask

Vamos começar com um exemplo simples de como criar um site básico usando Flask:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo ao Flask!"

if __name__ == '__main__':
    app.run(debug=True)
```

**Explicando cada parte:**

- `Flask(__name__)`: cria o aplicativo Flask.
- `@app.route('/')`: define o que vai acontecer quando alguém acessar a URL principal do site.
- `def home()`: função que devolve o texto "Bem-vindo ao Flask!" quando a página for acessada.
- `debug=True`: ativa o modo de desenvolvimento, que mostra erros e reinicia o servidor automaticamente quando você faz alterações no código.

---

## 2. Como Criar, Atualizar e Excluir Endpoints de uma API REST

### O que é um endpoint?

Um endpoint é um endereço específico de uma API, geralmente representado por uma URL, que serve para realizar ações sobre os dados. Cada endpoint responde a um tipo de requisição HTTP. Veja os principais:

- `GET`: usado para buscar dados
- `POST`: usado para adicionar novos dados
- `PUT`: usado para atualizar dados existentes
- `DELETE`: usado para remover dados

Agora vamos montar uma API simples que faz operações em uma lista de usuários. Essa estrutura é conhecida como CRUD (Create, Read, Update, Delete).

### Exemplo prático de CRUD completo:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = [
    {"id": 1, "nome": "Pedro"},
    {"id": 2, "nome": "Joana"}
]

# Listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios)

# Ver um único usuário pelo ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    for usuario in usuarios:
        if usuario['id'] == id:
            return jsonify(usuario)
    return jsonify({"erro": "Usuário não encontrado"}), 404

# Criar um novo usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    novo_usuario = {
        "id": usuarios[-1]['id'] + 1 if usuarios else 1,
        "nome": dados['nome']
    }
    usuarios.append(novo_usuario)
    return jsonify(novo_usuario), 201

# Atualizar um usuário existente
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.get_json()
    for usuario in usuarios:
        if usuario['id'] == id:
            usuario['nome'] = dados['nome']
            return jsonify(usuario)
    return jsonify({"erro": "Usuário não encontrado"}), 404

# Deletar um usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    for i, usuario in enumerate(usuarios):
        if usuario['id'] == id:
            del usuarios[i]
            return jsonify({"mensagem": "Usuário excluído com sucesso"})
    return jsonify({"erro": "Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

Com esse código, você tem uma mini API funcional. Pode testar usando o Postman, Insomnia ou com `curl` no terminal.

---

## 3. Outros Usos do Flask

### a) Integração com Páginas HTML

Com o Flask, você pode mostrar páginas HTML completas para o usuário, usando o mecanismo de template Jinja2. Isso permite colocar dados dinâmicos na página.

```python
from flask import render_template

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', usuarios=usuarios)
```

A função `render_template()` busca um arquivo HTML na pasta "templates" e permite usar os dados da aplicação dentro desse arquivo usando {{ variáveis }}.

### b) Usar com Banco de Dados (SQLAlchemy)

Você pode usar SQLAlchemy para se conectar com bancos de dados como SQLite, MySQL, PostgreSQL etc.

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
```

### c) Autenticação e Segurança

Você pode proteger rotas com login e autenticação. Usando extensões como Flask-Login (para autenticação com sessão) ou Flask-JWT (para autenticação com token), você controla quem acessa o quê.

---

## 4. Boas Práticas para Trabalhar com Flask

- **Organização**: Separe os arquivos em pastas como `routes`, `models`, `controllers`, `templates`.
- **Reutilização**: Não escreva o mesmo código em vários lugares; crie funções para isso.
- **Validação de Dados**: Sempre confira se os dados recebidos de formulários ou requisições estão corretos.
- **Blueprints**: Use essa função do Flask para dividir sua aplicação em módulos.
- **Ambiente Seguro**: Nunca coloque senhas e informações confidenciais no código diretamente. Use arquivos `.env` e bibliotecas como `python-dotenv`.
- **Mensagens de Erro**: Deixe claro para o usuário (ou cliente da API) o que está errado quando der erro.
- **Documentação**: Documente sua API com ferramentas como Swagger ou Postman.

---

## 5. Como Integrar uma API Flask com JavaScript no Frontend

Depois de criar sua API com Flask, você pode usá-la em uma aplicação frontend (como um site feito com HTML, CSS e JavaScript). A comunicação entre o frontend e a API geralmente acontece por meio de requisições HTTP, usando a função `fetch()` do JavaScript.

### Exemplo: Buscando dados de uma API Flask com JavaScript

Imagine que você tem a rota `/usuarios` criada no Flask, e ela retorna uma lista de usuários. Para acessar esses dados no frontend, você pode fazer:

```
<!DOCTYPE html>
<html>
<head>
    <title>Lista de Usuários</title>
</head>
<body>
    <h1>Usuários</h1>
    <ul id="lista-usuarios"></ul>

    <script>
        fetch('http://localhost:5000/usuarios')
            .then(response => response.json())
            .then(data => {
                const lista = document.getElementById('lista-usuarios');
                data.forEach(usuario => {
                    const item = document.createElement('li');
                    item.textContent = usuario.nome;
                    lista.appendChild(item);
                });
            })
            .catch(error => console.error('Erro:', error));
    </script>
</body>
</html>

```

Esse código faz uma requisição para a API Flask, pega os dados e os exibe na tela.

> ⚠️ Atenção: Para que funcione corretamente, o servidor Flask deve estar rodando e o navegador deve aceitar requisições entre domínios (CORS). Veja o próximo tópico para resolver isso.

---

## 6. Habilitando o CORS no Flask para Permitir Requisições do Frontend

O navegador, por padrão, bloqueia requisições de domínios diferentes por motivos de segurança. Para que o JavaScript do frontend consiga se comunicar com a API Flask, é necessário ativar o CORS (Cross-Origin Resource Sharing).

Você pode fazer isso facilmente com a biblioteca `flask-cors`.

### Passo a passo:

1. Instale a biblioteca:

```
pip install flask-cors

```

2. Importe e use no seu código Flask:

```
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

```

Se quiser permitir só um domínio específico (como seu site em produção), você pode fazer assim:

```
CORS(app, origins=["https://meusite.com"])

```

Com isso, sua API estará liberada para ser usada no navegador por aplicações JavaScript, inclusive em frameworks como React, Vue ou Angular.

---

## 7. Como Configurar um Banco de Dados SQLite no Flask

O Flask permite que você use bancos de dados como o SQLite de forma bem simples. O SQLite é um banco de dados leve, que armazena tudo em um único arquivo `.db`, ideal para testes e projetos pequenos.

### Passo 1: Instale o SQLAlchemy

O Flask não vem com suporte a banco de dados por padrão, mas podemos adicionar isso com a extensão `Flask-SQLAlchemy`:

```
pip install flask-sqlalchemy

```

### Passo 2: Configurando o Flask para usar o SQLite

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'  # Cria ou conecta com o arquivo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Apenas para remover um aviso

db = SQLAlchemy(app)

```

### Passo 3: Criando um modelo (tabela)

```
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

```

### Passo 4: Criando o banco de dados

Você precisa criar o arquivo `.db` e as tabelas. Isso pode ser feito com:

```
with app.app_context():
    db.create_all()

```

Esse comando cria o banco com as tabelas definidas pelos modelos Python (no caso, a tabela `Usuario`).

---

## 8. Como Usar o Banco de Dados SQLite na API Flask

Agora que temos o banco de dados configurado, podemos fazer com que a API use ele ao invés de uma lista em memória.

### Criando um usuário (POST)

```
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    novo_usuario = Usuario(nome=dados['nome'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"id": novo_usuario.id, "nome": novo_usuario.nome}), 201

```

### Listando usuários (GET)

```
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    lista = [{"id": u.id, "nome": u.nome} for u in usuarios]
    return jsonify(lista)

```

### Atualizando um usuário (PUT)

```
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.get_json()
    usuario = Usuario.query.get_or_404(id)
    usuario.nome = dados['nome']
    db.session.commit()
    return jsonify({"id": usuario.id, "nome": usuario.nome})

```

### Deletando um usuário (DELETE)

```
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário removido com sucesso"})

```

Com isso, sua API Flask agora está conectada a um banco de dados de verdade, com persistência de dados entre execuções. Você pode visualizar o conteúdo do banco com ferramentas como DB Browser for SQLite ou extensões do VS Code.

---

## 9. Tipos de Dados Suportados pelo SQLite

O SQLite é um banco de dados leve, mas suporta os principais tipos de dados que você vai precisar na maioria das aplicações. Quando usamos SQLAlchemy com Flask, esses tipos são representados por classes específicas. Aqui estão os principais:

| Tipo SQLite Tipo SQLAlchemy Descrição |                                     |                                        |
| ------------------------------------- | ----------------------------------- | -------------------------------------- |
| INTEGER                               | `db.Integer`                        | Números inteiros                       |
| TEXT                                  | `db.String`                         | Texto (é necessário definir o tamanho) |
| REAL                                  | `db.Float`                          | Números decimais                       |
| NUMERIC                               | `db.Numeric`                        | Números com precisão definida          |
| BLOB                                  | `db.LargeBinary`                    | Dados binários (imagens, arquivos etc) |
| BOOLEAN (simulado)                    | `db.Boolean`                        | Verdadeiro ou falso                    |
| DATE/TIME                             | `db.Date`, `db.Time`, `db.DateTime` | Datas e horários                       |

### Exemplo:

```
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    em_estoque = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

```

Esse modelo `Produto` mostra como usar vários tipos diferentes em um banco SQLite com Flask.

---

## 10. Criando Relacionamentos e Manipulando Tabelas com Flask e SQLAlchemy

Além de tabelas simples, você também pode criar relacionamentos entre elas — como um usuário que tem vários pedidos, ou uma categoria com vários produtos. Isso é feito com chaves estrangeiras e relacionamentos do SQLAlchemy.

### Exemplo: Relacionamento 1 para muitos (Usuário -> Postagens)

```
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    postagens = db.relationship('Postagem', backref='autor', lazy=True)

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    conteudo = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

```

Neste exemplo, cada `Usuario` pode ter várias `Postagem`. E cada `Postagem` está ligada a um `Usuario` pelo campo `usuario_id`, que é uma chave estrangeira.

### Criando e acessando os dados com relacionamento

```
# Criar novo usuário e postagem
usuario = Usuario(nome="Pedro")
post = Postagem(titulo="Olá Mundo", conteudo="Meu primeiro post!", autor=usuario)
db.session.add(usuario)
db.session.add(post)
db.session.commit()

# Listar postagens de um usuário
usuario = Usuario.query.first()
for p in usuario.postagens:
    print(p.titulo)

```

### Alterando tabelas e campos existentes

Se você quiser adicionar colunas novas ou modificar tabelas depois que o banco já foi criado, é recomendado usar migrações com a biblioteca `Flask-Migrate`:

```
pip install flask-migrate

```

```
from flask_migrate import Migrate
migrate = Migrate(app, db)

```

Depois use comandos como:

```
flask db init       # cria a estrutura
flask db migrate -m "adicionando campo"
flask db upgrade    # aplica a mudança no banco

```

Assim, você evita perder dados ou precisar recriar o banco sempre que quiser fazer alterações.

---

## Conclusão

O Flask é uma ferramenta excelente para quem quer criar projetos web com Python. Mesmo sendo simples, ele é poderoso e pode ser usado tanto por iniciantes quanto por desenvolvedores experientes. Você consegue criar desde um site pessoal até sistemas mais avançados com rotas protegidas, conexão com banco de dados e APIs REST completas.

Se você seguir boas práticas e estudar os recursos disponíveis, vai conseguir fazer ótimos projetos com ele. Flask é uma ótima porta de entrada para o mundo do desenvolvimento web.

