from string import ascii_uppercase
from random import randint

def build_table(text_file,tabbed=False,lettered=False,start=0):
    dict = {}
    entries = []
    for line in text_file:
        if line != '\n' and line != '\r\n':
            if not tabbed:
                entries.append(line.strip('\n'))
            else:
                entries.append(line.strip('\n').split('\t'))
        else:
            if not lettered:
                dict.update({start:entries})
            else:
                dict.update({ascii_uppercase[start]:entries})
            entries = []
            start += 1
    return dict

def build_encounters():
    """Returns a dictionary of encounter tables."""
    with open('encounters.txt','r') as text:
        return build_table(text,tabbed=True,start=1)

def build_matrices():
    """Returns a dictionary of matrix response tables."""
    with open('responses.txt','r') as row_text, open('matrices.txt','r') as column_text:
        matrix_dict = build_table(row_text,lettered=True)
        altered_dict = {k:[v] for k,v in matrix_dict.iteritems()}
        counter = 0
        response_column = []
        for line in column_text:
            if line != '\n' and line != '\r\n':
                response_column.append(line.strip('\n'))
            else:
                altered_dict[ascii_uppercase[counter]].append(response_column)
                response_column = []
                counter += 1
    return altered_dict

def build_tales():
    """Returns a dictionary containing each encounter/reaction matrix"""
    with open('tales.txt','r') as text:
        return build_table(text,tabbed=True,lettered=True)

def calc_entry():
    """Returns the entry number for the current encounter table"""
    location = int(raw_input('Enter the number on your current location (0 if blank): '))
    destiny_score = raw_input('Enter your current destiny score: ')
    if destiny_score < 4:
        destiny_mod = 0
    elif destiny_score > 6:
        destiny_mod = 2
    else:
        destiny_mod = 1
    entry_number = randint(1,6) + int(location) + destiny_mod
    if entry_number > 12:
        return 12
    else:
        return entry_number

def n_encounters(encounter_dict):
    """A special function for N location encounters"""
    while True:
        entry_number = raw_input(
                    """Please select the appropriate encounter from the list below
                    1. Ape Island               11. Pavillion of the Black Giant
                    2. Barber                   12. Pearl Diving
                    3. Crystal Palace           13. Rhino
                    4. Dendan                   14. Serpent
                    5. Elephant                 15. Sex-Change Spring
                    6. Elephant's Graveyard     16. Valley of Dogs
                    7. Islands of Camphor       17. Volcano
                    8. Lion                     18. Warfleet
                    9. Magnetic Mountain
                    10. Palace of 100 Closets
                    > """)

        try:
            zero_test = 1 / int(entry_number)
            return encounter_dict.get(113)[abs(int(entry_number)) - 1]
        except (ZeroDivisionError, IndexError, KeyError,TypeError, ValueError) as e:
            print "Unacceptable response. Try again"

def find_encounter(encounter_dict):
    """The user inputs an encounter number. The function then checks the entry value and returns that entry
    entry from the corresponding encounter table. """
    while True:
        encounter_number = raw_input('Enter the number on your encounter card: ')
        try:
            if encounter_number.upper() == 'N':
                return n_encounters(encounter_dict)
            elif encounter_number.upper() == 'G':
                return ['Badly Lost','G']
            else:
                return encounter_dict.get(int(encounter_number))[calc_entry()-1]
        except (KeyError, TypeError) as e:
            print('Not an acceptable encounter number.')

def check_matrix(encounter, matrix_dict):
    """Returns a tuple of the encounter and the given response to an encounter"""
    matrix_table = matrix_dict[encounter[1]]
    while True:
        print('Encounter type: %s. Choose one of the following responses from Matrix Table %s:\n%s.'
          % (encounter[0], encounter[1],matrix_table[1]))
        response = raw_input(': ')
        try:
            for row in matrix_table[0]:
                if encounter[0].find(row) >= 0:
                    return matrix_table[0].index(row), matrix_table[1].index(response)
            print("Please type the desired response.")
        except (ValueError, TypeError) as e:
            print("Please type the desired response.")

def match_tale(tales_dict, encounter,matrix_coordinates):
    """Returns the resulting tale from a given encounter and response, +/- 1"""
    row, column = matrix_coordinates
    tales_array = tales_dict.get(encounter[1])
    modifier = randint(-1,1)
    return int(tales_array[row][column]) + modifier

def puttin_it_together():
    encounter_dict = build_encounters()
    matrix_dict = build_matrices()
    tales_dict = build_tales()
    current_encounter = find_encounter(encounter_dict)
    matrix_coordinates = check_matrix(current_encounter, matrix_dict)
    print "Read entry number: %i" % (match_tale(tales_dict, current_encounter, matrix_coordinates))

puttin_it_together()