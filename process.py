import csv
import sys
import flow_validator



if __name__ == "__main__":

    registrations = flow_validator.parse_flow(sys.argv[1])

    bad, warning, good, ignored = flow_validator.validate(registrations)

    for dog in bad:
        print (dog['reason'], dog['dog']['Dog Name'])
        print (dog)

    print()

    for dog in warning:
        print (dog['reason'], dog['dog']['Dog Name'])

    print (len(bad), len(warning), len(good))
