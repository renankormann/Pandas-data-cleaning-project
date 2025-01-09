import numpy as np
import pandas as pd


# Importar todos os clientes como DF
clientes = pd.read_excel(io = 'ClientesAll.xlsx')
#print(clientes.shape) # Testing

# Importar clientes que nao compram a 5 anos ou mais como DF
clientes5Anos = pd.read_excel(io = 'ClientesSemCompra5anos.xlsx')

# Importar clientes com credito como DF
clientesComCredito = pd.read_excel(io = 'ClientesComCredito.xlsx')

# Importar Clientes Inadimplentes como DF
clientesInadimplentes = pd.read_excel(io ='ClientesInadimplentes.xlsx')

# Objetivo do programa: Limpar os dados da empresa excluindo clientes que:
# - Ficaram 5 anos sem comprar
# - Clientes com CPF 999.999.999-99
# - Clientes que tem no nome (Troca)
# - Duplicados
# - Caducou.
# Lembrando sempre que antes de excluir qualquer nome devo conferir se este nome esta presente nos DF
# de ClientesComCredito e ClientesInadimplentes.

## Definir funcao que confere se os nomes estao presentes na lista de inadimplentes e com creditos
# e devolver DF sem esses nomes
def conferir_nomes(arg1):
    clientesSemInadimplencia = arg1[~arg1['fccod'].isin(clientesInadimplentes['fccod'])]
    # print("clientes S Inadimplencia ", clientesSemInadimplencia.shape) # Teste
    clientesFinal = clientesSemInadimplencia[~clientesSemInadimplencia['fccod'].isin(clientesComCredito['fccod'])]
    # print("Clientes pos funcao ", clientesFinal.shape) # Teste
    return clientesFinal


# 1-  Criar um DF com a lista de clientes que nao compram a mais de 5 anos que nao sao inadimplentes
# para remover da lista total de clientes

#print("Clientes 5 Anos antes funcao ", clientes5Anos.shape) # Teste

# Removendo do DF de Clientes5Anos os nomes de quem deve ou tem credito na loja e salvando em 
# clientes5AnosClean
clientes5AnosClean = conferir_nomes(clientes5Anos)
#print("Clientes 5 anos clean ",clientes5AnosClean.shape) #Teste
#print("Clientes " , clientes.shape) #Teste

# Remover clientes5AnosClean de Clientes e salvar como novo DF clientesClean, que sera o final
clientesClean = clientes[~clientes["fccod"].isin(clientes5AnosClean["fccod"])]
#print("Clientes Clean 5 anos ", clientesClean.shape) # Teste

## Criar um DF com os clientes que possuem CPF 999.999.999-99
clientesCPF_errado = clientesClean[clientesClean['fccpg'] == 99999999999]
#print("CPF", clientesCPF_errado.shape) # Teste

# Remover do DF de CPF errado os nomes de quem esta devendo ou que tem credito
clientesCPF_erradoClean = conferir_nomes(clientesCPF_errado)
#print("CPF clean", clientesCPF_erradoClean.shape) # Teste

# Remover clientesCPF_erradoClean de clientesClean
clientesClean = clientesClean[~clientesClean['fccod'].isin(clientesCPF_erradoClean['fccod'])]
#print("Clientes Clean ,PF ", clientesClean.shape)


## Criar um DF com os clientes que possuem (Troca) no nome
clientesTroca = clientesClean[clientesClean['fcnom'].str.contains(pat = 'TROCA') == True]
#print("Troca ", clientesTroca.shape) # Teste
#print(clientesTroca.head()) # Teste

# Remover do DF de clientes que possuem TROCA no nome os que estao devendo ou tem credito
clientesTrocaClean = conferir_nomes(clientesTroca)
#print("Clientes Troca Clean" , clientesTrocaClean.shape) # Teste

# Remover clientesTrocaClean de clientesClean
clientesClean = clientesClean[~clientesClean['fccod'].isin(clientesTrocaClean['fccod'])]
#print("Clientes Clean Troca ", clientesClean.shape) #Teste

## Criar DF com clientes duplicados
clientesDuplicados = clientesClean[clientesClean["fcnom"].duplicated(keep = False)]
#print("Clientes Duplicados", clientesDuplicados.shape) #Teste

# Remover de clientesDuplicados os clientes que tem credito ou estao devendo
clientesDuplicadosClean = conferir_nomes(clientesDuplicados)
#print("Clientes Duplicados Clean", clientesDuplicadosClean.shape) #Test

# Remover clientes duplicadosClean de clientes
clientesClean = clientesClean[~clientesClean['fccod'].isin(clientesDuplicadosClean['fccod'])]
#print("Clientes Clean Duplicados ", clientesClean.shape) #Test


## Passar clientesClean para uma planilha excel
clientesClean.to_excel('ClientesClean.xlsx')


## Montar uma planilha unica com Clientes que devem ser removidos
clientesParaRemover = pd.concat([clientes5AnosClean,clientesCPF_erradoClean,clientesTrocaClean,clientesDuplicadosClean])
clientesParaRemover.to_excel('ClientesParaRemover.xlsx')