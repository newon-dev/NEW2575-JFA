
Documentação da API do sistema de tracking de ponte rolante Newon.
## Projeto

* NEW2575 
* Numero Documento: NEW2575-JFA-MDE-004
## Autores

- [Victor Sousa](mailto:victor.sousa@newon.io)
- [Newon](http://newon.io)


## Histórico de Revisões

| Data | Comentários | Retorno | Status |
| ---- | ----------- | ------- | ------ |
|   26/02/2025   |    Emissão Original         |     --    |   --     |
|      |             |         |        |
|      |             |         |        |
|      |             |         |        |
|      |             |         |        |
```Comentários






```







## Comissionado por

Esse projeto é usado pelas seguintes empresas:

- ArcelorMittal

## Stack utilizada

**Front-end:** #ReactJs #TailwindCss

**Back-end:** #Python #Flask

## Suporte

Este sistema foi projetado para ser executado para utilização em sistemas Linux/Unix. No entanto pode ser utilizado em sistemas Microsoft Windowns, com algumas modificações. (Não recomendado)


##  Instalação
Para realizar a instalação do projeto.

Após realizar o download do projeto, extraia o conteúdo, e navegue até a pasta do projeto utilizando o terminal.

```bash
 cd pasta_do_projeto
``` 

Em seguida crie o ambiente virtual para execução do projeto. 

```bash
python -m venv ponte_rolante
```

>Caso seu sistema, não reconheça a instalação do python, tente utilizar:

```bash
python3 -m venv ponte_rolante
```

Em seguida iremos ativar nosso ambiente virtual. 

```bash
. ponte_rolante/bin/activate
```

Deverá aparecer uma legenda antes do seu nome de usuário com o escrito:
```bash
(ponte_rolante) nome de usuário $: 
```

## Instalação das bibliotecas necessárias:

Para instalar as bibliotecas necessárias iremos executar ainda no terminal, com  o ambiente virtual inicializado. 

```bash
pip install -r requirements.txt
```

>Este procedimento pode levar alguns minutos (esperado). E não deve apresentar erros. 

==Caso sejam apresentados erros entre em contato com o suporte newon.io==

## Inicialização do servidor. 

Agora iremos inicializar o servidor. 

O servidor utiliza por padrão a porta 8080. Lembre-se de realizar as ações de liberação necessárias em seu sistema de segurança de rede interna, para permitir o funcionamento adequado do sistema.

>Primeiramente ative o ambiente virtual como descrito no passo anterior (Instalação) .

Em seguida:
```bash
python run.py
```

Caso o sistema acuse erro tente utilizar:

```bash
python3 run.py
```

Isso irá garantir que o sistema seja executado, e realize o monitoramento necessário. 

>Nota o sistema irá ser executado apenas enquanto o terminal estiver aberto com o sistema em execução. 

Para realizar a execução em segundo plano:

```bash
nohup python run.py &
```

Isso irá garantir que o sistema fique em execução em segundo plano

>Nota em caso de reinicialização do sistema, a aplicação deverá ser reinicializada. Pode ser recomendado a configuração da aplicação como serviço.

[Configurando aplicação python como serviço linux](https://www.codementor.io/@ufuksfk/how-to-run-a-python-script-in-linux-with-systemd-1nh2x3hi0e)

>Adicionalmente o usuário tem a opção de utilizar o sistema utilizando diretamente o comando:

```bash
python api.py
```

> Quando executado diretamente, o programa irá ser executado em modo manual, e portanto, em caso de falha NÃO será reiniciado automaticamente.

## Reinicialização Automática

O módulo de supervisão **run.py** possuí como responsabilidades, a reinicialização do sistema de servidores, automaticamente.  

>Caso o sistema de servidor apresente mais de 3 erros seguidos em um intervalor igual ou menor a 300 segundos. O sistema de supervisão irá automaticamente suspender a execução do módulo afetado. Os demais continuarão em funcionamento. 
>==É extremamente recomendado que não se utilize o sistema com módulos apresentando erros ou em mal funcionamento. Isso pode comprometer a integridade dos dados apresentados==


## Utilizando o arquivo de logs. 

Quando o sistema estiver em execução o módulo irá gerar em um arquivo de logs configurável informações relevantes sobre o funcionamento do sistema. 

**Exemplo de arquivos de logs**

``` NewonDaemonLogs.log
2025-02-20 13:54:43 - INFO - Iniciando track_new.py...
2025-02-20 13:54:43 - INFO - Iniciando api.py...
2025-02-20 13:54:50 - INFO - Monitoramento interrompido pelo usuário.
2025-02-20 13:54:50 - ERROR - api.py falhou.
2025-02-20 13:54:50 - ERROR - track_new.py falhou.
2025-02-25 08:20:29 - INFO - Iniciando api.py...
2025-02-25 08:20:29 - INFO - Iniciando track_new.py...
2025-02-25 08:20:29 - ERROR - api.py falhou.
2025-02-25 08:20:29 - ERROR - track_new.py falhou.
```


#### Configurando o nome do arquivo de logs:

>Todos os parâmetros programáveis, devem ser editados diretamente nos arquivos de código fonte do sistema. Sempre tenha em mãos um backup prévio do sistema. NÃO modifique esses arquivos sem o conhecimento concreto das mudanças que estas a realizar.

| Paramêtro | Funcionalidade                      | Tipo |
| --------- | ----------------------------------- | ---- |
| LOG_FILE  | Nome do arquivo de log a ser gerado | STR  |

#### Configurando o máximo de tentativas e limite de tempo para reinicialização.



| Paramêtro     | Funcionalidade                           | Tipo |
| ------------- | ---------------------------------------- | ---- |
|  MAX_ATTEMPTS | Máximo de tentativas de reinicialização  | INT  |
| TIME_WINDOW   | Tempo de reset do contador de tentativas | INT  |

## Configuração API

Após a instalação e configuração do sistema de monitoramento do sistema, iremos apresentar as configurações e descrição da API do sistema de tracking ponte rolante Newon.

### Banco de dados.
O sistema já vai embarcado com um banco de dados do tipo SQLITE configurado para utilização. Recomendamos máxima cautela ao manipular este arquivo. No entanto o módulo de banco de dados possuí todos os métodos necessários para recriação do banco de dados. 

>Em caso de necessidade de recriação do banco de dados solicite o suporte newon.io

##### Configuração do nome do banco de dados. 

O nome do banco de dados utilizado pode ser facilmente modificado se modificando no código fonte o parâmetro:

```bash
	db = BancoDeDados("movimentacao.db")
```

>Apenas realize mudanças no código fonte, se tiver plena convicção do que estiveres modificando.

#### Porta de comunicação da aplicação (API)

A aplicação API usa por padrão a porta TCP 8080 para evitar conflitos.

>Em casos raros podem acontecer conflitos, caso alguma outra aplicação esteja utilizando a mesma porta para se comunicar no mesmo endereço IP.

``` Error
OSError: [Errno 98] Address already in use
```

>Erro representando uma tentativa, de utilização de uma mesma porta por duas aplicações. 

**Modificando a porta de comunicação da aplicação**

Para modificar a porta de comunicação da aplicação basta modificar no código fonte a seguinte informação:

``` python
	app.run(debug=True, host="0.0.0.0", port=8080)
```

> Para modificar a porta de comunicação, basta modificar a numeração 8080 por outra.
>As portas são numeradas de 0 até 65535. E qualquer uma pode ser utilizada desde que não esteja em uso.

**Outros parâmetros de inicialização da API**

| Parâmetro | Funcionalidade                                 | Tipo |
| --------- | ---------------------------------------------- | ---- |
| DEBUG     | Inicializa o servidor em modo de debug         | BOOL |
| HOST      | Endereço de ip que o servidor tentará utilizar | STR  |
| PORT      | Porta de comunicação utilizada pelo servidor   | INT  |
>Mais a frente iremos descrever em detalhes cada endpoint da API da aplicação.


## Configuração Do Módulo de Leitura de Tags

O módulo rfid.py é responsável pela comunicação direta com as antenas, responsável por receber e processar os dados das antenas. 

#### Configurações do módulo.

| Parâmetro | Funcionalidade                            | Tipo |
| --------- | ----------------------------------------- | ---- |
| Port      | Porta usada para comunicar com as antenas | int  |
| Timeout   | Tempo limite da operação de leitura       | int  |
> A porta de comunicação é definida pela antena, e não deve ser modificada, uma vez que o dispositivo espera receber a conexão por essa porta TCP.

> O sistema de RFID foi desenvolvido e testado para se comunicar exclusivamente com as antenas RFID SIEMENS SIMATIC RF610R 


## Configuração Do Módulo DB

O módulo db.py é responsável por abstrair todas as comunicações com o banco de dados do sistema.

#### Configurações do módulo.

| Parâmetro       | Funcionalidade                                | Tipo |
| --------------- | --------------------------------------------- | ---- |
| NUMERO_POSICOES | Número máximo de possíveis posições no galpão | int  |

## Configuração Do Módulo Track_New

O módulo Track_New.py   é responsável realizar o rastreamento das pontes, atualização do banco de dados com as novas leituras.

#### Configurações do módulo.

| Parâmetro                  | Funcionalidade                                             | Tipo |
| -------------------------- | ---------------------------------------------------------- | ---- |
| MOSTRAR_BARRA_CARREGAMENTO | Deprecated: Mostrava uma barra de carregamento no terminal | BOOL |
| Database                   | Banco de dados utilizado                                   | STR  |
> O database utilizado no módulo deve ser o mesmo utilizado nos outros locais da aplicação. Sob pena de não funcionamento adequado do sistema. 

## Documentação dos Endpoints da API

A Api utiliza objetos json para envio e recebimento de dados. 

>Todas as comunicações com a API devem exclusivamente serem realizadas através do método POST utilizando payloads do tipo JSON. 

### Endpoint: /ultima_posicao

Retorna a ultima posição conhecida da ponte solicitada. 

``` Modelo requisição
{
	'ponte': 1
}
```

Resposta Esperada:

``` Resultado
	{
		"x": 1,
		"y": 2 
		"horario": 2025-02-04 10:00:00
	}
```

>Após receber o numero da ponte desejada, o sistema irá retornar com o horário e a ultima leitura da posição da ponte. (Em geral será a posição atual dela, uma vez que o sistema é atualizado constantemente)

==A leitura pode não corresponder com a realidade caso: 
O sistema de tracking tenha sido desligado
A ponte tenha se movido para outra posição e não tenha sido movida após o 
religamento do sistema de tracking. ==

Neste caso assim que a ponte se mova novamente ela será atualizada. 

### Endpoint: /chek_antena

Realiza um teste, e retorna uma lista com as antenas conectadas na rede.

>Para que essa conexão ocorra com sucesso, é imprescindível que as antenas tenham sido configuradas via frontend. 

``` Modelo requisição
{
	
}
```

>Para essa requisição não é necessário que se envie nada no corpo da mensagem

Resposta Esperada:

``` Resultado
[
    {

        "ip": "10.0.0.11",

        "nome": "Antena Eixo X"
    },

    {
        "ip": "10.0.0.10",

        "nome": "Antena eixo y"
    }
]
```

>O sistema irá retornar um array de dicionários contendo o ip e o nome cadastrado de cada antena que foi configurada e conectada corretamente ao sistema.


### Endpoint: /recuperar_antenas

Retorna as antenas cadastradas no sistema, independente do status de conexão

``` Modelo requisição
{
	
}
```

>Para essa requisição não é necessário que se envie nada no corpo da mensagem

Resposta Esperada:

``` Resultado
[
    {

        "ip": "10.0.0.11",

        "nome": "Antena Eixo X"
    },

    {
        "ip": "10.0.0.10",

        "nome": "Antena eixo y"
    }
]
```

>O sistema irá retornar o nome e endereço de ips cadastrados no sistema para cada antena cadastrada. Limite de 4 antenas.


### Endpoint: /modificar_antenas

Modifica os dados de uma antena no banco de dados

``` Modelo requisição
{
	'id': 1,
	'nome': 'Antena X1',
	'ip' : '10.0.0.11'
}
```

>Todos os dados são necessários para modificação da antena

Resposta Esperada:

``` Resultado
	{
		"success": "false", 
		"erro": "Não foi possível atualizar a antena."
	}
```
	 ou
``` retorno
	{
		"success": "true"
	}
```
	 

>O sucesso retorna a flag sucess informando o sucesso ou falha da operação, e em caso de falha o motivo.

### Endpoint: /download_csv

Faz o download das ultimas posições em formato csv para análise

``` Modelo requisição
{
	'limite' : 50
}
```

>Limite se trata do número máximo de leituras a serem recebidas.

Resposta Esperada:

``` Resultado
	{
		id,x,y,ponte,hora
		5,4,0,1,2025-02-04 10:00:00
		4,3,0,1,2025-02-04 10:00:00
		3,2,0,1,2025-02-04 10:00:00
		2,1,0,1,2025-02-04 10:00:00
		1,0,0,1,2025-02-04 10:00:00
	}
```

>O retorno do endpoint já é o arquivo CSV.

























