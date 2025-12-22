# Backend configuration for production Terraform state

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# IMPORTANT: For production, use Azure Storage backend:
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "rg-terraform-state"
#     storage_account_name = "stterraformstate"
#     container_name       = "tfstate"
#     key                  = "approvethis/production.tfstate"
#   }
# }
