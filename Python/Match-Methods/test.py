import os.path as path

two_up =  path.abspath(path.join(__file__ ,"../../.."))


paths = two_up + '/Data/atp_matches*.csv'

print(paths)