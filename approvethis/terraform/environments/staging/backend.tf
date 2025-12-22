# Backend configuration for staging Terraform state

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# For production deployment, use Azure Storage:
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "rg-terraform-state"
#     storage_account_name = "stterraformstate"
#     container_name       = "tfstate"
#     key                  = "approvethis/staging.tfstate"
#   }
# }
