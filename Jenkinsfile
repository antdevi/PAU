pipeline {
    agent any

    environment {
        PROJECT_NAME = 'PAU'
        DOCKER_IMAGE = 'pau-app'
        DOCKER_CONTEXT = 'docker'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Environment') {
            steps {
                script {
                    if (fileExists('.env')) {
                        def props = readFile('.env').split("\n")
                        for (line in props) {
                            if (line.trim() && !line.startsWith("#")) {
                                def keyValue = line.trim().split("=")
                                if (keyValue.length == 2) {
                                    env."${keyValue[0]}" = keyValue[1]
                                }
                            }
                        }
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            when {
                expression { fileExists('tests') }
            }
            steps {
                sh 'pytest tests/'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir("${DOCKER_CONTEXT}") {
                    sh '''
                        cp ../.env .env
                        docker build -t ${DOCKER_IMAGE} --build-arg OPENAI_API_KEY=$OPENAI_API_KEY -f Dockerfile ..
                    '''
                }
            }
        }

        stage('Docker Compose (Optional)') {
            when {
                expression { fileExists("${DOCKER_CONTEXT}/docker-compose.yml") }
            }
            steps {
                dir("${DOCKER_CONTEXT}") {
                    sh 'docker-compose up -d --build'
                }
            }
        }
    }

    post {
        success {
            echo "✅ Jenkins pipeline for ${PROJECT_NAME} completed successfully."
        }
        failure {
            echo "❌ Pipeline failed for ${PROJECT_NAME}. Check logs above."
        }
        cleanup {
            sh 'docker system prune -f'
        }
    }
}
