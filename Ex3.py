import csv
import random

class Leaf:
    def __init__(self, feature, criteria):
        self.feature = feature
        self.criteria = criteria
        self.subtree_l = None
        self.subtree_h = None

class SLinkedList:
    def __init__(self):
        self.headval = None


feature_id=[]
feature_name=[]
coun = []
def read_csv (csv_file):
    global feature_id, feature_name, coun
    with open(csv_file, newline='\n', encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        feature_id=next(reader)[1:-1]
        feature_name=next(reader)[1:-1]
        for line in reader:
            ln=line[1:]
            ln=[int(x) for x in ln]
            coun.append(ln)

read_csv("DefaultOfCreditCardClients.csv")



def buildTree(k):
    dataSet, examinationSet = split_data(k)
    tresholds = setTresholds(dataSet)
    decision_Tree = recursiveBuildingTree(dataSet, tresholds, entropies, dataSet)
    print_tree(decision_Tree)
  #  print reportError(examinationSet, decision_Tree)

def split_data(k):
    dataSet, valSet = [], []
    lp=int(len(coun)*k)
    dataSet=random.choices(coun, k=lp)
    valSet=[l for l in coun if l not in dataSet]
    return dataSet, valSet

def setTresholds(dataset):
    avarage = [0] * len(feature_id)
    for i in dataset:
        for j in range(len(feature_id)):
            avarage[j] += i[j]
    for k in range(len(avarage)):
        avarage[k] = avarage[k] / float(len(dataset))
    return avarage



def calcEntropy(attribute, treshold, dataset):
    spam, ham = [], []
    for line in dataset:
        if line[attribute] > treshold:
            spam.append(line)
        else:
            ham.append(line)
    return entropy(len(spam)/float(len(spam) + len(ham)), len(ham)/float(len(spam)+len(ham)))

def splitLines(dataset, treshold, attribute):
    spam, ham = [], []
    for line in dataset:
        if line[attribute] > treshold:
            spam.append(line)
        else:
            ham.append(line)
    return spam, ham



def entropy(pos, neg):
    if pos == 0:
        return -(neg * float(math.log(neg, 2)))
    elif neg == 0:
        return -(pos * float(math.log(pos, 2)))
    else:
        return -(pos * float(math.log(pos, 2)))-(neg * float(math.log(neg, 2)))

def plurality(dataset):
    sumSpam, sumHam = 0, 0
    for line in dataset:
        if line[57] == 1:
            sumSpam += 1
        else:
            sumHam += 1
    if sumSpam > sumHam:
        return 1
    else:
        return 0

def treeError(k):
    errors= []
    sum = 0
    for i in k:
        errors[i] = kCrossValidation(i, k)
        sum += errors[i]
    return sum/float(k)


def kCrossValidation(i, k):
    dataSet, examinationSet = [], []
    for line in range(len(content)):
        if line < i*(k/i) and line > (i+1)*(k/i):
            dataSet.append(content[line])
        else:
            examinationSet.append(content[line])
    entropies = {}
    for i in range(56):
        entropies.setdefault(i)
    tresholds = setTresholds(dataSet)
    decision_tree = recursiveBuildingTree(dataSet, tresholds, entropies)
#    return reportError(examinationSet, decision_tree, tresholds)


def recursiveBuildingTree(dataset, tresholds, entropies, parentDataset):
    if len(dataset) == 0 or dataset is None:
        return plurality(parentDataset)
    else:
        sumSpam, sumHam = 0, 0
        for line in dataset:
            if line[57] == 1:
                sumSpam += 1
            else:
                sumHam += 1
        if sumSpam == len(dataset):
            return 1
        elif sumHam == len(dataset):
            return 0
        elif entropies is None or len(entropies) == 0:
            return plurality(dataset)
        else:
            for i in range(56):
                if i in entropies.keys():
                    entropies[i] = calcEntropy(i, tresholds[i], dataset)
            root = min(entropies.values())
            if root == 1:
                return
            else:
                spam, ham = [], []
                tree = SLinkedList()
                for j in range(56):
                    if j in entropies.keys():
                        if entropies[j] == root:
                            root = j
                            spam, ham = splitLines(dataset, tresholds[j], j)
                            entropies.pop(j)
                            break
                tree.headval = Leaf(root, tresholds[root])
                true_branch = recursiveBuildingTree(spam, tresholds, entropies, dataset)
                tree.headval.next_val_spam = true_branch
                false_branch = recursiveBuildingTree(ham, tresholds, entropies, dataset)
                tree.headval.next_val_ham = false_branch
                return tree

def print_tree(tree, depth=0):
    if isinstance(tree, SLinkedList):
        if (isinstance(tree.headval, Leaf)):
            print('%s[X%d > %.3f]' % (depth * ' ', tree.headval.attribute, tree.headval.treshold))
            print_tree(tree.headval.next_val_spam, depth + 1) #### תבדקי ששמתי נכון
            print_tree(tree.headval.next_val_ham, depth) #### תבדקי ששמתי נכון
    else:
        print('%s[%s]' % ((depth * ' ', tree)))


if __name__ == '__main__':
    # treeError(10)
    buildTree(0.5)
    # isThisSpam(np.array([0,0.64,0.64,0,0.32,0,0,0,0,0,0,0.64,0,0,0,0.32,0,1.29,1.93,0,0.96,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    # 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.778,0,0,3.756,61,278]))
