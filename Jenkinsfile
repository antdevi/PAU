pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('openai-api-key')
        IMAGE_NAME = 'pau-flask-app'
        CONTAINER_NAME = 'silly_bassi'
        PORT = '5000'
        EC2_IP = '13.126.149.202'
        REMOTE_USER = 'ec2-user'
        PEM_FILE_NAME = 'ec2-key.pem' // Use the actual file name of your PEM key
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
                sh '''
                    docker ps -q --filter "name=$CONTAINER_NAME" | grep -q . && docker stop $CONTAINER_NAME || echo "No container running"
                    docker ps -a -q --filter "name=$CONTAINER_NAME" | grep -q . && docker rm $CONTAINER_NAME || echo "No container to remove"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME -f docker/Dockerfile .'
            }
        }

        stage('Run Docker Locally') {
            steps {
                sh 'docker run -d --name $CONTAINER_NAME -p $PORT:$PORT -e OPENAI_API_KEY=$OPENAI_API_KEY $IMAGE_NAME'
            }
        }

        stage('Save and Deploy to EC2') {
            steps {
                withCredentials([file(credentialsId: 'ec2-pem-key', variable: 'EC2_PEM')]) {
                    script {
                        def tarFile = "${env.IMAGE_NAME}.tar"
                        sh """
                            echo 'Saving Docker image as TAR...'
                            docker save -o ${tarFile} ${IMAGE_NAME}

                            echo 'Transferring Docker image to EC2...'
                            scp -o StrictHostKeyChecking=no -i $EC2_PEM ${tarFile} ${REMOTE_USER}@${EC2_IP}:/home/${REMOTE_USER}/

                            echo 'Deploying on EC2...'
                            ssh -o StrictHostKeyChecking=no -i $EC2_PEM ${REMOTE_USER}@${EC2_IP} << 'EOF'
                                docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q . && docker stop ${CONTAINER_NAME} || echo "No container running"
                                docker ps -a -q --filter "name=${CONTAINER_NAME}" | grep -q . && docker rm ${CONTAINER_NAME} || echo "No container to remove"
                                docker load -i ${IMAGE_NAME}.tar
                                docker run -d --name ${CONTAINER_NAME} -p ${PORT}:${PORT} -e OPENAI_API_KEY=${OPENAI_API_KEY} ${IMAGE_NAME}
                            EOF
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline complete. Clean up or notify if needed.'
        }
    }
}
