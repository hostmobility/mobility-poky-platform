pipeline {
    agent any

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
    }
}