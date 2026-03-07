import csv
import datetime
import time

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
    # licenses by license number
    licences = { l['Nº Licença']: l for l in reader }
    lop_licences = { l['Nº Registo']: l for l in licences.values() }

def parse_date(strdate):
    # date.strptime my beloved only available in 3.14
    return datetime.date(*(time.strptime(strdate,'%d/%m/%Y')[0:3]))

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

# maps classes in licenses for classes in flow
# leaving design space for S+M or I+L and that kind of things
# no example in the liceses for a XS dog so I'm assuming the license is for SMALL (S)
classes = {
        "SMALL (S)"       : ["XS+S (XS)", "XS+S (S)", "S", "XS"],
        "MEDIUM (M)"      : ["M"], 
        "INTERMEDIATE (I)": ["I"],
        "LARGE (L)"       : ["L"]
}


def validate(registrations):
    good     = []
    bad      = []
    warning  = []
    ignored  = []


    for dog in registrations:
        # remove white space
        # aka, the Peach case
        dog['Agility License Number'] = dog['Agility License Number'].strip()

        if dog['Agility Federation'] != "CPC":
            ignored.append(dog)
            continue

        if dog['Agility License Number'] not in licences:
            # try by LOP
            if dog['Dog Studbook Number'].strip() in lop_licences:
                bad.append(
                    {'dog': dog, 
                     'reason': f"licença {dog['Agility License Number']} incorrecta. licença para {dog['Dog Studbook Number']} devia ser {lop_licences[dog['Dog Studbook Number'].strip()]['Nº Licença']}"
                })
            else:
                bad.append({'dog': dog, 'reason': 'licença nao encontrada'})
            continue
        
        license = licences[dog['Agility License Number']]

        # not checking licence date for G0 dogs
        if dog['Grade'] != 'G0' and parse_date(license['Validade']) < datetime.date.fromisoformat(dog['Trial Date']):
            bad.append({'dog': dog, 'reason': 'licença nao valida a data da prova. data prova: {dog["Trial Date"]} licença expira: {license["Validade"]}'})
            continue
        
        # check that license matches dog registration
        if dog['Dog Studbook Number'].strip() and dog['Dog Studbook Federation'] == 'Clube Português de Canicultura':
            if dog['Dog Studbook Number'].replace(' ', '').strip().lower() != license['Nº Registo'].replace(' ','').strip().lower():
                bad.append({'dog': dog, 'reason': f"Nº registo da licença {license['Nº Registo']} nao corresponde ao nº registo na prova {dog['Dog Studbook Number']}"})
                continue

        if dog['Grade'] != license['Grau']:
            warning.append(
                    {'dog': dog, 'reason': f"grau inconsistente. licença: {license['Grau']}, prova: {dog['Grade']}"}
            )
            continue

        # some dogs don't have class assigned in the license
        if license['CLASSE'].strip() in classes:
            if dog['Category'] not in classes[license['CLASSE'].strip()]:
                warning.append(
                    { 'dog': dog,
                      'reason': f"Categoria da licença {license['CLASSE']} nao corresponde a categoria de inscricao {dog['Category']}"
                    }
                )
                continue
        
        # no issues found
        good.append(dog)
    return ( bad, warning, good, ignored)

