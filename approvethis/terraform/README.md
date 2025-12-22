# Terraform Infrastructure for ApproveThis

This directory contains Terraform configurations for deploying the ApproveThis application infrastructure on Azure.

## Structure

```
terraform/
├── modules/               # Reusable Terraform modules
│   ├── azure-function/   # Azure Function for Terraform execution
│   ├── app-service/      # Azure App Service for web app
│   └── storage-account/  # Azure Storage Account
└── environments/         # Environment-specific configurations
    ├── dev/             # Development environment
    ├── staging/         # Staging environment
    └── production/      # Production environment
```

## Modules

### azure-function

Creates an Azure Function App for executing Terraform operations remotely. This module will be fully implemented in lab exercises.

**Resources:**
- Resource Group
- Storage Account (for Function App)
- App Service Plan
- Linux Function App

**To be implemented in labs:**
- Function code deployment
- Authentication configuration
- Terraform execution environment setup

### app-service

Creates an Azure App Service for hosting the ApproveThis web application.

**Resources:**
- Resource Group
- App Service Plan
- Linux Web App

**Customization options in labs:**
- Deployment slots
- Custom domains
- Authentication providers

### storage-account

Creates an Azure Storage Account for application data and backups.

**Resources:**
- Resource Group
- Storage Account
- Storage Containers

**Enhancement options in labs:**
- Network rules
- Advanced threat protection
- Lifecycle management

## Environments

Each environment (dev, staging, production) composes the modules with environment-specific configuration:

- **dev**: Development environment with minimal resources (B1 tier)
- **staging**: Staging environment with production-like setup (S1 tier)
- **production**: Production environment with high availability (P1V2 tier, GRS storage)

## Prerequisites

1. **Azure CLI**: Install and login
   ```bash
   az login
   ```

2. **Terraform**: Install Terraform >= 1.0
   ```bash
   terraform --version
   ```

3. **Azure Subscription**: Ensure you have an active Azure subscription with appropriate permissions

## Getting Started

### Running Terraform Locally

1. Navigate to the desired environment:
   ```bash
   cd environments/dev
   ```

2. Copy the example variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your values:
   - Update resource names (must be globally unique)
   - Set location if different from default
   - Configure any sensitive variables

4. Initialize Terraform:
   ```bash
   terraform init
   ```

5. Review the execution plan:
   ```bash
   terraform plan
   ```

6. Apply the configuration:
   ```bash
   terraform apply
   ```

### Running via GitHub Actions

The repository includes GitHub Actions workflows for automated Terraform operations:

- **terraform-plan.yml**: Run Terraform plan
- **terraform-apply.yml**: Apply Terraform changes
- **terraform-destroy.yml**: Destroy infrastructure

To use these workflows:

1. Configure GitHub secrets:
   - `AZURE_CREDENTIALS`: Azure service principal credentials
   - `TF_VAR_*`: Terraform variables (e.g., `TF_VAR_database_url`)

2. Trigger workflow via GitHub UI or workflow dispatch

3. Review workflow logs for results

### Running via Azure Function

The Azure Function provider allows executing Terraform from the ApproveThis application:

1. Deploy the Azure Function using Terraform
2. Configure the function URL in ApproveThis config
3. Use the Jobs UI to trigger Terraform operations

This will be implemented in lab exercises.

## State Management

### Development

Development environment uses local state (`terraform.tfstate`) for simplicity.

**Warning**: Local state is not suitable for team collaboration or production use.

### Staging and Production

For staging and production, configure Azure Storage backend:

1. Create a storage account for Terraform state:
   ```bash
   az group create --name rg-terraform-state --location eastus
   az storage account create --name stterraformstate --resource-group rg-terraform-state --location eastus --sku Standard_LRS
   az storage container create --name tfstate --account-name stterraformstate
   ```

2. Uncomment the `backend "azurerm"` block in `backend.tf`

3. Run `terraform init` to migrate state

## Variable Management

### Required Variables

All environments require:
- `storage_account_name`: Globally unique, 3-24 lowercase letters/numbers
- `function_storage_name`: Globally unique, 3-24 lowercase letters/numbers
- `app_service_name`: Globally unique
- `function_app_name`: Globally unique

### Optional Variables

- `location`: Azure region (default: "East US")
- `database_url`: Database connection string (use environment variables in CI/CD)

### Sensitive Variables

Never commit sensitive values to version control:
- Use `terraform.tfvars` (add to `.gitignore`)
- Use environment variables: `TF_VAR_variable_name`
- Use Azure Key Vault in production

## Common Commands

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Format code
terraform fmt -recursive

# Plan changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Show current state
terraform show

# List resources
terraform state list

# Destroy infrastructure
terraform destroy

# Output values
terraform output
```

## Troubleshooting

### Name already exists

Azure resource names must be globally unique. If you get a "name already exists" error:
- Modify the resource name in `terraform.tfvars`
- Add a random suffix or your initials

### Authentication errors

Ensure you're logged in to Azure:
```bash
az login
az account show
```

### State lock errors

If using Azure Storage backend and state is locked:
```bash
terraform force-unlock <lock-id>
```

## Lab Exercises

This Terraform configuration provides the foundation for hands-on lab exercises:

### Lab 1: Deploy Development Environment
- Customize variable values
- Deploy infrastructure locally
- Verify resources in Azure Portal

### Lab 2: Implement Azure Function
- Add function code deployment
- Configure Terraform execution environment
- Test Terraform operations via function

### Lab 3: Set up GitHub Actions
- Configure workflows
- Add Azure credentials to GitHub
- Trigger automated deployments

### Lab 4: Production Deployment
- Configure Azure Storage backend
- Set up approval workflows
- Deploy to production environment

## Best Practices

1. **Always run `terraform plan`** before `apply`
2. **Use remote state** for team collaboration
3. **Never commit** `terraform.tfvars` or `.tfstate` files
4. **Use modules** for reusable infrastructure patterns
5. **Tag all resources** for cost tracking and organization
6. **Use workspaces** for managing multiple environments (alternative to separate directories)
7. **Lock Terraform version** in production
8. **Review changes** carefully before applying to production

## Additional Resources

- [Terraform Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure Terraform Quickstarts](https://learn.microsoft.com/en-us/azure/developer/terraform/)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Terraform and Azure documentation
3. Consult with your lab instructor
