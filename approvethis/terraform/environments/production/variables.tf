variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}

variable "storage_account_name" {
  description = "Storage account name (must be globally unique)"
  type        = string
}

variable "app_service_name" {
  description = "App Service name (must be globally unique)"
  type        = string
}

variable "function_app_name" {
  description = "Function App name (must be globally unique)"
  type        = string
}

variable "function_storage_name" {
  description = "Function storage account name (must be globally unique)"
  type        = string
}

variable "database_url" {
  description = "Database connection string"
  type        = string
  sensitive   = true
  default     = ""
}
