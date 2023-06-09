

# Pacote para fornecer support aos projetos da Venidera através do Trello.

![GitHub Release](https://img.shields.io/badge/release-v0.1.0-blue.svg)
![GitHub license](https://img.shields.io/badge/license-Proprietary-yellow.svg)

O pacote vsupport faz a interface entre os projetos da Venidera e o Trello.

## Tabela de conteúdos

[TOC]

## Pré-requisitos

* Python 3.8 ou superior (`sudo apt-get install python3.8`)
* Python virtual environment (`sudo apt-get install python3.8-venv`)
* 
* Trello Delevoper Guides:
  * [Authorizing with Trello's REST API](https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/)
  * [REST API](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/)

## Estrutura dos pacotes

Os arquivos do pacote estão estruturados inicialmente em:

- `vsupport` diretório raiz.
    -   `README.md`  Descritivo do pacote, escrito em Markdown.
    -   `setup.py` O script para construir/instalar o pacote.
    -   `LICENSE` Texto padrão da licença.
    -   `.gitignore` Contém especificações de arquivos a serem ignorados no GIT.
    -   `vsupport` Diretório base dos pacotes.
        -   `vtrello.py` Pacote para manipular dados do Trello.
    -   `scripts` Diretório base dos scripts do usuário.
        -   `run.py` Script padrão para executar o aplicativo.
    -   `tests` Coleção de testes de uso geral.
        -   `test_vtrello.py` Script com testes para o módulo trello `vtrello.py`.

### Personalizando o arquivo setup.py

O arquivo setup.py é o que descreve o pacote e diz ao setuptools como empacotá-lo, compilá-lo e instalá-lo. O script de configuração pode incluir metadados adicionais que devem ser definidos de acordo com os requisitos de cada projeto. Essas informações incluem:

| Metadados | Descrição Valor | Notas
| - | - | - | - |
| name | nome do pacote | texto curto | O pacote deve ter nomes curtos, todos em minúsculas. Sublinhados podem ser usados ​​no nome do módulo se melhorar a legibilidade. |

| version | versão deste lançamento | texto curto | Recomenda-se que as versões tenham o formato _major.minor [.patch] _. Consulte [PEP 440] (https://www.python.org/dev/peps/pep-0440) para obter mais detalhes sobre as versões. |

| author | nome do autor do pacote | texto curto | |

| author_email | endereço de email do autor do pacote | endereço de email | |

| url | página principal do projeto | URL | Este será apenas um link para GitHub, GitLab, Bitbucket ou serviço similar de hospedagem de código. |

| description | uma breve descrição resumida do pacote | texto curto | |

| keywords | uma lista de palavras-chave | lista de textos | Se você passar um texto separado por vírgulas `'foo, bar'`, ele será convertida em` [' foo ',' bar ']`, Em caso contrário, ele será convertido em uma lista de um texto. |

| classifiers | uma lista de classificadores | lista de textos | Os classificadores válidos estão listados em [PyPI] (https://pypi.org/classifiers). |

| license | licença sob a qual o projeto é lançado | texto curto | O campo `license` é um texto que indica a licença que cobre o pacote e atua como um apelido para o arquivo` LICENSE`. |

| public_dependencies | uma lista pública de pacotes Python [pacotes de importação] públicos (https://packaging.python.org/glossary/#term-import-package) | lista de texxtos | |

| private_dependencies | uma lista de dependências de pacotes privados | lista de textos | Eles representam os nomes dos pacotes privados da Venidera no Bitbucket/GitHub.

## Desenvolvimentos e Testes

### 1. Clonando o repositório

Primeiro devemos fazer uma "cópia" clonando o repositório `vsupport do Github. Você precisa ter o ssh configurado no seu sistema, com acesso autorizado no Github.
```bash
$ mkdir ~/git
$ git clone git@github.org:venidera/vsupport.git ~/git/vsupport
$ cd ~/git/vsupport
```

### 2. Instalando o pacote

Inicie criando um novo ambiente virtual para seu projeto (python/venv). Em seguida, atualize os pacotes `pip` e` setuptools` para a versão mais recente. E finalmente, instale o próprio pacote.
```bash
$ /usr/bin/python3.8 -m venv --prompt="projeto" venv
$ source venv/bin/activate
(projeto) $ pip install --upgrade setuptools==58.4.0 pip
(projeto) $ python setup.py install
```

### 3. Verificando o código

Durante a codificação, é possível utilizar o `Pylint`para verificar os possíveis erros nos códigos python usand:
```bash
(projeto) $ python setup.py pylint
```
Pylint é uma ferramente que tenta manter uma padronização de codificação procurando por possíveis falhas nos códigos. [code smells](https://martinfowler.com/bliki/CodeSmell.html). Pylint mostrará vária mensagens enquanto analisa o código e ele também pode mostrar algumas estatísticas. O pacote atual utiliza uma configuração personalizada para o padrão da Benidera [configuration file](https://drive.google.com/a/venidera.com/uc?id=1SeUYS-g-MTj-7a_XYwaXZUQpDiQ26JuW).


### 4. Testando os módulos do pacote

Os testes Python são classes Python presentes em arquivos separados dos códigos e servem para testá-los. Os testes são baseados no pacote Python `unitest` e estão localizados na pasta `tests`. Eles podem ser executados por:
```bash
(projeto) $ python setup.py test
```
Em geral, o desenvolvedor pode criar e executar quantos testes achar necessários. Entretanto, eles são importantes para validar as alterações dos códigos, antes de publicá-las nos repositórios (`Github`),  evitando os erros. É importante mencionar que os testes serão realizados somente se as classes de testes estenderem o objeto `unittest.TestCase`.


### 5. Execuntando o aplicativo

Para executar o seu pacote (e também para gerar um script que ajude outros a usarem o seu pacote), coloque as rotinas de execução do seu pacote no arquivo `scripts/run.py`. Então, uma vez que a sintaxe do pacote esteja no padrão `Venidera`, e todos os testes executados com sucesso, você pode executar o seu aplicativo como segue:
```bash
(projeto) $ python scripts/run.py
```

## Problemas e Soluções:

Por favor, registre os problemas no Github em [report a bug](https://github.org/venidera/vsupport/issues?status=new&status=open).

## Desenvolvedores

-   Venidera Development Team - [suporte@venidera.com](mailto:suporte@venidera.com)

## Licença

Este pacote está publicado e distribuído sob a licença [GNU GPL Version 3, 29 June 2007](https://www.gnu.org/licenses/gpl-3.0.html).

#   v s u p p o r t  
 