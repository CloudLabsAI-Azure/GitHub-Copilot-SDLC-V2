# Azure App Service Module
# This module creates an Azure App Service for hosting web applications
# To be customized in lab exercises

resource "azurerm_resource_group" "app" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

resource "azurerm_service_plan" "app" {
  name                = var.app_service_plan_name
  resource_group_name = azurerm_resource_group.app.name
  location            = azurerm_resource_group.app.location
  os_type             = "Linux"
  sku_name            = var.sku_name
  tags                = var.tags
}

resource "azurerm_linux_web_app" "app" {
  name                = var.app_service_name
  resource_group_name = azurerm_resource_group.app.name
  location            = azurerm_resource_group.app.location
  service_plan_id     = azurerm_service_plan.app.id
  tags                = var.tags

  site_config {
    always_on = var.always_on

    application_stack {
      python_version = var.python_version
    }
  }

  app_settings = var.app_settings

  # Lab exercise: Configure deployment slots
  # Lab exercise: Set up custom domains
  # Lab exercise: Configure authentication
}
