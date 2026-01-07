output "function_app_name" {
  description = "Name of the Function App"
  value       = azurerm_linux_function_app.approval_functions.name
}

output "function_app_url" {
  description = "Default hostname of the Function App"
  value       = azurerm_linux_function_app.approval_functions.default_hostname
}

output "function_app_id" {
  description = "ID of the Function App"
  value       = azurerm_linux_function_app.approval_functions.id
}

output "function_app_identity_principal_id" {
  description = "Principal ID of the Function App's managed identity"
  value       = azurerm_linux_function_app.approval_functions.identity[0].principal_id
}

output "request_approval_url" {
  description = "URL for the request-approval function"
  value       = "https://${azurerm_linux_function_app.approval_functions.default_hostname}/api/approval/request"
}

output "approval_response_url" {
  description = "URL for the approval-response function"
  value       = "https://${azurerm_linux_function_app.approval_functions.default_hostname}/api/approval/response"
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.function.name
}

output "storage_account_name" {
  description = "Name of the storage account"
  value       = azurerm_storage_account.function.name
}
