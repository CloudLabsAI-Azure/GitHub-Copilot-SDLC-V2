# Azure Storage Account Module
# This module creates an Azure Storage Account
# To be customized in lab exercises

resource "azurerm_resource_group" "storage" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.storage.name
  location                 = azurerm_resource_group.storage.location
  account_tier             = var.account_tier
  account_replication_type = var.replication_type
  tags                     = var.tags

  # Lab exercise: Configure network rules
  # Lab exercise: Enable advanced threat protection
  # Lab exercise: Set up lifecycle management
}

resource "azurerm_storage_container" "containers" {
  for_each              = toset(var.container_names)
  name                  = each.value
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}
