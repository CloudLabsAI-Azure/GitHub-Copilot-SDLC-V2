# Backend configuration for Terraform state
# For dev environment, using local backend

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# For production, consider using Azure Storage backend:
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "rg-terraform-state"
#     storage_account_name = "stterraformstate"
#     container_name       = "tfstate"
#     key                  = "approvethis/dev.tfstate"
#   }
# }
