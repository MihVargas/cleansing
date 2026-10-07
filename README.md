# Correspondência inteligente de produtos

Estudo de matching de produtos que compara a descrição informada por uma loja com os itens de um catálogo. A proposta é combinar similaridade semântica e textual para identificar possíveis correspondências e sinalizar casos que precisam de revisão.

> **Status:** protótipo de estudo, executado com dados de exemplo definidos diretamente no código.

## Objetivo

Descrições de um mesmo produto podem variar entre sistemas. Diferenças de abreviação, ordem das palavras, acentuação e formatação tornam a comparação literal pouco confiável. Este projeto explora uma forma de ranquear candidatos usando duas perspectivas complementares:

- **Similaridade semântica**, calculada por embeddings de texto.
- **Similaridade textual**, calculada com comparação aproximada de palavras.

## Como funciona

1. Normaliza as descrições, separando transições entre letras minúsculas e maiúsculas, convertendo o texto para minúsculas, removendo acentos e ajustando espaços.
2. Gera embeddings para as descrições do catálogo e para o nome recebido da loja.
3. Calcula a similaridade semântica por produto usando o produto escalar dos embeddings normalizados.
4. Calcula a similaridade textual com `token_set_ratio`, da biblioteca RapidFuzz.
5. Combina os dois resultados com peso igual e ordena os candidatos.
6. Usa a pontuação do melhor candidato e a diferença para o segundo colocado para indicar match automático, possível ambiguidade ou ausência de correspondência confiável.

No exemplo atual, um resultado é aceito automaticamente quando a pontuação combinada é de pelo menos `0.85` e a diferença para o segundo colocado é de pelo menos `0.03`. Resultados a partir de `0.70` são tratados como ambíguos; abaixo disso, o exemplo recomenda revisão manual. Esses valores são parâmetros exploratórios e ainda precisam ser avaliados com dados reais.

## Tecnologias

- Python 3.12 ou superior
- [Sentence Transformers](https://www.sbert.net/) com o modelo `paraphrase-multilingual-mpnet-base-v2`
- NumPy
- RapidFuzz

## Executar o exemplo

Instale as dependências usadas pelo script:

```bash
python -m pip install sentence-transformers numpy rapidfuzz
```

Execute:

```bash
python main.py
```

Na primeira execução, o Sentence Transformers pode baixar o modelo escolhido. O script imprime as pontuações semântica, textual e combinada, o melhor candidato e a decisão correspondente.

## Estrutura

```text
.
├── main.py       # Normalização, cálculo das similaridades e decisão do exemplo
├── pyproject.toml
└── README.md
```

## Escopo e próximos passos

O código atual demonstra a ideia com um catálogo pequeno e fixo. Os pesos, limites de decisão e o modelo foram escolhidos para explorar a abordagem, não como parâmetros validados em produção. A indicação de desempate por LLM ou revisão humana aparece como possibilidade para casos ambíguos; essa integração ainda não está implementada.

Evoluções naturais para o estudo:

- carregar catálogo e consultas de arquivos ou de uma fonte de dados;
- avaliar pesos e limites com um conjunto rotulado de correspondências;
- medir precisão, cobertura e falsos matches;
- separar a preparação do catálogo da busca para evitar recalcular embeddings;
- adicionar testes para normalização, ranking e regras de decisão.

## Aprendizados explorados

- normalização de texto para reduzir diferenças de formatação;
- uso de embeddings multilíngues para comparar descrições semanticamente;
- combinação de sinais semânticos e lexicais;
- uso da margem entre os melhores candidatos para identificar ambiguidades.
