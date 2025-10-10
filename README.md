# JusFacil - Sistema de Reconhecimento Facial

O **JusFacil** é um sistema desenvolvido em **Python** e **Django** que utiliza **reconhecimento facial** para auxiliar no **cumprimento de medidas cautelares** no Tribunal de Justiça da Paraíba.  

A aplicação permite o **cadastro e verificação facial de acautelados**, facilitando o controle de presença de pessoas que precisam comparecer periodicamente ao fórum.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.9.13**
- **Django**
- **DeepFace**
- **SQLite**
- **HTML5 / CSS3 / Bootstrap** 

---

## Instalação e Execução do Projeto

Siga os passos abaixo para rodar o projeto localmente:

### 1️ Clonar o repositório
```bash
git clone https://github.com/bvasconcelos710/reconhecimento-deep-face.git
```

### 2 Criar ambiente virtual
```bash
python -m venv venv
```
### 3 Ativar o ambiente virtual
```bash
# Ativar no Windows
venv\Scripts\activate
# Ativar no Linux/Mac
source venv/bin/activate
```

### 4 Instalar as dependências
```bash
pip install -r requirements.txt
```

### 5 Aplicar as migrações do banco de dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6 Criar um superusuario (opcional, para acessar o painel admin)
```bash
python manage.py createsuperuser
```

### 7 Executar o servidor
```bash
python manage.py runserver
```
