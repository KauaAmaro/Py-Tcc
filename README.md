# Leitor de Códigos de Barras

Aplicativo desktop para leitura de códigos de barras via câmera IP com interface gráfica e banco de dados local.

## Funcionalidades

- Leitura em tempo real de códigos de barras via câmera IP
- Cadastro de produtos com códigos de barras
- Registro automático de leituras no banco de dados
- Visualização de estatísticas com gráficos
- Interface gráfica intuitiva

## Instalação

### Opção 1: Instalação Automática
```bash
python3 install.py
```

### Opção 2: Instalação Manual
1. Instale as dependências:
```bash
pip3 install -r requirements.txt
```

2. No Ubuntu/Debian, instale tkinter:
```bash
sudo apt-get install python3-tk
```

## Execução

### Opção 1: Script de execução
```bash
./run.sh
```

### Opção 2: Execução direta
```bash
python3 main.py
```

## Geração de Executável

Para gerar um executável autônomo:

```bash
python build.py
```

O executável será criado na pasta `dist/`.

## Configuração da Câmera IP

Por padrão, o aplicativo está configurado para a URL: `http://192.168.1.244:8080/video`

Para alterar, modifique a URL no arquivo `barcode_reader.py`.

## Estrutura do Banco de Dados

### Tabela produtos
- `codigo_barras` (TEXT, PRIMARY KEY)
- `descricao` (TEXT)

### Tabela leituras
- `id` (INTEGER, AUTOINCREMENT)
- `codigo_barras` (TEXT, FK)
- `data_hora` (TIMESTAMP)

## Uso

1. **Cadastrar Produtos**: Clique em "Cadastrar Produto" para adicionar códigos de barras
2. **Iniciar Leitura**: Clique em "Iniciar Leitura" para começar a capturar da câmera IP
3. **Ver Estatísticas**: Clique em "Ver Estatísticas" para visualizar gráficos de leitura

## Tratamento de Erros

- Conexão com câmera IP indisponível
- Códigos não cadastrados (exibe aviso)
- Validação de dados de entrada