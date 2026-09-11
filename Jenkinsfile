pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

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

                        def status = sh(
                            script: """
                                python3 ci/sha_state.py get \
                                    --sha '${prSha}'
                            """,
                            returnStdout: true
                        ).trim()

                        echo "PR #${prNumber}"
                        echo "SHA: ${prSha}"
                        echo "Branch: ${prBranch}"
                        echo "Current CI state: ${status}"

                        if (status == 'success') {
                            echo 'Already successfully processed. Skipping.'
                            return
                        }

                        if (status == 'running') {
                            echo 'Already being processed. Skipping.'
                            return
                        }

                        echo "Scheduling PR #${prNumber}"

                        sh """
                            python3 ci/sha_state.py set \
                                --sha '${prSha}' \
                                --status running \
                                --pr '${prNumber}'
                        """

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