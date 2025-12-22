output "function_app_name" {
  description = "Name of the Function App"
  value       = azurerm_linux_function_app.terraform_executor.name
}

output "function_app_url" {
  description = "Default hostname of the Function App"
  value       = azurerm_linux_function_app.terraform_executor.default_hostname
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.function.name
}

output "storage_account_name" {
  description = "Name of the storage account"
  value       = azurerm_storage_account.function.name
}
