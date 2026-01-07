variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}

variable "storage_account_name" {
  description = "Name of the storage account (must be globally unique)"
  type        = string
}

variable "app_service_plan_name" {
  description = "Name of the App Service Plan"
  type        = string
}

variable "function_app_name" {
  description = "Name of the Function App (must be globally unique)"
  type        = string
}

variable "sku_name" {
  description = "SKU for the App Service Plan"
  type        = string
  default     = "B1"
}

variable "app_insights_key" {
  description = "Application Insights instrumentation key"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

variable "approvethis_api_url" {
  description = "URL of the ApproveThis application API"
  type        = string
  default     = ""
}

variable "approvethis_api_key" {
  description = "API key for authenticating with ApproveThis"
  type        = string
  default     = ""
  sensitive   = true
}

variable "github_token" {
  description = "GitHub Personal Access Token for API communication"
  type        = string
  default     = ""
  sensitive   = true
}

variable "cors_allowed_origins" {
  description = "List of allowed origins for CORS"
  type        = list(string)
  default     = ["*"]
}

variable "additional_app_settings" {
  description = "Additional app settings to add to the function app"
  type        = map(string)
  default     = {}
}
