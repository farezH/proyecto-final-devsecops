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
                trivy image \
                --exit-code 1 \
                --severity CRITICAL \
                ${IMAGE_NAME}:${BUILD_NUMBER}
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

