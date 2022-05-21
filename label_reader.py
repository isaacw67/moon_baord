import numpy as np
import pandas as pd
import pathlib as fl
import os as os
from PIL import Image
import pytesseract




def read_in(path):

    p = fl.Path(path)
    p.resolve
    pos_fls = os.listdir(p)
    print()
    words = []

    # Go through pos:

    for file_name in range(1,len(pos_fls)):
        # Get all words in 'file_name' and store them in a string\
        if file_name % 3000 == 0:
            print(file_name)
        words.append(parse_lab(pytesseract.image_to_string(Image.open(path + "/" + str(file_name)+".png"))))

    return words

def del_prefix(word):
    remove_strs = ['(B}','CB}','CB)','(B)','+','™','»','©','te)','[8','x)','uJ','[co]','0','>', 'Â©','ui', 'ST)']
    for pref in remove_strs:
        if word.startswith(pref):
            return (word.removeprefix(pref), True)

    return (word, False)
def parse_lab(label):
    # '(B} FAR FROM THE MADDING CROWD\nBen Moon\n20928 repeats\n6B+ (User grade 6B+)\nFeet follow hands\n\nKKKKY\n\neee\n'
    #
    parts = label.split('\n')
    parts[0] = parts[0].strip()
    rep = True
    while rep:
        parts[0] = parts[0].strip()
        (parts[0], rep) = del_prefix(parts[0])
    parts[0] = parts[0].strip()

    # Remove any empty strings
    num_remove = parts.count('')
    while num_remove > 0:
        parts.remove('')
        num_remove -= 1

    parts[0] = parts[0].replace('|','I')
    if (len(parts) > 7):
        print(parts)
        parts = parts[0:7]
    return parts

def create_names():
    df = pd.read_csv("labels.csv")
    # Need to find the place of all numbers, where
    # the entire name is within a string above it.
    # Need to track by ID, since its possible that two names match perfectly
    df['ex'] = 0
    count = 0
    for i in range(0, len(df)):
        if i % 1000 == 0:
            print(str(i))
        count = find_count_above(df['Name'][i], i, df)
        df['ex'][i] = count
    df[['Name', 'ex']].to_csv('names.txt', index = False, quoting = None)

def edit_names(path):
    df = pd.read_csv(path)
    df['total_app'] = np.where(df['ex_scroll'] > 0, 1, 0)
    for i in range(0, len(df)):
        if i % 1000 == 0:
            print(str(i))
        df['total_app'][i] = find_count_mod(df.loc[i]['Name'], i, df)
    df.to_csv('mod_names.txt', index = False, quoting = None)

def find_count_above(word, index, df):
    count = 0
    for i in range(0, index):
        if word in df['Name'][i]:
            count += 1
    return count

def find_count_mod(word, index, df):
    if df.loc[index]['ex_scroll'] == 0:
        return 1
    count = 0
    for i in range(0, len(df)):
        if word in df.loc[i]['Name']:
            count += 1
    return count

def create_pd_frame(words):
    ret = pd.DataFrame(words, columns= ['Name', 'Creator', 'Repeats', 'Grade', 'Type', 'Stars1', 'Stars2'])
    ret.to_csv("labels.csv")
    return ret

def calc_offset(path):
    df = pd.read_csv(path)
    df['offset'] = df['total_app'] - df['ex_scroll']
    df['offset'] = np.where(df['offset'] < 9, df['offset'], 0)
    df['offset'] = np.where(df['offset'] > 0, df['offset'] - np.mod(df['ex_scroll'], 8), 0)
    df['ex_scroll'] = np.where(df['offset'] > 0, df['ex_scroll'] - np.mod(df['ex_scroll'], 8), 0)
    df.to_csv("offset.txt")



    
    
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"
    #print(parse_lab('(B} FAR FROM THE MADDING CROWD\nBen Moon\n20928 repeats\n6B+ (User grade 6B+)\nFeet follow hands\n\nKKKKY\n\neee\n'))
    #df = create_pd_frame(read_in("C:/Users/isaac/Pictures/win_label"))
    #create_names()
    #df = pd.read_csv("labels_backup.csv")
    #print(df.columns)
    #calc_offset('mod_names.txt')
    edit_names("names_orig.txt")