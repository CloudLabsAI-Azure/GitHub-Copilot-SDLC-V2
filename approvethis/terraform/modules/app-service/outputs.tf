output "app_service_name" {
  description = "Name of the App Service"
  value       = azurerm_linux_web_app.app.name
}

output "app_service_url" {
  description = "Default hostname of the App Service"
  value       = azurerm_linux_web_app.app.default_hostname
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.app.name
}

output "app_service_plan_id" {
  description = "ID of the App Service Plan"
  value       = azurerm_service_plan.app.id
}
