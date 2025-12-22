# Development Environment Configuration
# This composes the modules to create a complete dev environment

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Storage Account for application data
module "storage" {
  source = "../../modules/storage-account"

  resource_group_name  = "rg-approvethis-dev"
  location             = var.location
  storage_account_name = var.storage_account_name
  container_names      = ["uploads", "backups", "terraform-state"]

  tags = local.common_tags
}

# App Service for the ApproveThis application
module "app_service" {
  source = "../../modules/app-service"

  resource_group_name      = "rg-approvethis-app-dev"
  location                 = var.location
  app_service_plan_name    = "asp-approvethis-dev"
  app_service_name         = var.app_service_name
  sku_name                 = "B1"
  python_version           = "3.11"
  always_on                = false

  app_settings = {
    "ENVIRONMENT"        = "dev"
    "FLASK_ENV"          = "development"
    "DATABASE_URL"       = var.database_url
    "GITHUB_PROVIDER"    = "mock"
  }

  tags = local.common_tags
}

# Azure Function for Terraform execution
module "terraform_function" {
  source = "../../modules/azure-function"

  resource_group_name      = "rg-approvethis-func-dev"
  location                 = var.location
  storage_account_name     = var.function_storage_name
  app_service_plan_name    = "asp-terraform-dev"
  function_app_name        = var.function_app_name
  sku_name                 = "B1"

  tags = local.common_tags
}

locals {
  common_tags = {
    Environment = "dev"
    Project     = "ApproveThis"
    ManagedBy   = "Terraform"
  }
}
