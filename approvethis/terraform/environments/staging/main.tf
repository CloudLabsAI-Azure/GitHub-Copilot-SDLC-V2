# Staging Environment Configuration

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

module "storage" {
  source = "../../modules/storage-account"

  resource_group_name  = "rg-approvethis-staging"
  location             = var.location
  storage_account_name = var.storage_account_name
  container_names      = ["uploads", "backups", "terraform-state"]

  tags = local.common_tags
}

module "app_service" {
  source = "../../modules/app-service"

  resource_group_name      = "rg-approvethis-app-staging"
  location                 = var.location
  app_service_plan_name    = "asp-approvethis-staging"
  app_service_name         = var.app_service_name
  sku_name                 = "S1"
  python_version           = "3.11"
  always_on                = true

  app_settings = {
    "ENVIRONMENT"        = "staging"
    "FLASK_ENV"          = "production"
    "DATABASE_URL"       = var.database_url
    "GITHUB_PROVIDER"    = "real"
  }

  tags = local.common_tags
}

module "terraform_function" {
  source = "../../modules/azure-function"

  resource_group_name      = "rg-approvethis-func-staging"
  location                 = var.location
  storage_account_name     = var.function_storage_name
  app_service_plan_name    = "asp-terraform-staging"
  function_app_name        = var.function_app_name
  sku_name                 = "S1"

  tags = local.common_tags
}

locals {
  common_tags = {
    Environment = "staging"
    Project     = "ApproveThis"
    ManagedBy   = "Terraform"
  }
}
