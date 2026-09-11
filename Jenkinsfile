pipeline {
    agent any

    /*triggers {
        cron('H 8-18 * * 1-5')
    }*/

    stages {
        stage('Checkout Info') {
            steps {
                echo 'mobility-poky-platform was checked out successfully'
                sh 'git rev-parse HEAD'
                sh 'git status --short --branch'
            }
        }

        stage('Hello') {
            steps {
                echo 'Hello from mobility-poky-platform CI!'
            }
        }

        stage('Find Open PRs') {
            steps {
                sh 'python3 ci/find_open_prs.py'
            }
        }

        stage('Trigger Candidate Jobs') {
            steps {
                script {
                    def candidates = readFile('candidates.tsv').trim()

                    if (!candidates) {
                        echo 'No candidate PRs to process.'
                        return
                    }

                    candidates.split('\n').each { line ->
                        def fields = line.split('\t')

                        def prNumber = fields[0]
                        def prSha = fields[1]
                        def prBranch = fields[2]

                        echo "Triggering build-test for PR #${prNumber}"
                        echo "SHA: ${prSha}"
                        echo "Branch: ${prBranch}"

                        build job: 'mobility-poky-platform-build',
                            wait: false,
                            parameters: [
                                string(
                                    name: 'PR_NUMBER',
                                    value: prNumber
                                ),
                                string(
                                    name: 'PR_SHA',
                                    value: prSha
                                ),
                                string(
                                    name: 'PR_BRANCH',
                                    value: prBranch
                                )
                            ]
                    }
                }
            }
        }
    }
}