# Similarity Detection Library

# Globals
DUPLICATE_THRESHOLD = 0.75

# takes in a fingerprint and checks fingerprint dictionary for a match
# Arguments: 
# cur_fp, list of integers representing the fingerprint
def detect_near_similars(cur_fp, fingerprints):
    for fp in fingerprints:
        if similar(set(fp), set(cur_fp)):
            return True
    return False


def similar(A, B):
    global DUPLICATE_THRESHOLD
    card_union = sum([1 for i in A if i in B])
    s = card_union / (len(A) + len(B) - card_union)
    if s >= DUPLICATE_THRESHOLD:
        print("Similarity Factor:", s)
        return True
    else:
        return False
    #return s >= DUPLICATE_THRESHOLD


#detect near duplicates using fingerprint method
def compute_fingerprint(tokens):
    triple_lst = []
    #print(tokens)
    # add triplets to triple_lst
    for i in range(len(tokens)-2):
        triple_lst.append([tokens[i], tokens[i+1], tokens[i+2]])
    
    # hash each triplet
    hashed_lst = [fingerprint_hash(lst) for lst in triple_lst]
    res = [v for v in hashed_lst if v % 4 == 0]
    return res


def fingerprint_hash(word):
    res = 0
    for w in word:
        for c in w:
            res += ord(c)
    return res
