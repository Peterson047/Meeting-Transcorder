Para o seu projeto em Streamlit, aqui está o conteúdo do `requirements.txt`, com as bibliotecas que você está usando ou que devem ser instaladas:

### Arquivo `requirements.txt`

```plaintext
streamlit
st_audiorec
requests
python-dotenv
google-generativeai
```

Se você estiver usando threads adicionais, pode ser que precise do `threading` na lista, mas geralmente ele faz parte do Python e não precisa ser instalado separadamente.

### Documentação para Instalação

Abaixo, veja um guia para configurar e instalar as dependências deste projeto.

---

### Documentação de Instalação

#### Pré-requisitos

- **Python 3.7 ou superior**: Certifique-se de que o Python está instalado em sua máquina. Você pode verificar sua versão com o comando:
  ```bash
  python --version
  ```

#### Passo 1: Clone ou Baixe o Projeto

Clone o repositório ou baixe o projeto em sua máquina local.

#### Passo 2: Crie um Ambiente Virtual (opcional, mas recomendado)

Crie um ambiente virtual para isolar as dependências do projeto:
```bash
python -m venv venv
```

Ative o ambiente virtual:
- No Windows:
  ```bash
  venv\Scripts\activate
  ```
- No macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

#### Passo 3: Instale as Dependências

No diretório raiz do projeto, instale as dependências listadas no `requirements.txt` com o seguinte comando:
```bash
pip install -r requirements.txt
```

#### Passo 4: Configurar as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API nele:

```plaintext
GROQ_API_KEY=Sua_Chave_GROQ
GEMINI_API_KEY=Sua_Chave_GEMINI
```

#### Passo 5: Execute o Projeto

Execute a aplicação com o comando:
```bash
streamlit run nome_do_arquivo.py
```

Substitua `nome_do_arquivo.py` pelo nome do arquivo Python principal, caso o arquivo tenha outro nome.

#### Passo 6: Acessar a Aplicação

Após iniciar a aplicação, acesse-a em um navegador pelo endereço indicado (geralmente `http://localhost:8501`).

---

Isso deve configurar e iniciar seu projeto. Caso surjam erros, verifique se o `.env` está configurado corretamente e se as dependências foram instaladas sem problemas.