pipeline {
    agent any

    environment {
        IMAGE_NAME = 'pau-flask-app'
        CONTAINER_NAME = 'silly_bassi'
        PORT = '5000'
    }

    stages {
        stage('Prepare') {
            steps {
                echo "Code checked out by Jenkins SCM."
                sh 'ls -l'
                sh 'cat .env || echo ".env not found!"'
            }
        }

        stage('Stop and Remove Old Container') {
            steps {
                script {
                    sh '''
                    docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q . && docker stop ${CONTAINER_NAME} || echo "No container running"
                    docker ps -a -q --filter "name=${CONTAINER_NAME}" | grep -q . && docker rm ${CONTAINER_NAME} || echo "No container to remove"
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME} -f docker/Dockerfile .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d --name ${CONTAINER_NAME} -p ${PORT}:${PORT} --env-file .env ${IMAGE_NAME}'
            }
        }
    }

    post {
        always {
            echo 'Cleanup, report, or notify if needed.'
        }
    }
}
