import csv
import re


class CsvReader:

    def __init__(self, filename):
        with open(filename, newline = "") as csvfile:
            delimiter = ","
            self.reader = csv.reader(csvfile, delimiter = ",")
            
            self.headless = False
            self.head_list = next(self.reader)
            
            # check if the csv file has a header row
            if not any(map(lambda header: re.match("[a-zA-Z]", header.strip()[0]), self.head_list)):
                self.headless = True
                csvfile.seek(0)

            self.value_list = []
            for row in self.reader:
                self.value_list.append(row)
            
            

    def head(self):
        if not self.headless:
            return tuple([header.strip() for header in self.head_list])
        else:
            return ()

    def head_d(self, columns):
        if not self.headless:
            columns = list(filter(lambda c: c > 0 and c < len(self.head_list) + 1, columns))
            return tuple([self.head_list[c - 1].strip() for c in columns])
        else:
            return ()
            
    def values(self):
        return list(map(lambda l: tuple(l), self.value_list))

    def values_d(self, columns):
        columns = list(filter(lambda c: c > 0 and c < len(self.value_list[0]) + 1, columns))
        return list(map(lambda l: tuple([l[c - 1] for c in columns]), self.value_list))
