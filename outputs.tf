output "function_app_url" {
  value = "https://${azurerm_linux_function_app.function.default_hostname}/api/contact-api"
}
