# Azure Function Module
# This module will create an Azure Function App for executing Terraform operations
# To be implemented in lab exercises

resource "azurerm_resource_group" "function" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

resource "azurerm_storage_account" "function" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.function.name
  location                 = azurerm_resource_group.function.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags                     = var.tags
}

resource "azurerm_service_plan" "function" {
  name                = var.app_service_plan_name
  resource_group_name = azurerm_resource_group.function.name
  location            = azurerm_resource_group.function.location
  os_type             = "Linux"
  sku_name            = var.sku_name
  tags                = var.tags
}

resource "azurerm_linux_function_app" "terraform_executor" {
  name                       = var.function_app_name
  resource_group_name        = azurerm_resource_group.function.name
  location                   = azurerm_resource_group.function.location
  storage_account_name       = azurerm_storage_account.function.name
  storage_account_access_key = azurerm_storage_account.function.primary_access_key
  service_plan_id            = azurerm_service_plan.function.id
  tags                       = var.tags

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"       = "python"
    "APPINSIGHTS_INSTRUMENTATIONKEY" = var.app_insights_key
    # Additional settings will be configured in lab exercises
  }

  # Lab exercise: Implement function code deployment
  # Lab exercise: Configure authentication
  # Lab exercise: Set up Terraform execution environment
}
