import csv


FLOW_FIELDS = [
    'Dorsal',
    'Handler (first name)',
    'Handler (last name)',
    'Email',
    'Dog Microchip',
    'Dog Name',
    'Dog Date of Birth',
    'Dog Gender',
    'Dog in Season',
    'Dog Height',
    'Dog Breed',
    'Dog Studbook Name',
    'Dog Studbook Number',
    'Dog Studbook Federation',
    'Agility Club',
    'Agility License Number',
    'Agility Federation',
    'Agility Country',
    'No Agility License',
    'Participant Type',
    'NP',
    'Trial Name',
    'Trial Date',
    'Handler',
    'Grade',
    'Category',
    'Team Requested',
    'Team Assigned',
    'Participant Observations',
    'Organizer Observations',
    'Flagged',
    'Status',
    'Registered at',
    'Handler (full name)'
]


with open("licencas.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    licences = { l['Nº Licença']: l for l in reader}


# registrations
# Dorsal
# Handler (first name)
# Handler (last name)        | Condutor (Último Nome)
# Email
# Dog Microchip              | Microchip
# Dog Name                   | Cão
# Dog Date of Birth          | Data de nascimento
# Dog Gender                 | Género
# Dog in Season              | Em cio
# Dog Height                 | Altura
# Dog Breed                  | Raça
# Dog Studbook Name          | Nome de Pedigree
# Dog Studbook Number        | Nr de Pedigree
# Dog Studbook Federation    | Federação de Registo
# Agility Club               | Clube
# Agility License Number     | Licença
# Agility Federation         | Federação
# Agility Country            | País
# No Agility License         | Sem Licença
# Participant Type           | Tipo de participante
# NP
# Trial Name                 | Nome da Prova
# Trial Date                 | Data da Prova
# Handler                    | Condutor
# Grade                      | Grau
# Category                   | Categoria
# Team Requested             | Equipa Pedida
# Team Assigned              | Equipa Assignada
# Participant Observations   | Observações Participante
# Organizer Observations     | Observações Organizador
# Flagged                    | Sinalizado
# Status                     | Estado
# Registered at              | Data de inscrição
# Handler (full name)

def parse_flow(fname):
    with open(fname, newline='', encoding='utf-16') as f:
        reader = csv.DictReader(f, fieldnames=FLOW_FIELDS, delimiter='\t')
        # skip the headers
        next(reader)
        return list(reader)


# licences
# Grau
# Válida
# Nº Licença
# Nº Registo
# Nome do cão
# Nome de Registo
# Raça
# Proprietário
# Data Início G1
# Data Pagamento
# Validade
# CLASSE
# Medição Efetuada

def validate(registrations):
    good     = []
    bad      = []
    warning  = []
    ignored  = []


    for dog in registrations:

        # if dog['Agility Federation'] != "CPC":
        if dog['Federação'] != "CPC":
            ignored.append(dog)
            continue

        # if dog['Agility License Number'] not in licences:
        if dog['Licença'] not in licences:
            bad.append({'dog': dog, 'reason': 'licença nao encontrada'})
            continue

        # if licences[dog['Agility License Number']]['Válida'] != "SIM":
        if licences[dog['Licença']]['Válida'] != "SIM":
            bad.append({'dog': dog, 'reason': 'licença inválida'})
            continue

        good.append(dog)
    return ( bad, warning, good, ignored)

