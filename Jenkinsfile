pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('openai-api-key')
        IMAGE_NAME = 'pau-flask-app'
        CONTAINER_NAME = 'silly_bassi'
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
                sh 'docker build -t ${IMAGE_NAME} -f docker/Dockerfile .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d --name ${CONTAINER_NAME} -p ${PORT}:${PORT} -e OPENAI_API_KEY=${OPENAI_API_KEY} ${IMAGE_NAME}'
            }
        }

        stage('Save and Transfer Image to EC2'){
            steps{
                script{
                    def tarFile = "${IMAGE_NAME}.tar"
                    sh "docker save -o ${tarFile} ${IMAGE_NAME}"
                    
                    sshagent (credentials: ['ec2-ssh']) {
                        sh """
                        scp -o StrictHostKeyChecking=no ${tarFile} ec2-user@<YOUR_EC2_PUBLIC_IP>:/home/ec2-user/
                        ssh ec2-user@<YOUR_EC2_PUBLIC_IP> << EOF
                            docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q . && docker stop ${CONTAINER_NAME} || echo "No container running"
                            docker ps -a -q --filter "name=${CONTAINER_NAME}" | grep -q . && docker rm ${CONTAINER_NAME} || echo "No container to remove"
                            docker load -i ${tarFile}
                            docker run -d --name ${CONTAINER_NAME} -p ${PORT}:${PORT} -e OPENAI_API_KEY=${OPENAI_API_KEY} ${IMAGE_NAME}
                        EOF
                        """         
                }
            }
        }
    }

    post {
        always {
            echo 'Cleanup, report, or notify if needed.'
        }
    }
}}
