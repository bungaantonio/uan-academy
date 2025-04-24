# Passos para Rodar o Projeto Django

Siga os passos abaixo para configurar e rodar o projeto Django:

## Pré-requisitos
1. Certifique-se de ter o Python instalado (versão 3.8 ou superior).
2. Instale o `pip` e o `virtualenv` se ainda não estiverem instalados.

## Passos
1. **Clone o repositório**:
    ```bash
    git clone https://github.com/bungaantonio/uan-academy.git
    cd uan-academy
    ```

2. **Crie e ative um ambiente virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate # No Linux:
    venv\Scripts\activate # No Windows:
    ```
    2.1. **Configure a política de execução do PowerShell (apenas no Windows)**:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
3. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o banco de dados**:
    - Edite o arquivo `settings.py` para configurar o banco de dados.
    - Aplique as migrações:
      ```bash
      python manage.py migrate
      ```

5. **Inicie o servidor de desenvolvimento**:
    ```bash
    python manage.py runserver
    ```

6. **Acesse o projeto**:
    Abra o navegador e vá para `http://127.0.0.1:8000`.

## Comandos Úteis
- Criar um superusuário:
  ```bash
  python manage.py createsuperuser
  ```
- Rodar testes:
  ```bash
  python manage.py test
  ```

Pronto! O projeto está configurado e rodando.