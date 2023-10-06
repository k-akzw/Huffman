import operator

class Node:
    def __init__(self, symbol: str, freq, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
        self.huff = ""

class HuffmanCode:
    def __init__(self, symbols=[]):
        self.symbolDict = {}
        self.symbols = symbols
        self.inputSymbolsInDict()

    # create keys for each characters
    def inputSymbolsInDict(self):
        for ch in self.symbols:
            self.symbolDict[ch] = 0

    # calculate frequency for each character
    def getFrequency(self, text):
        i = 0
        while i < len(text):
            for j in range(3, -1, -1):
                if j == 0:
                    self.symbolDict[text[i]] = self.symbolDict.get(text[i],0) + 1
                    i += 1
                if text[i:i+j] in self.symbolDict:
                    self.symbolDict[text[i:i+j]] += 1
                    i += j
                    break
    
    def sortDict(self):
        self.symbolList = sorted(self.symbolDict.items(), key=operator.itemgetter(1))
    
    def assignHuffman(self):
        l = Node(self.symbolList[0][0], self.symbolList[0][1])
        r = Node(self.symbolList[1][0], self.symbolList[1][1])
        l.huff = "0"
        r.huff = "1"
        i = 2
        while i < len(self.symbolList):
            p = Node("", l.freq+r.freq, l, r)
            newNode = Node(self.symbolList[i][0], self.symbolList[i][1])
            if p.freq < newNode.freq:
                l = p
                r = newNode
            else:
                l = newNode
                r = p
            l.huff = "0"
            r.huff = "1"
            i += 1
        self.p = Node("", l.freq+r.freq, l, r)
        self.getHuffman(self.p, "")

    def getHuffman(self, node: Node, val):
        huff = val+node.huff

        if node.left:
            self.getHuffman(node.left, huff)
        if node.right:
            self.getHuffman(node.right, huff)
        
        if not node.left and not node.right:
            self.symbolDict[node.symbol] = huff
    
    def printHuffman(self, file):
        for symbol in self.symbolDict:
            file.write(symbol + " " + self.symbolDict[symbol] + "\n")

    def textToHuffman(self, file, text):
        i = 0
        huff = ""
        while i < len(text):
            for j in range(3, -1, -1):
                if text[i:i+j] in self.symbolDict:
                    huff += self.symbolDict[text[i:i+j]]
                    i += j
        file.write(huff)


    def decode(self, file, text):
        res = ""
        i = 0
        while i < len(text):
            symbol, i = self.huffmanToText(text, i)
            res += symbol
        file.write(res)

    def huffmanToText(self, text, i):
        curr = self.p
        while curr.left and curr.right:
            if text[i] == "0":
                curr = curr.left
            else:
                curr = curr.right
            i += 1
        return curr.symbol, i


def main():
    test1 = HuffmanCode(["the", "and", "sh", "th", "e "])
    file = open("original.txt", "r")
    originalText = file.read()
    test1.getFrequency(originalText)
    test1.sortDict()
    test1.assignHuffman()
    file.close()
    file = open("table.txt", "w")
    test1.printHuffman(file)
    file.close()
    file = open("huffman.txt", "w")
    test1.textToHuffman(file, originalText)
    file.close()
    file = open("huffman.txt", "r")
    huff = file.read()
    file.close()
    file = open("decoded.txt", "w")
    test1.decode(file, huff)
    file.close()

main()