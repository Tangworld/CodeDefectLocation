
def main():
    resource = open('data/aspectj.csv', 'r')
    lines = resource.readlines()
    resource.close()

    bugids = []
    for i in range(1, len(lines)):
        bugid = lines[i].split(',')[0]
        print bugid
        bugids.append(int(bugid))
    print len(lines)
    print len(bugids)
    r_bugids = list(set(bugids))
    print len(r_bugids)
    bugidmap = open('data/BugidMap.txt', 'w')
    for r in r_bugids:
        print >> bugidmap, r
    bugidmap.close()

if __name__ == "__main__":
    main()