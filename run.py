import os, filehelper, tree, sys

import tests.add_add as add_add
import tests.update_update as update_update
import tests.add_child_remove_parent as add_child_remove_parent
import tests.update_child_remove_parent as update_child_remove_parent

folders = ["Dropbox", "Google Drive", "OneDrive", "ownCloud"]
tests = [add_add, update_update, add_child_remove_parent, update_child_remove_parent]
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

def getWinningChange(test, folder, client, direction):
    os.chdir(os.path.join(str(client), folder, getTestName(test) + str(direction)))
    winningChange = test.getWinningChange()
    os.chdir(os.path.join("..", "..", ".."))
    return winningChange

# expects client sync folders in two folders: 1 and 2
def evaluate():
    print("Evaluating, writing result to " + evalDir)

    print("Cleaning evaluation directory")
    filehelper.clean(evalDir)

    for test in tests:
        testName = getTestName(test)
        print("Evaluation of test " + testName)

        summaryFileName = os.path.join(evalDir, testName)
        filehelper.write(summaryFileName, "# Sync Client, Result when syncing change 1 first (1/2: change 1/2 won, 0: neither change won, -1: inconsistent states), Result when syncing change 2 first\n")

        for folder in folders:
            results = []
            for direction in [1, 2]:
                # detect winning change only on client 1 (if client 2 has an different state, we detect this through the tree view)
                winningChange = getWinningChange(test, folder, 1, direction)

                # detect inconsistency by comparing directory contents
                treeClient1 = tree.tree(os.path.join("1", folder, testName + str(direction)))
                treeClient2 = tree.tree(os.path.join("2", folder, testName + str(direction)))

                if treeClient1 != treeClient2:
                    filehelper.write(os.path.join(evalDir, testName + str(direction), folder + "1"), treeClient1)
                    filehelper.write(os.path.join(evalDir, testName + str(direction), folder + "2"), treeClient2)
                    winningChange = -1
                results.append(winningChange)
            # write results
            filehelper.append(summaryFileName, "{},{}\n".format(folder, ",".join(map(str, results))))
        

def run(step, client=None):
    if step == "setup":
        setup()
    elif step == "change":
        change(client)
    elif step == "evaluate":
        evaluate()
    else:
        print("Unrecognized command. Use setup, change, evaluate")

if __name__ == "__main__":
    run(*sys.argv[1:])
