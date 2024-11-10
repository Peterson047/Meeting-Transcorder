### Demo: https://transcorder.streamlit.app/

### Documentação de Instalação
![Texto Alternativo](/junk/capture.png)

**Descrição do Projeto:**

Este projeto é uma aplicação web desenvolvida com **Streamlit** para gravação de áudio, transcrição e geração de relatórios automáticos. Ele foi projetado para ser uma ferramenta útil para quem deseja transcrever áudios de reuniões, palestras ou outras atividades e gerar resumos ou relatórios detalhados com base no conteúdo transcrito. A aplicação integra gravação de áudio ao vivo e a possibilidade de envio de arquivos de áudio previamente gravados, com uma interface simples e interativa.

### Funcionalidades Principais:
1. **Gravação de Áudio**:
   - Utiliza o componente `st_audiorec` do Streamlit para capturar o áudio diretamente no navegador.
   - O áudio gravado é automaticamente enviado para transcrição após a gravação ser concluída.

2. **Envio de Áudio Pré-gravado**:
   - Caso o usuário não queira gravar o áudio, ele pode enviar um arquivo de áudio já gravado diretamente na interface.

3. **Transcrição de Áudio**:
   - O áudio gravado ou enviado é transcrito utilizando a API da **Groq**, que converte o áudio para texto.
   - O texto transcrito é mostrado para o usuário, permitindo que ele visualize a transcrição.

4. **Geração de Relatório**:
   - A transcrição gerada é processada para criar um relatório utilizando a API da **Groq**.
   - O relatório pode ser visualizado diretamente na interface e também pode ser baixado em formato de arquivo de texto.

5. **Interface de Usuário**:
   - A interface foi cuidadosamente desenhada para ser clara e fácil de usar, com dois containers: um para a gravação e transcrição (à esquerda) e outro para a exibição do relatório gerado (à direita).
   - Os usuários podem baixar tanto o áudio gravado quanto o relatório gerado.

### Tecnologias Utilizadas:
- **Streamlit**: Framework utilizado para criar a interface interativa.
- **st_audiorec**: Componente para gravação de áudio em Streamlit.
- **API da Groq**: Utilizada para transcrição de áudio e geração de relatórios.
- **Requests**: Biblioteca para fazer requisições HTTP para a API da Groq.
- **Python-dotenv**: Para carregar variáveis de ambiente a partir de um arquivo `.env`.

### Objetivo do Projeto:
O objetivo principal deste projeto é proporcionar uma ferramenta rápida e prática para transformar gravações de áudio em textos transcritos e relatórios de forma automatizada. Ele é ideal para ambientes corporativos, acadêmicos ou pessoais, onde a eficiência e a precisão na geração de relatórios a partir de áudios são importantes.

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
```

#### Passo 5: Execute o Projeto

Execute a aplicação com o comando:
```bash
streamlit app.py
```


#### Passo 6: Acessar a Aplicação

Após iniciar a aplicação, acesse-a em um navegador pelo endereço indicado (geralmente `http://localhost:8501`).

---

Isso deve configurar e iniciar seu projeto. Caso surjam erros, verifique se o `.env` está configurado corretamente e se as dependências foram instaladas sem problemas.
