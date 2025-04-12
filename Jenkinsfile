pipeline {
    agent any

    environment {
        IMAGE_NAME = "pau-app"
        CONTAINER_NAME = "pau-container"
        ENV_FILE = ".env"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/antdevi/PAU', credentialsId: 'antdevi'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME -f docker/Dockerfile .'
            }
        }

        stage('Stop Existing Container (if running)') {
            steps {
                sh '''
                if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
                  docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME
                fi
                '''
            }
        }

        stage('Run Docker Container with .env') {
            steps {
                sh 'docker run -d -e OPENAI_API_KEY=$OPENAI_API_KEY -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME'
            }
        }
    }

    post {
        always {
            echo '✅ CI/CD process complete.'
        }
    }
}
