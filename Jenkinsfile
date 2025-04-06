pipeline {
  agent { label 'master' }

  environment {
    AZURE_CLIENT_ID       = credentials('azure-client-id')
    AZURE_CLIENT_SECRET   = credentials('azure-client-secret')
    AZURE_TENANT_ID       = credentials('azure-tenant-id')
    AZURE_SUBSCRIPTION_ID = credentials('azure-subscription-id')
  }

  stages {
    stage('Azure Login') {
      steps {
        dir('/app') {
          sh '''
          az login --service-principal \
            -u "$AZURE_CLIENT_ID" \
            -p "$AZURE_CLIENT_SECRET" \
            --tenant "$AZURE_TENANT_ID"
          az account set --subscription "$AZURE_SUBSCRIPTION_ID"
          '''
        }
      }
    }

    stage('Terraform Deploy Infra') {
      steps {
        dir('/app') {
          sh '''
          terraform init
          terraform apply -auto-approve
          '''
        }
      }
    }

    stage('Zip Function Code') {
      steps {
        dir('/app') {
          sh 'zip -r app.zip function_app.py requirements.txt host.json'
        }
      }
    }

    stage('Deploy Function to Azure') {
      steps {
        dir('/app') {
          sh '''
          az functionapp deployment source config-zip \
            --resource-group tf-contactapi-rg \
            --name tf-contact-api-demo \
            --src app.zip
          '''
        }
      }
    }
  }
}
