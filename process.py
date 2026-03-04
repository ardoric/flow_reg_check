import csv
import sys
import flow_validator



if __name__ == "__main__":
    with open("registrations.csv", newline='', encoding='utf-16') as file:
        reader = csv.DictReader(file, delimiter='\t')
        registrations = list(reader)

    bad, warning, good, ignored = flow_validator.validate(registrations)

    for dog in bad:
        print (dog['reason'], dog['dog']['Dog Name'])

    print (len(bad), len(warning), len(good))
