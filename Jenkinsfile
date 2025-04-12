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
                bat 'docker build -t %IMAGE_NAME% -f docker/Dockerfile .'
            }
        }

        stage('Stop Existing Container (if running)') {
            steps {
                bat '''
                FOR /F "tokens=*" %%i IN ('docker ps -q -f "name=%CONTAINER_NAME%"') DO (
                    docker stop %%i
                    docker rm %%i
                )
                '''
            }
        }

        stage('Run Docker Container with .env') {
            steps {
                bat 'docker run -d --env-file %ENV_FILE% -p 5000:5000 --name %CONTAINER_NAME% %IMAGE_NAME%'
            }
        }
    }

    post {
        always {
            echo '✅ CI/CD process complete.'
        }
    }
}
