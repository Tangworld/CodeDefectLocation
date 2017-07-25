def main():
    wordmap = open('WordMap.txt', 'r')
    lines = wordmap.readlines()
    wordmap.close()
    words = []
    for line in lines:
        line = line.replace('\n', '')
        words.append(line)
    finalwords = list(set(words))
    wordmap = open('WordMap.txt', 'w')
    for f in finalwords:
        print >> wordmap, f

if __name__ == '__main__':
    main()