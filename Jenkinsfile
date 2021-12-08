// Hyungmin Han 12/08/2021
// Jenkins pipline for python bookstore app
pipeline {
    agent any
    parameters {
        booleanParam(defaultValue: false, description: 'Run Unit Test', name: 'TEST')
    }
    stages {
        stage('Build') {
            steps {
                echo 'installing the Python Requirements...'
                echo 'Student number: A01088624, Grp Num: 17'
                sh 'pip install -r requirements.txt'
                echo 'Requirement complete'
            }
        }
        stage('Code Quality') {
            steps {
                sh 'pylint-fail-under --fail_under 7.0 *.py'
            }
        }
        stage("Code Quantity") {
            steps {
                sh "ls *.py | wc -l"
            }
        }
        stage("Test") {
            when {
                expression {params.TEST}
            }
            post {
                always {
                    script{
                        sh "python3 test_book_manager.py"
                    }
                }
            }
        }
        stage('Zip Artifacts') {
            steps {
                sh 'zip package.zip *.py'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'package.zip', 
                    onlyIfSuccessful: true
                }
            }
        }
    }
}