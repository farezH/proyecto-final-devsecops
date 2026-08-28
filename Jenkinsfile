pipeline {

    agent any

    environment {
        IMAGE_NAME = 'devsecops-app'
    }

    stages {

        stage('Checkout') {

            steps {
                checkout scm
            }
        }

        stage('Build') {

            steps {

                sh '''
                docker build \
                -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                ./app
                '''
            }
        }

        stage('Tests') {

            steps {

                sh '''
                docker run \
                --rm \
                ${IMAGE_NAME}:${BUILD_NUMBER} \
                pytest -q
                '''
            }
        }

        stage('Trivy Scan') {

            steps {

                sh '''
                docker save ${IMAGE_NAME}:${BUILD_NUMBER} -o app-image.tar

                trivy image \
                --input app-image.tar \
                --exit-code 1 \
                --severity CRITICAL \
                --scanners vuln
                '''
            }
        }

        stage('Deploy') {

            steps {

                sh '''
                APP_VERSION=${BUILD_NUMBER} \
                docker compose up \
                -d \
                --no-build \
                app1 app2 nginx
                '''
            }
        }
    }

    post {

        success {
            echo 'Pipeline completado correctamente.'
        }

        failure {
            echo 'Pipeline bloqueado.'
        }
    }
}

