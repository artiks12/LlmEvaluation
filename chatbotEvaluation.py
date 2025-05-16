from os import listdir
from os.path import isfile, join
import json

ASPEKTI = {
    'Līdzība':{
        '[aspektu]':'teksta semantisko līdzību',
        '[aspekts]':'teksta semantiskā līdzība',
        '[anti-aspekts]':'nesakritība',
        '[ideals-aspekts]':'ideāla līdzība',
        '[aspekta-ins]':'cik semantiski/saturīgi līdzīgs/adekvāts/pilnvērtīgs ir ģenerētais teksts attiecībā pret cilvēka/jurista sagatavoto atsauci. Ņem vērā, ka vienu un to pašu tekstu/atbildi var uzrakstīt dažādi, lai pateiktu vienu un to pašu domu.'
    }
}

UZDEVUMI = {
    'LatLegQ&A':{
        '[uzdevums]':'atbildi uz jautājumu par Latvijas likumdošanu un normatīvajiem aktiem, izmantojot dotās atsauces uz relevantajiem likumu pantiem un likumiem kopumā'
    }
}

def GetSupervisedEvaluationInstructions(file,source,metric,task):
    instructions = {}

    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    # Iztulkots un paņemts no šejienes: https://arxiv.org/pdf/2303.04048
    instruction_base = """Novērtē šādu [uzdevums] attiecībā uz [aspektu] nepārtrauktā skalā no 0 līdz 100, kur vērtējums nulle nozīmē "[anti-aspekts]", bet vērtējums simts nozīmē "[ideals-aspekts]". Ņem vērā, ka [aspekts] nosaka, [aspekta-ins] Izdrukā tikai vērtējumu.
Jautājums: [Jautājums]
Cilvēka atsauce: [Cilvēka atsauce]
Ģenerētais teksts: [Ģenerētais teksts]
Vērtējums: """

    instruction_base = instruction_base.replace('[uzdevums]',UZDEVUMI[task]['[uzdevums]'])
    
    for d in data['Qs&As']:
        question = d['question'].replace('\n',' ').replace('\r',' ')
        answer = d['answer'].replace('\n',' ').replace('\r',' ')
        gold = d['gold'].replace('\n',' ').replace('\r',' ')

        instruction = instruction_base.replace('[Jautājums]',question) \
                                        .replace('[Cilvēka atsauce]',gold) \
                                        .replace('[Ģenerētais teksts]', answer)
                                        

        for aspect in ASPEKTI[metric].keys():
            value = ASPEKTI[metric][aspect]
            instruction = instruction.replace(aspect, value)
        
        num_id = d['id'] if 'id' in d.keys() else count
        instructions[str(num_id)] = instruction
        count += 1

    with open(f'instructions/SupervisedLlmEvaluation/ChatbotEvaluate{source}', 'wt', encoding='utf-8') as f:
        json.dump(instructions, f, ensure_ascii=False, indent=4)

path = 'ModelResponses/'

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
for file in onlyfiles:
    fullFile = path + file
    GetSupervisedEvaluationInstructions(fullFile,file,'Līdzība','LatLegQ&A')