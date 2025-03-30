pipeline {
    agent any

    environment {
        IMAGE_NAME = 'pau-flask-app'
        CONTAINER_NAME = 'loving_johnson'
        PORT = '5000'
    }

    stages {
        stage('Prepare') {
            steps {
                echo "Code checked out by Jenkins SCM."
                sh 'ls -l'
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
                sh 'docker build -t ${IMAGE_NAME} ./docker'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d --name ${CONTAINER_NAME} -p ${PORT}:${PORT} ${IMAGE_NAME}'
            }
        }
    }

    post {
        always {
            echo 'Cleanup, report, or notify if needed.'
        }
    }
}
