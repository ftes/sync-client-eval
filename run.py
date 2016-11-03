import os, filehelper, tree, sys, filecmp

import tests.example as example

folders = ["Dropbox", "Google Drive", "OneDrive", "ownCloud"]
tests = [example]
evalDir = "eval"

def getTestName(testModule):
    return testModule.__name__.split(".")[1]

def setup():
    print("Performing setup of tests")

    # clean folders
    print("Cleaning sync client folders")
    for folder in folders:
        filehelper.clean(folder)

    # perform setup of all tests
    for test in tests:
        for direction in [1, 2]:
            testName = getTestName(test) + str(direction)
            print("Setting up test " + testName)
            for folder in folders:
                print("  for sync client " + folder)
                os.chdir(folder)
                filehelper.mkdir(testName)
                os.chdir(testName)
                test.setup()
                os.chdir(os.path.join("..", ".."))

def change(client):
    if client != "1" and client != "2":
        print("Unrecognized client. Use 1 or 2")
        return

    print("Performing change of tests for client " + client)
    for test in tests:
        for direction in [1, 2]:
            testName = getTestName(test) + str(direction)
            print("Changes for test " + testName)
            for folder in folders:
                print("  for sync client " + folder)
                os.chdir(os.path.join(folder, testName))
                test.change1() if client == str(direction) else test.change2()
                os.chdir(os.path.join("..", ".."))

def evaluate():
    print("Performing evaluation, writinig result to " + evalDir)

    print("Cleaning evaluation directory")
    filehelper.clean(evalDir)

    for test in tests:
        testName = getTestName(test)
        print("Evaluation of test " + testName)
        for folder in folders:
            print("  for sync client " + folder)
            # read results for direction 1
            os.chdir(os.path.join(folder, testName + "1"))
            winningChange1 = test.getWinningChange()
            directoryStructure1 = tree.tree(".")
            os.chdir(os.path.join("..", ".."))

            # read results for direction 2
            os.chdir(os.path.join(folder, testName + "2"))
            winningChange2 = test.getWinningChange()
            directoryStructure2 = tree.tree(".")
            os.chdir(os.path.join("..", ".."))
            
            # output results
            summaryFile = os.path.join(evalDir, testName, "summary")
            filehelper.append(summaryFile, "{},{},{}\n".format(folder, winningChange1, winningChange2))
            filehelper.write(os.path.join(evalDir, testName, folder + "1"), directoryStructure1)
            filehelper.write(os.path.join(evalDir, testName, folder + "2"), directoryStructure2)

# expects evaluation results in two folders: 1 and 2
def merge():
    print("Merging evaluation, writinig result to " + evalDir)

    print("Cleaning evaluation directory")
    filehelper.clean(evalDir)

    for test in tests:
        testName = getTestName(test)
        print("Merging results of test " + testName)

        summaryFileName = os.path.join(evalDir, testName)
        filehelper.write(summaryFileName, "# Sync Client, Result when syncing change 1 first (1/2: change 1/2 won, 0: neiter change won, -1: inconsistent states), Result when syncing change 2 first\n")
        summaryClient1FileName = os.path.join("1", testName, "summary")
        summary2ClientFileName = os.path.join("2", testName, "summary")

        with open(summaryClient1FileName, "r") as client1File, open(summary2ClientFileName, "r") as client2File:
            for folder in folders:
                # detect inconsistency
                client1Result = client1File.readline().rstrip().split(",")
                client2Result = client2File.readline().rstrip().split(",")
                # different directory contents are also inconsistent
                if not filecmp.cmp(os.path.join("1", testName, folder + "1"), os.path.join("2", testName, folder + "1")): winningChangeDirection1 = -1
                if not filecmp.cmp(os.path.join("1", testName, folder + "2"), os.path.join("2", testName, folder + "2")): winningChangeDirection2 = -1

                # write result
                filehelper.append(summaryFileName, "{},{},{}\n".format(folder, winningChangeDirection1, winningChangeDirection2))

        

def run(step, client=None):
    if step == "setup":
        setup()
    elif step == "change":
        change(client)
    elif step == "evaluate":
        evaluate()
    elif step == "merge":
        merge()
    else:
        print("Unrecognized command. Use setup, change, evaluate or merge")

if __name__ == "__main__":
    run(*sys.argv[1:])
