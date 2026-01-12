# Azure Function Module
# This module creates an Azure Function App for the ApproveThis approval workflow
# The functions facilitate communication between GitHub Actions and the ApproveThis application

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

resource "azurerm_linux_function_app" "approval_functions" {
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
    
    cors {
      allowed_origins = var.cors_allowed_origins
      support_credentials = false
    }
  }

  app_settings = merge(
    {
      "FUNCTIONS_WORKER_RUNTIME"       = "python"
      "APPINSIGHTS_INSTRUMENTATIONKEY" = var.app_insights_key
      "APPROVETHIS_API_URL"            = var.approvethis_api_url
      "APPROVETHIS_API_KEY"            = var.approvethis_api_key
      "GITHUB_TOKEN"                   = var.github_token
      "WEBSITE_RUN_FROM_PACKAGE"       = "1"
    },
    var.additional_app_settings
  )

  # Enable system-assigned managed identity for secure access to Azure resources
  identity {
    type = "SystemAssigned"
  }
}
