import os

import testDeploy


def test_deploy():
    files = os.listdir('../results')
    for i in range(len(files)):
        files[i] = '../results/' + files[i]
    testDeploy.predict(testDeploy.load_model(), files)
